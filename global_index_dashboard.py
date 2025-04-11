
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
