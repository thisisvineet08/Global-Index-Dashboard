import pandas as pd
import streamlit as st
import yfinance as yf
import datetime
import matplotlib.pyplot as plt


st.set_page_config(page_title="Global Index Dashboard", layout="wide")

st.title("📈 Global Stock Index Dashboard")
st.markdown("Compare the performance of major global indices over different time periods.")

# Index list
indices = {
    "S&P 500 (US)": "^GSPC",
    "Nasdaq (US)": "^IXIC",
    "Dow Jones (US)": "^DJI",
    "FTSE 100 (UK)": "^FTSE",
    "DAX (Germany)": "^GDAXI",
    "CAC 40 (France)": "^FCHI",
    "Nikkei 225 (Japan)": "^N225",
    "Hang Seng (HK)": "^HSI",
    "Shanghai Composite (China)": "000001.SS",
    "Nifty 50 (India)": "^NSEI",
    "Sensex (India)": "^BSESN"
}

selected_indices = st.multiselect(
    "Select indices to compare:",
    options=list(indices.keys()),
    default=["S&P 500 (US)", "Nifty 50 (India)", "Sensex (India)"]
)

range_option = st.selectbox(
    "Select time range:",
    options=["1 Year", "5 Years", "10 Years", "Max"]
)

end = datetime.date.today()

if range_option == "1 Year":
    start = end - datetime.timedelta(days=365)
elif range_option == "5 Years":
    start = end - datetime.timedelta(days=365 * 5)
elif range_option == "10 Years":
    start = end - datetime.timedelta(days=365 * 10)
else:
    start = datetime.date(2000, 1, 1)

if selected_indices:
    fig, ax = plt.subplots(figsize=(14, 8))
    for index in selected_indices:
        ticker = indices[index]
        try:
            data = yf.download(ticker, start=start, end=end, progress=False, timeout=5)
            if not data.empty:
                normalized = data['Close'] / data['Close'].iloc[0]
                ax.plot(normalized, label=index)
            else:
                st.warning(f"No data for {index}")
        except Exception as e:
            st.error(f"Failed to load {index}: {str(e)}")
    ax.set_title(f"Normalized Index Performance ({range_option})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Price")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
else:
    st.info("Please select at least one index.")

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime



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

# Fetch data and calculate returns
all_data = pd.DataFrame()
returns = {}
highs = {}
lows = {}

if selected_indices:
    for name in selected_indices:
        ticker = index_tickers[name]
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if 'Adj Close' in data.columns:
                data = data['Adj Close']
                all_data[name] = data
                returns[name] = ((data[-1] - data[0]) / data[0]) * 100
                highs[name] = data.max()
                lows[name] = data.min()
        except Exception as e:
            st.warning(f"Could not load data for {name}: {e}")

# Display charts and stats
if not all_data.empty:
    st.subheader("📈 Historical Prices")
    st.line_chart(all_data)

    st.subheader("📊 Index Performance Summary")
    stats_df = pd.DataFrame({
        "Return (%)": returns,
        "All-Time High in Period": highs,
        "All-Time Low in Period": lows
    })
    st.dataframe(stats_df.style.format("{:.2f}"))
else:
    st.info("Please select at least one valid index and date range.")


