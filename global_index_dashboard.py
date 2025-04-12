import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Hide Streamlit warnings


# Global index tickers
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
st.title("🌍 Global Indices Dashboard")

selected_indices = st.multiselect(
    "Choose indices to plot:", 
    options=list(index_dict.keys()), 
    default=["Nifty 50 (India)"]
)

start_date = st.date_input("Start date", pd.to_datetime("2015-01-01"))
end_date = st.date_input("End date", pd.to_datetime("today"))

if start_date >= end_date:
    st.warning("⚠️ Start date must be before end date")
else:
    st.subheader("📊 Index Performance")

    for index_name in selected_indices:
        ticker = index_dict[index_name]
        df = yf.download(ticker, start=start_date, end=end_date)

        if df.empty:
            st.warning(f"No data found for {index_name}")
            continue

        # Check for 'Adj Close' fallback to 'Close'
        price_col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'

        if price_col not in df.columns:
            st.warning(f"{index_name} data does not contain 'Close' or 'Adj Close'")
            continue

        # Calculate Return
        df['Return (%)'] = ((df[price_col] - df[price_col].iloc[0]) / df[price_col].iloc[0]) * 100
        return_over_period = df['Return (%)'].iloc[-1]
        all_time_high = df[price_col].max()
        all_time_low = df[price_col].min()

        # Plotting
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(df.index, df[price_col], label=index_name, linewidth=2)
        ax.set_title(f"{index_name} | Return: {return_over_period:.2f}%", fontsize=14)
        ax.set_ylabel("Price", fontsize=12)
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        # Stats Display
        st.markdown(f"### 📈 {index_name} Summary")
        st.markdown(f"- **All-time High (in selected period)**: `{all_time_high:.2f}`")
        st.markdown(f"- **All-time Low (in selected period)**: `{all_time_low:.2f}`")
        st.markdown(f"- **Return from {start_date} to {end_date}**: `{return_over_period:.2f}%`")
        st.markdown("---")
