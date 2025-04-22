import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

# -------- Streamlit UI --------
st.set_page_config(page_title="Global Index Dashboard", layout="wide")
st.title("🌐 Global Index Dashboard")
st.markdown("Analyze major stock indices (Nifty 50, Sensex, S&P 500, etc.) over a custom date range.")

# Date inputs
start_date = st.date_input("Start Date", datetime(2020, 1, 1))
end_date = st.date_input("End Date", datetime.today())

# -------- Index Dictionary --------
index_dict = {
    'S&P 500': '^GSPC',
    'Dow Jones': '^DJI',
    'Nasdaq': '^IXIC',
    'FTSE 100': '^FTSE',
    'Nikkei 225': '^N225',
    'Hang Seng': '^HSI',
    'DAX': '^GDAXI',
    'CAC 40': '^FCHI',
    'Nifty 50': '^NSEI',
    'Sensex': '^BSESN'
}

# -------- Index Selection --------
selected_indices = st.multiselect(
    "Select indices to analyze:",
    options=list(index_dict.keys()),
    default=['Nifty 50', 'Sensex', 'S&P 500', 'Dow Jones']
)

if not selected_indices:
    st.warning("Please select at least one index to proceed.")
    st.stop()

selected_tickers = {name: index_dict[name] for name in selected_indices}

# -------- Download Data --------
st.subheader("📥 Downloading Data...")

try:
    raw_data = yf.download(
        tickers=list(selected_tickers.values()),
        start=start_date,
        end=end_date,
        group_by='ticker',
        auto_adjust=True,
        progress=False
    )

    price_data = pd.DataFrame()

    for name, ticker in selected_tickers.items():
        if isinstance(raw_data.columns, pd.MultiIndex):
            if ticker in raw_data.columns.levels[0]:
                price_data[name] = raw_data[ticker]['Close']
        else:
            price_data[name] = raw_data['Close']

except Exception as e:
    st.error(f"Error downloading data: {e}")
    st.stop()

price_data.dropna(axis=1, how='all', inplace=True)

# -------- Plot Normalized Performance --------
st.subheader("📊 Normalized Index Performance (Base 100)")

normalized = price_data / price_data.iloc[0] * 100

fig, ax = plt.subplots(figsize=(14, 6))
normalized.plot(ax=ax)
ax.set_title("Index Performance (Normalized to 100)")
ax.set_xlabel("Date")
ax.set_ylabel("Normalized Price")
ax.grid(True)
st.pyplot(fig)

# -------- Returns Calculation --------
st.subheader("📈 Total Returns (%)")

returns = (price_data.iloc[-1] / price_data.iloc[0] - 1) * 100
returns = returns.sort_values(ascending=False)
st.dataframe(returns.round(2).to_frame(name="Return (%)"))

# Bar plot of returns
fig2, ax2 = plt.subplots()
returns.plot(kind='bar', ax=ax2, color='skyblue')
ax2.set_title(f"Returns (%) from {start_date} to {end_date}")
ax2.set_ylabel("Return (%)")
st.pyplot(fig2)

# -------- Correlation Matrix --------
st.subheader("🔗 Correlation of Daily Returns")

daily_returns = price_data.pct_change().dropna()
correlation = daily_returns.corr()

fig3, ax3 = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f", ax=ax3)
ax3.set_title("Correlation Matrix of Daily Returns")
st.pyplot(fig3)
