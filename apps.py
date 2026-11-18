import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Ride Analytics | Executive View", page_icon="🚖", layout="wide")

DATA_FILE = "ncr_ride_bookingccccc.csv"  # matches the file name in your repo
PALETTE = ["#2563eb", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]

st.markdown("""
<style>
.block-container {padding-top: 1.5rem;}

/* ---------- KPI cards ---------- */
div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-left: 6px solid #2563eb;
    padding: 16px 20px;
    border-radius: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,.08);
}
/* label */
[data-testid="stMetric"] label,
[data-testid="stMetric"] label *,
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetric"] p {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    opacity: 1 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    white-space: normal !important;      /* don't cut the text with "..." */
    overflow: visible !important;
    text-overflow: clip !important;
}
/* big value */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #0f172a !important;
    font-weight: 800 !important;
    font-size: 1.7rem !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
}
/* delta */
div[data-testid="stMetricDelta"] {
    font-weight: 600 !important;
}

/* a different accent color for each card (supports old + new Streamlit) */
div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"],
div[data-testid="stColumn"]:nth-of-type(1) div[data-testid="stMetric"] {border-left-color: #2563eb;}
div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"],
div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stMetric"] {border-left-color: #10b981;}
div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"],
div[data-testid="stColumn"]:nth-of-type(3) div[data-testid="stMetric"] {border-left-color: #f59e0b;}
div[data-testid="column"]:nth-of-type(4) div[data-testid="stMetric"],
div[data-testid="stColumn"]:nth-of-type(4) div[data-testid="stMetric"] {border-left-color: #8b5cf6;}
div[data-testid="column"]:nth-of-type(5) div[data-testid="stMetric"],
div[data-testid="stColumn"]:nth-of-type(5) div[data-testid="stMetric"] {border-left-color: #ef4444;}

/* ---------- Revenue card (2nd card) ---------- */
div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"],
div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stMetric"] {
    background: #ecfdf5;
}
div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetricLabel"] *,
div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stMetricLabel"] * {
    color: #000000 !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: clip !important;
    font-weight: 700 !important;
}
div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetricValue"] *,
div[data-testid="stColumn"]:nth-of-type(2) div[data-testid="stMetricValue"] * {
    color: #064e3b !important;
    font-size: 1.7rem !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
}

.insight {background:#f0f6ff; border-radius:10px; padding:12px 16px; margin-bottom:8px; color:#1e3a8a;}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    if "Ride Start Datetime" in df.columns:
        df["Ride Start Datetime"] = pd.to_datetime(df["Ride Start Datetime"], errors="coerce")
    else:  # original NCR dataset has separate Date + Time columns
        df["Ride Start Datetime"] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str), errors="coerce")
    df = df.dropna(subset=["Ride Start Datetime"])
    df["Hour"] = df["Ride Start Datetime"].dt.hour
    df["Weekday"] = df["Ride Start Datetime"].dt.day_name()
    return df


df = load_data()

# ---------------- Sidebar ----------------
st.sidebar.header("🎛️ Filters")
dmin, dmax = df["Ride Start Datetime"].min().date(), df["Ride Start Datetime"].max().date()
date_range = st.sidebar.date_input("Date range", (dmin, dmax), min_value=dmin, max_value=dmax)
vehicles = st.sidebar.multiselect("Vehicle type", sorted(df["Vehicle Type"].dropna().unique()),
                                  default=sorted(df["Vehicle Type"].dropna().unique()))
statuses = st.sidebar.multiselect("Booking status", sorted(df["Booking Status"].dropna().unique()),
                                  default=sorted(df["Booking Status"].dropna().unique()))

if len(date_range) != 2:
    st.info("Select both a start and end date.")
    st.stop()

start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)
base = df[df["Vehicle Type"].isin(vehicles) & df["Booking Status"].isin(statuses)]
cur = base[(base["Ride Start Datetime"] >= start) & (base["Ride Start Datetime"] < end)]
prev_start = start - (end - start)
prev = base[(base["Ride Start Datetime"] >= prev_start) & (base["Ride Start Datetime"] < start)]

if cur.empty:
    st.warning("No data for the selected filters.")
    st.stop()


# ---------------- KPI helpers ----------------
def kpis(d):
    completed = d[d["Booking Status"] == "Completed"]
    return {
        "rides": len(d),
        "revenue": completed["Booking Value"].sum(),
        "avg_value": completed["Booking Value"].mean() if len(completed) else 0,
        "completion": len(completed) / len(d) * 100 if len(d) else 0,
        "cancel": d["Booking Status"].str.contains("Cancel", na=False).mean() * 100 if len(d) else 0,
    }


k, kp = kpis(cur), kpis(prev)


def delta(key, pct=False):
    if prev.empty or not kp[key]:
        return None
    return f"{k[key] - kp[key]:+.1f} pts" if pct else f"{(k[key] / kp[key] - 1) * 100:+.1f}%"


# ---------------- Header ----------------
st.title("🚖 NCR Ride Analytics — Executive Summary")
st.caption(f"{date_range[0]:%d %b %Y} → {date_range[1]:%d %b %Y}  •  changes vs. previous period of equal length")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Rides", f"{k['rides']:,}", delta("rides"))
c2.metric("Revenue (Completed)", f"${k['revenue']/1e6:,.2f}M" if k["revenue"] >= 1e6 else f"${k['revenue']:,.0f}", delta("revenue"))
c3.metric("Avg. Booking Value", f"${k['avg_value']:,.2f}", delta("avg_value"))
c4.metric("Completion Rate", f"{k['completion']:.1f}%", delta("completion", pct=True))
c5.metric("Cancellation Rate", f"{k['cancel']:.1f}%", delta("cancel", pct=True), delta_color="inverse")

# ---------------- Auto insights ----------------
completed = cur[cur["Booking Status"] == "Completed"]
insights = []
if len(completed):
    top_v = completed.groupby("Vehicle Type")["Booking Value"].sum().idxmax()
    insights.append(f"💡 **{top_v}** is the top revenue-generating vehicle type.")
    peak = cur.groupby("Hour").size().idxmax()
    insights.append(f"⏰ Demand peaks at **{peak}:00**; plan driver supply around this hour.")
canc = cur[cur["Booking Status"].str.contains("Cancel", na=False)]
if len(canc):
    insights.append(f"🚫 **{len(canc):,}** rides were cancelled — {k['cancel']:.1f}% of all bookings.")
st.markdown("### 🔎 Key Takeaways")
for i in insights:
    st.markdown(f'<div class="insight">{i}</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📈 Performance", "🚗 Vehicles & Pricing", "🚫 Cancellations", "🗂️ Data"])

# ---------------- Tab 1: Performance ----------------
with tab1:
    freq = st.radio("Granularity", ["Daily", "Weekly", "Monthly"], horizontal=True, index=1)
    rule = {"Daily": "D", "Weekly": "W", "Monthly": "MS"}[freq]
    ts = cur.resample(rule, on="Ride Start Datetime").agg(
        rides=("Booking Status", "size"),
        revenue=("Booking Value", lambda s: s[cur.loc[s.index, "Booking Status"] == "Completed"].sum()),
    ).reset_index()

    fig = go.Figure()
    fig.add_bar(x=ts["Ride Start Datetime"], y=ts["rides"], name="Rides", marker_color="#bfdbfe")
    fig.add_scatter(x=ts["Ride Start Datetime"], y=ts["revenue"], name="Revenue", yaxis="y2",
                    line=dict(color="#2563eb", width=3))
    fig.update_layout(title="Ride Volume & Revenue Trend", height=400, hovermode="x unified",
                      yaxis=dict(title="Rides"), yaxis2=dict(title="Revenue ($)", overlaying="y", side="right"),
                      legend=dict(orientation="h", y=1.12), template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heat = cur.pivot_table(index="Weekday", columns="Hour", values="Booking Status", aggfunc="size").reindex(order)
    fig_h = px.imshow(heat, aspect="auto", color_continuous_scale="Blues",
                      labels=dict(x="Hour of day", y="", color="Rides"), title="When Is Demand Highest?")
    fig_h.update_layout(height=380, template="plotly_white")
    st.plotly_chart(fig_h, use_container_width=True)

# ---------------- Tab 2: Vehicles & Pricing ----------------
with tab2:
    a, b = st.columns(2)
    rev_v = completed.groupby("Vehicle Type")["Booking Value"].sum().sort_values().reset_index()
    a.plotly_chart(px.bar(rev_v, x="Booking Value", y="Vehicle Type", orientation="h", text_auto=".2s",
                          title="Revenue by Vehicle Type", color_discrete_sequence=[PALETTE[0]])
                   .update_layout(template="plotly_white", height=400), use_container_width=True)

    share = cur["Vehicle Type"].value_counts().reset_index()
    share.columns = ["Vehicle Type", "Rides"]
    b.plotly_chart(px.pie(share, names="Vehicle Type", values="Rides", hole=.55, title="Ride Share by Vehicle",
                          color_discrete_sequence=PALETTE).update_layout(height=400), use_container_width=True)

    samp = completed.sample(min(len(completed), 2000), random_state=1) if len(completed) else completed
    st.plotly_chart(px.scatter(samp, x="Ride Distance", y="Booking Value", color="Vehicle Type", opacity=.6,
                               trendline="ols" if len(samp) > 10 else None,
                               title="Price vs. Distance (sampled)", color_discrete_sequence=PALETTE)
                    .update_layout(template="plotly_white", height=420), use_container_width=True)

# ---------------- Tab 3: Cancellations ----------------
with tab3:
    a, b = st.columns(2)
    st_cnt = cur["Booking Status"].value_counts().reset_index()
    st_cnt.columns = ["Status", "Rides"]
    a.plotly_chart(px.bar(st_cnt, x="Rides", y="Status", orientation="h", color="Status", text_auto=True,
                          title="Booking Outcomes", color_discrete_sequence=PALETTE)
                   .update_layout(showlegend=False, template="plotly_white", height=380), use_container_width=True)

    rate = cur.groupby("Vehicle Type")["Booking Status"].apply(lambda s: s.str.contains("Cancel", na=False).mean() * 100).reset_index()
    rate.columns = ["Vehicle Type", "Cancellation %"]
    b.plotly_chart(px.bar(rate.sort_values("Cancellation %"), x="Cancellation %", y="Vehicle Type", orientation="h",
                          text_auto=".1f", title="Cancellation Rate by Vehicle", color_discrete_sequence=[PALETTE[3]])
                   .update_layout(template="plotly_white", height=380), use_container_width=True)

    def reasons(col, title, color, container):
        if col not in cur.columns:
            return
        r = cur[cur[col].notna() & ~cur[col].isin(["Not Applicable", "null", ""])][col].value_counts().head(5)
        if r.empty:
            container.info("No data for the selected filters.")
            return
        r = r.sort_values().reset_index()
        r.columns = ["Reason", "Count"]
        container.plotly_chart(px.bar(r, x="Count", y="Reason", orientation="h", text_auto=True, title=title,
                                      color_discrete_sequence=[color])
                               .update_layout(template="plotly_white", height=380), use_container_width=True)

    c, d = st.columns(2)
    reasons("Reason for cancelling by Customer", "Top Customer Cancellation Reasons", PALETTE[2], c)
    reasons("Driver Cancellation Reason", "Top Driver Cancellation Reasons", PALETTE[4], d)

# ---------------- Tab 4: Data ----------------
with tab4:
    st.dataframe(cur.drop(columns=["Hour", "Weekday"]).head(200), use_container_width=True)
    st.download_button("⬇️ Download filtered data (CSV)", cur.to_csv(index=False).encode(), "filtered_rides.csv")
