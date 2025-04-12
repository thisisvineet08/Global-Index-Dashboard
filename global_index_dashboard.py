import streamlit as st
import seaborn as sns
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Index dictionary with Yahoo Finance tickers
index_dict = {
    "Nifty 50 (India)": "^NSEI",
    "Sensex (India)": "^BSESN",
    "S&P 500 (USA)": "^GSPC",
    "Dow Jones (USA)": "^DJI",
    "Nasdaq (USA)": "^IXIC",
    "FTSE 100 (UK)": "^FTSE",
    "DAX (Germany)": "^GDAXI",
    "CAC 40 (France)": "^FCHI",
    "Nikkei 225 (Japan)": "^N225",
    "Hang Seng (Hong Kong)": "^HSI"
}

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🌍 Global Indices Dashboard")

selected_indices = st.multiselect(
    "Choose indices to plot:",
    options=list(index_dict.keys()),
    default=["Nifty 50 (India)", "S&P 500 (USA)"]
)

start_date = st.date_input("Start date", pd.to_datetime("2015-01-01"))
end_date = st.date_input("End date", pd.to_datetime("today"))

if start_date >= end_date:
    st.warning("⚠️ Start date must be before end date.")
    st.stop()

st.subheader("📊 Price Trend Comparison")

# Data container
combined_df = pd.DataFrame()
summary_list = []

for index_name in selected_indices:
    ticker = index_dict[index_name]
    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        st.warning(f"No data found for {index_name}.")
        continue

    price_col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'

    df = df[[price_col]].copy()
    df.columns = [index_name]
    df.dropna(inplace=True)

    # Normalize to 100 for performance comparison
    df[index_name] = (df[index_name] / df[index_name].iloc[0]) * 100

    # Merge into combined_df
    if combined_df.empty:
        combined_df = df
    else:
        combined_df = combined_df.join(df, how='outer')

    # Metrics
    raw_df = yf.download(ticker, start=start_date, end=end_date)
    if price_col not in raw_df.columns or raw_df[price_col].dropna().empty:
        continue

    price_series = raw_df[price_col].dropna()

    try:
        all_time_high = float(price_series.max())
        all_time_low = float(price_series.min())
        return_over_period = float(((price_series.iloc[-1] - price_series.iloc[0]) / price_series.iloc[0]) * 100)
    except Exception:
        all_time_high = all_time_low = return_over_period = float('nan')

    summary_list.append({
        "Index": index_name,
        "All-time High": all_time_high,
        "All-time Low": all_time_low,
        "Return (%)": return_over_period
    })

# Plot all selected indices on one graph
if not combined_df.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    for col in combined_df.columns:
        ax.plot(combined_df.index, combined_df[col], label=col, linewidth=2)

    ax.set_title("Normalized Price Comparison (Base = 100)", fontsize=16)
    ax.set_ylabel("Normalized Index Value")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# Show Summary Table
if summary_list:
    st.subheader("📈 Summary Statistics")
    summary_df = pd.DataFrame(summary_list)
    st.dataframe(summary_df.set_index("Index").style.format({
        "All-time High": "{:.2f}",
        "All-time Low": "{:.2f}",
        "Return (%)": "{:.2f}"
    }))



#vineet is doing its work
import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import timedelta

# Index dictionary with Yahoo Finance tickers
index_dict = {
    "Nifty 50 (India)": "^NSEI",
    "Sensex (India)": "^BSESN",
    "S&P 500 (USA)": "^GSPC",
    "Dow Jones (USA)": "^DJI",
    "Nasdaq (USA)": "^IXIC",
    "FTSE 100 (UK)": "^FTSE",
    "DAX (Germany)": "^GDAXI",
    "CAC 40 (France)": "^FCHI",
    "Nikkei 225 (Japan)": "^N225",
    "Hang Seng (Hong Kong)": "^HSI"
}

# Streamlit UI setup


# Dark mode toggle
theme_option = st.sidebar.selectbox("Select Theme", ["Light", "Dark"])
if theme_option == "Dark":
    st.markdown("""
    <style>
    .main {background-color: #2c2f36; color: white;}
    .sidebar .sidebar-content {background-color: #2c2f36; color: white;}
    </style>
    """, unsafe_allow_html=True)

# Index selection
selected_indices = st.multiselect(
    "Choose indices to plot:",
    options=list(index_dict.keys()),
    default=["Nifty 50 (India)", "S&P 500 (USA)"]
)

# Date range input
start_date = st.date_input("Start date", pd.to_datetime("2015-01-01"))
end_date = st.date_input("End date", pd.to_datetime("today"))

