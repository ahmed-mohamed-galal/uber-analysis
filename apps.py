import streamlit as st
st.set_page_config(page_title="Ride Analytics Dashboard", layout="wide")
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    # Tell pandas to treat this specific column as dates right from the start
    df = pd.read_csv(
        'C:/Users/ahmed/Downloads/ncr_ride_bookingccccc.csv', 
        parse_dates=['Ride Start Datetime']
    )
    return df

df = load_data()

st.title("🚖 NCR Ride Bookings: Interactive Visual Analysis")
st.markdown("Explore trends, pricing, and cancellation patterns through interactive filtering.")

# --- Sidebar Filters ---
st.sidebar.header("Dashboard Filters")
vehicle_types = st.sidebar.multiselect("Select Vehicle Type", options=df['Vehicle Type'].unique(), default=df['Vehicle Type'].unique())
booking_status = st.sidebar.multiselect("Select Booking Status", options=df['Booking Status'].unique(), default=df['Booking Status'].unique())

# Apply Filters
mask = (df['Vehicle Type'].isin(vehicle_types)) & (df['Booking Status'].isin(booking_status))
filtered_df = df[mask]

# --- Key Metrics ---
m1, m2, m3 = st.columns(3)
m1.metric("Total Selected Rides", len(filtered_df))
m2.metric("Avg. Booking Value", f"${filtered_df['Booking Value'].mean():.2f}")
m3.metric("Avg. Distance", f"{filtered_df['Ride Distance'].mean():.2f} km")

# --- Visualizations ---
st.subheader("📈 Ride Volume Over Time")
daily_vol = filtered_df.resample('D', on='Ride Start Datetime').size()
fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(daily_vol.index, daily_vol.values, color='#2c7fb8', linewidth=2)
ax1.set_title("Daily Booking Counts")
st.pyplot(fig1)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Booking Status Distribution")
    fig2, ax2 = plt.subplots()
    status_data = filtered_df['Booking Status'].value_counts()
    sns.barplot(x=status_data.values, y=status_data.index, hue=status_data.index, palette='viridis', ax=ax2, legend=False)
    st.pyplot(fig2)

with col2:
    st.subheader("💰 Value vs Distance Correlation")
    fig3, ax3 = plt.subplots()
    # Sample for performance if dataset is huge
    sample_df = filtered_df.sample(min(len(filtered_df), 1000))
    sns.scatterplot(data=sample_df, x='Ride Distance', y='Booking Value', hue='Vehicle Type', alpha=0.6, ax=ax3)
    st.pyplot(fig3)

st.subheader("🚫 Cancellation Deep Dive")
c1, c2 = st.columns(2)
with c1:
    st.write("**Customer Cancellation Reasons**")
    cust_reasons = filtered_df[filtered_df['Reason for cancelling by Customer'] != 'Not Applicable']
    if not cust_reasons.empty:
        fig4, ax4 = plt.subplots()
        sns.countplot(data=cust_reasons, y='Reason for cancelling by Customer', order=cust_reasons['Reason for cancelling by Customer'].value_counts().index[:5], palette='magma', ax=ax4)
        st.pyplot(fig4)
    else:
        st.info("No customer cancellations in filtered data.")

with c2:
    st.write("**Driver Cancellation Reasons**")
    driv_reasons = filtered_df[filtered_df['Driver Cancellation Reason'] != 'Not Applicable']
    if not driv_reasons.empty:
        fig5, ax5 = plt.subplots()
        sns.countplot(data=driv_reasons, y='Driver Cancellation Reason', order=driv_reasons['Driver Cancellation Reason'].value_counts().index[:5], palette='flare', ax=ax5)
        st.pyplot(fig5)
    else:
        st.info("No driver cancellations in filtered data.")

st.markdown("--- ")
st.write("**Raw Data Preview (Filtered)**")
st.dataframe(filtered_df.head(50))
