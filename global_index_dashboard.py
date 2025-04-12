import streamlit as st
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
