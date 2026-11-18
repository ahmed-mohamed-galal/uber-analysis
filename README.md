# 🚖 Uber Data Analysis

Exploratory analysis and an interactive dashboard of Uber ride bookings in the National Capital Region (NCR). The project covers data cleaning, exploration, and visualization in a Jupyter notebook, plus a Streamlit app for exploring the data interactively.

## 📁 Repository Structure

```
uber-analysis/
├── apps.py                      # Streamlit dashboard
├── uber.ipynb                   # Data cleaning & exploratory analysis notebook
├── ncr_ride_bookingccccc.csv    # NCR ride bookings dataset
├── requirements.txt             # Python dependencies
└── README.md
```

## 🎯 Project Goals

- Clean and prepare the ride bookings data for analysis
- Explore booking patterns (status, time, vehicle type, locations, payment methods)
- Understand cancellations and completed rides
- Present insights through interactive charts

## 🛠️ Tech Stack

- **Python**
- **Pandas / NumPy** — data cleaning and manipulation
- **Matplotlib / Seaborn** — static visualizations
- **Plotly** — interactive charts
- **Streamlit** — web dashboard
- **Jupyter Notebook** — analysis workflow

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ahmed-mohamed-galal/uber-analysis.git
cd uber-analysis
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the notebook

```bash
jupyter notebook uber.ipynb
```

### 5. Launch the dashboard

```bash
streamlit run apps.py
```

The app will open in your browser at `http://localhost:8501`.

## 📊 Dataset

`ncr_ride_bookingccccc.csv` contains Uber ride booking records for the NCR region. Typical fields include booking date/time, booking status, vehicle type, pickup and drop locations, payment method, and ride-related metrics.

> Make sure the CSV file stays in the same folder as `apps.py` so the app can load it.

## 🔍 Analysis Overview

The notebook walks through:

1. **Data loading & inspection** — shape, types, missing values
2. **Data cleaning** — handling nulls, duplicates, and formatting
3. **Exploratory analysis** — distributions and trends across key columns
4. **Visualization** — charts highlighting booking behavior and cancellations
5. **Insights** — key takeaways from the data

## 📸 Screenshots

_Add screenshots of the dashboard here._

```markdown
![Dashboard](images/dashboard.png)
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## 📄 License

This project is open source. Add a license of your choice (e.g., MIT) in a `LICENSE` file.

## 👤 Author

**Ahmed Mohamed Galal**
GitHub: [@ahmed-mohamed-galal](https://github.com/ahmed-mohamed-galal)
