import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

# List of major indices with robust tickers
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

def fetch_data(start_date, end_date, selected_indices):
    """Fetch historical data with comprehensive error handling"""
    data = {}
    failures = 0
    
    for name in selected_indices:
        ticker = indices.get(name)
        if not ticker:
            st.warning(f"Ticker not found for {name}")
            continue
            
        try:
            df = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if df.empty:
                st.warning(f"No data for {name} in selected date range")
                failures += 1
                continue
                
            # Use Close if Adj Close not available
            price_series = df['Adj Close'] if 'Adj Close' in df.columns else df['Close']
            data[name] = price_series
            
        except Exception as e:
            st.error(f"Failed to fetch {name}: {str(e)}")
            failures += 1
    
    if failures == len(selected_indices):
        st.error("Failed to fetch data for all selected indices. Please try different dates or indices.")
        return None
        
    if not data:
        st.error("No valid data fetched. Please check your selections.")
        return None
        
    # Create DataFrame with proper date index
    try:
        combined = pd.DataFrame(data)
        return combined.dropna()
    except Exception as e:
        st.error(f"Error creating DataFrame: {str(e)}")
        return None

# Streamlit UI
st.title("📈 Global Indices Dashboard")

# Date input with validation
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime(2023, 1, 1))
with col2:
    end_date = st.date_input("End Date", datetime.today())

if start_date >= end_date:
    st.error("End date must be after start date")

# Index selection
selected_indices = st.multiselect(
    "Select Indices (2+ for correlation)",
    list(indices.keys()),
    default=["Nifty 50", "Sensex", "S&P 500"]
)

if st.button("Analyze", type="primary"):
    if not selected_indices:
        st.error("Please select at least one index")
    elif start_date >= end_date:
        st.error("Please fix date range")
    else:
        with st.spinner("Fetching data..."):
            data = fetch_data(start_date, end_date, selected_indices)
            
        if data is not None and not data.empty:
            # Plot performance
            st.subheader("📊 Normalized Performance (Base=100)")
            fig, ax = plt.subplots(figsize=(12, 6))
            for idx in data.columns:
                normalized = (data[idx] / data[idx].iloc[0]) * 100
                ax.plot(normalized, label=idx)
            ax.set_title("Indices Performance Comparison")
            ax.set_ylabel("Normalized Value")
            ax.legend()
            ax.grid()
            st.pyplot(fig)
            
            # Calculate returns
            st.subheader("💰 Returns Analysis")
            returns = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100
            st.dataframe(returns.round(2).rename("Return (%)").to_frame().style.background_gradient(cmap='RdYlGn'))
            
            # Correlation matrix
            if len(selected_indices) > 1:
                st.subheader("🔗 Correlation Matrix")
                corr = data.pct_change().corr()
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
                st.pyplot(fig)