if start_date >= end_date:
    st.warning("⚠️ Start date must be before end date.")
    st.stop()

st.subheader("📊 Price Trend Comparison")

# Data container for combined graph
combined_df = pd.DataFrame()
summary_list = []

# Download data and create DataFrames for selected indices
for index_name in selected_indices:
    ticker = index_dict[index_name]
    df = yf.download(ticker, start=start_date, end=end_date)

    if df.empty:
        st.warning(f"No data found for {index_name}.")
        continue

    price_col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'

    df = df[[price_col]].copy()
    df.columns = [index_name]
    df.dropna(inplace=True)

    # Normalize data for easy comparison
    df[index_name] = (df[index_name] / df[index_name].iloc[0]) * 100
    combined_df = combined_df.join(df, how='outer') if not combined_df.empty else df

    # Metrics calculations
    raw_df = yf.download(ticker, start=start_date, end=end_date)
    price_series = raw_df[price_col].dropna()

    try:
        all_time_high = float(price_series.max())
        all_time_low = float(price_series.min())
        return_over_period = float(((price_series.iloc[-1] - price_series.iloc[0]) / price_series.iloc[0]) * 100)
    except Exception:
        all_time_high = all_time_low = return_over_period = float('nan')

    summary_list.append({
        "Index": index_name,
        "All-time High": all_time_high,
        "All-time Low": all_time_low,
        "Return (%)": return_over_period
    })

# Plot all selected indices on one combined graph
if not combined_df.empty:
    fig, ax = plt.subplots(figsize=(12, 6))
    for col in combined_df.columns:
        ax.plot(combined_df.index, combined_df[col], label=col, linewidth=2)

    ax.set_title("Normalized Price Comparison (Base = 100)", fontsize=16)
    ax.set_ylabel("Normalized Index Value")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# Rolling Performance (1Y, 3Y, custom)
st.subheader("🔄 Rolling Performance")

rolling_period = st.selectbox("Select Rolling Period:", ["1 Year", "3 Year", "Custom"])
if rolling_period == "1 Year":
    window = 252  # Approximate number of trading days in a year
elif rolling_period == "3 Year":
    window = 756  # Approximate number of trading days in 3 years
else:
    custom_period = st.number_input("Enter number of days", min_value=1, max_value=1000, value=252)
    window = custom_period

# Rolling returns graph
fig, ax = plt.subplots(figsize=(12, 6))
for col in combined_df.columns:
    ax.plot(combined_df.index, combined_df[col].rolling(window=window).mean(), label=f"Rolling Avg ({window} days)", linestyle="--")
ax.set_title("Rolling Performance", fontsize=16)
ax.set_ylabel("Rolling Average Price")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# Return Comparison Bar Chart
st.subheader("📊 Return Comparison")

returns = [summary["Return (%)"] for summary in summary_list]
labels = [summary["Index"] for summary in summary_list]

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(labels, returns, color="skyblue")
ax.set_title("Return Comparison (Selected Period)", fontsize=16)
ax.set_ylabel("Return (%)")
ax.grid(True)
st.pyplot(fig)

# Volatility Heatmap (Standard Deviation)
st.subheader("📉 Volatility Heatmap (1Y Standard Deviation)")

returns_df = pd.DataFrame({index_name: yf.download(index_dict[index_name], start=start_date, end=end_date)['Adj Close'] for index_name in selected_indices})
returns_df = returns_df.pct_change().std() * np.sqrt(252)  # Annualized volatility

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(returns_df.to_frame().T, annot=True, cmap="coolwarm", cbar=True)
ax.set_title("Annualized Volatility (1Y)", fontsize=16)
st.pyplot(fig)

# Correlation Matrix
st.subheader("🔗 Correlation Matrix of Selected Indices")

corr_matrix = returns_df.corr()
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", cbar=True)
ax.set_title("Correlation Matrix", fontsize=16)
st.pyplot(fig)

# Export Data as CSV
st.subheader("📥 Export Data")
csv = pd.DataFrame(summary_list).to_csv(index=False)
st.download_button(label="Download Summary as CSV", data=csv, file_name="indices_summary.csv", mime="text/csv")

# AI Insight Mode
st.subheader("🧠 Insights Mode")

insight_button = st.button("Generate Insights")
if insight_button:
    insights = []
    for summary in summary_list:
        insights.append(f"{summary['Index']} had a return of {summary['Return (%)']:.2f}% over the selected period.")
    st.write("\n".join(insights))


