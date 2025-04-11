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
    
start_date = st.sidebar.date_input("Start Date", datetime.date(1995, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

# ---------------------
# 📊 Show Returns & High/Low Table
# ---------------------
all_data = pd.DataFrame()
if not all_data.empty:
    result_data = []

    for index in all_data.columns:
        df = all_data[index].dropna()

        if len(df) == 0:
            continue

        initial_value = df.iloc[0]
        final_value = df.iloc[-1]
        returns = ((final_value - initial_value) / initial_value) * 100

        highest = df.max()
        highest_date = df.idxmax().strftime('%Y-%m-%d')

        lowest = df.min()
        lowest_date = df.idxmin().strftime('%Y-%m-%d')

        result_data.append({
            "Index": index,
            "Initial Value": round(initial_value, 2),
            "Final Value": round(final_value, 2),
            "Return (%)": round(returns, 2),
            "All-Time High": round(highest, 2),
            "High Date": highest_date,
            "All-Time Low": round(lowest, 2),
            "Low Date": lowest_date
        })

    result_df = pd.DataFrame(result_data)
    st.subheader("📋 Index Performance Summary")
    st.dataframe(result_df)

import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# ------------------------
# 🌍 Global Index Options
# ------------------------
index_dict = {
    "S&P 500 (USA)": "^GSPC",
    "NASDAQ (USA)": "^IXIC",
    "Dow Jones (USA)": "^DJI",
    "FTSE 100 (UK)": "^FTSE",
    "DAX (Germany)": "^GDAXI",
    "CAC 40 (France)": "^FCHI",
    "Nikkei 225 (Japan)": "^N225",
    "Hang Seng (Hong Kong)": "^HSI",
    "Shanghai Composite (China)": "000001.SS",
    "ASX 200 (Australia)": "^AXJO",
    "Nifty 50 (India)": "^NSEI",
    "Sensex (India)": "^BSESN"
}

# ------------------------
# 🧭 Page Setup
# ------------------------
st.set_page_config(page_title="Global Index Dashboard", layout="wide")
st.title("🌍 Global Index Dashboard")

# ------------------------
# 📅 Date and Index Selection
# ------------------------
st.subheader("🔧 Customize View")

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Start Date", datetime.date(2015, 1, 1))
with col2:
    end_date = st.date_input("End Date", datetime.date.today())

selected_labels = st.multiselect(
    "Select Indexes to Plot",
    options=list(index_dict.keys()),
    default=["S&P 500 (USA)", "Nifty 50 (India)"]
)

selected_indexes = [index_dict[label] for label in selected_labels]

# ------------------------
# 📥 Fetch Data
# ------------------------
all_data = pd.DataFrame()

if selected_indexes:
    try:
        raw_data = yf.download(selected_indexes, start=start_date, end=end_date)
        if 'Adj Close' in raw_data:
            all_data = raw_data['Adj Close']
    except Exception as e:
        st.error(f"⚠️ Error downloading data: {e}")

# ------------------------
# 📊 Show Output
# ------------------------
if not all_data.empty:
    st.subheader("📈 Index Trend")
    st.line_chart(all_data)

    st.subheader("🔁 Returns and High/Low Info")

    # Calculate return, high, low
    returns = ((all_data.iloc[-1] - all_data.iloc[0]) / all_data.iloc[0]) * 100
    highs = all_data.max()
    lows = all_data.min()

    summary_df = pd.DataFrame({
        "Return (%)": returns.round(2),
        "All-Time High": highs.round(2),
        "All-Time Low": lows.round(2)
    })

    st.dataframe(summary_df)

else:
    st.warning("👆 Please select at least one index and a valid date range.")

