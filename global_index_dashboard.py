import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

# List of major indices
indices = {
    'Nifty 50': '^NSEI', 
    'Sensex': '^BSESN', 
    'S&P 500': '^GSPC', 
    'NASDAQ': '^IXIC', 
    'Dow Jones': '^DJI', 
    'FTSE 100': '^FTSE', 
    'DAX': '^GDAXI', 
    'Nikkei 225': '^N225', 
    'Hang Seng': '^HSI', 
    'Shanghai Composite': '000001.SS'
}

def fetch_data(start_date, end_date):
    """Fetch historical data with robust error handling"""
    data = {}
    for name, ticker in indices.items():
        try:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if not df.empty:
                if 'Adj Close' in df.columns:
                    data[name] = df['Adj Close']
                elif 'Close' in df.columns:
                    data[name] = df['Close']
                else:
                    st.warning(f"Skipping {name}: No 'Adj Close' or 'Close' column")
            else:
                st.warning(f"Skipping {name}: No data found for the date range")
        except Exception as e:
            st.error(f"Error fetching {name} ({ticker}): {str(e)}")
    
    if not data:
        st.error("No data fetched for any index. Check date range or tickers.")
        return pd.DataFrame()  # Return empty DataFrame to avoid ValueError
    
    # Align all series to a common index (union of all dates)
    return pd.DataFrame(data).dropna()

# Streamlit UI
st.title("Global Indices Dashboard")

# Date input
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime(2023, 1, 1))
with col2:
    end_date = st.date_input("End Date", datetime.today())

# Index selection
selected_indices = st.multiselect(
    "Select Indices", 
    list(indices.keys()), 
    default=["Nifty 50", "Sensex", "S&P 500"]
)

if st.button("Analyze"):
    if not selected_indices:
        st.error("Please select at least one index!")
    else:
        data = fetch_data(start_date, end_date)
        
        if data.empty:
            st.error("No data available for analysis. Adjust dates or indices.")
        else:
            # Plot performance
            st.subheader("Normalized Performance (Base=100)")
            fig, ax = plt.subplots(figsize=(12, 6))
            for idx in selected_indices:
                if idx in data.columns:
                    normalized = (data[idx] / data[idx].iloc[0]) * 100
                    ax.plot(normalized, label=idx)
            ax.set_title("Indices Performance")
            ax.legend()
            ax.grid()
            st.pyplot(fig)
            
            # Calculate returns
            st.subheader("Total Returns (%)")
            returns = {}
            for idx in selected_indices:
                if idx in data.columns:
                    returns[idx] = round(((data[idx].iloc[-1] - data[idx].iloc[0]) / data[idx].iloc[0]) * 100, 2)
            st.table(pd.Series(returns).rename("Return"))
            
            # Correlation heatmap (only if >1 index selected)
            if len(selected_indices) > 1:
                st.subheader("Correlation Matrix")
                corr = data[selected_indices].pct_change().corr()
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
                st.pyplot(fig)
            else:
                st.warning("Select at least 2 indices for correlation analysis.")
