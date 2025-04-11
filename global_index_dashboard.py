import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

# ✅ Set Streamlit page configuration first
st.set_page_config(page_title="Global Index Dashboard", layout="wide")

# Define index tickers and names
index_tickers = {
    "S&P 500": "^GSPC",
    "Dow Jones": "^DJI",
    "Nasdaq": "^IXIC",
    "FTSE 100": "^FTSE",
    "Nikkei 225": "^N225",
    "Hang Seng": "^HSI",
    "DAX": "^GDAXI",
    "CAC 40": "^FCHI",
    "Nifty 50": "^NSEI",
    "Sensex": "^BSESN"
}

# Main title
st.title("🌍 Global Index Dashboard")
st.markdown("Analyze historical returns of global market indices.")

# Date range selection on main page
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Select Start Date", datetime.date.today() - datetime.timedelta(days=3650))
with col2:
    end_date = st.date_input("Select End Date", datetime.date.today())

# Select indices to visualize
selected_indices = st.multiselect("Select Indices to Compare", list(index_tickers.keys()), default=list(index_tickers.keys()))

# Ensure valid selections
if not selected_indices:
    st.warning("Please select at least one index.")
elif start_date >= end_date:
    st.warning("Please ensure the start date is before the end date.")
else:
    # Fetch data and calculate returns
    all_data = pd.DataFrame()
    returns = {}
    highs = {}
    lows = {}

    for name in selected_indices:
        ticker = index_tickers[name]
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if data.empty:
                st.warning(f"No data downloaded for {name}. Ticker: {ticker}")
            else:
                price_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
                series = data[price_col].dropna()
                if series.empty:
                    st.warning(f"{price_col} column for {name} is empty after dropping NaNs.")
                elif len(series) < 2:
                    st.warning(f"Not enough data points for {name} to calculate return.")
                else:
                    all_data[name] = series
                    returns[name] = round(((series.iloc[-1] - series.iloc[0]) / series.iloc[0]) * 100, 2)
                    highs[name] = round(series.max(), 2)
                    lows[name] = round(series.min(), 2)
                    st.success(f"Fetched and processed data for {name}")
        except Exception as e:
            st.warning(f"Could not load data for {name}: {e}")

    # Display charts and stats if at least one index has valid data
    if all_data.shape[1] > 0:
        st.subheader("📈 Historical Prices")
        st.line_chart(all_data.ffill().bfill())

        if returns:
            st.subheader("📊 Index Performance Summary")

            # Replace any None values with np.nan for safety
            returns = {k: v if isinstance(v, (float, int)) else np.nan for k, v in returns.items()}
            highs = {k: v if isinstance(v, (float, int)) else np.nan for k, v in highs.items()}
            lows = {k: v if isinstance(v, (float, int)) else np.nan for k, v in lows.items()}

            stats_df = pd.DataFrame({
                "Return (%)": pd.Series(returns),
                "All-Time High in Period": pd.Series(highs),
                "All-Time Low in Period": pd.Series(lows)
            })

            st.dataframe(
                stats_df.style.format({
                    "Return (%)": "{:.2f}",
                    "All-Time High in Period": "{:.2f}",
                    "All-Time Low in Period": "{:.2f}"
                }, na_rep="NA")
            )
        else:
            st.info("No performance summary to display. All selected indices returned empty or invalid data.")
    else:
        st.info("No valid data retrieved for the selected indices and date range.")
