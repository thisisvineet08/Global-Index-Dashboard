import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st
import numpy as np

# List of Indian indices with their Yahoo Finance tickers
indices = {
    'NIFTY 50': '^NSEI',
    'SENSEX': '^BSESN',
    'NIFTY BANK': '^NSEBANK',
    'NIFTY MIDCAP 50': '^NSEMDCP50',
    'NIFTY SMALLCAP 100': '^NSESMLCAP100',
    'NIFTY IT': '^NSEIT',
    'NIFTY PHARMA': '^NSEPHARMA',
    'NIFTY AUTO': '^NSEAUTO',
    'NIFTY FMCG': '^NSEFMCG',
    'NIFTY METAL': '^NSEMETAL'
}

@st.cache_data
def fetch_data(index_ticker, start_date, end_date):
    """Fetch historical data for a given index."""
    try:
        data = yf.download(index_ticker, start=start_date, end=end_date, progress=False)
        if data.empty or 'Close' not in data.columns:
            st.warning(f"No data available for {index_ticker} in the selected date range.")
            return None
        # Ensure 'Close' contains numeric data
        if not pd.api.types.is_numeric_dtype(data['Close']):
            st.warning(f"Invalid data format for {index_ticker} 'Close' column.")
            return None
        return data
    except Exception as e:
        st.error(f"Error fetching data for {index_ticker}: {e}")
        return None

def calculate_metrics(data, index_name):
    """Calculate returns, ATH, and ATL for the data."""
    if data is None or data.empty or 'Close' not in data.columns:
        return None, None, None
    
    try:
        # Extract start and end prices
        start_price = data['Close'].iloc[0]
        end_price = data['Close'].iloc[-1]
        
        # Validate prices
        if not (isinstance(start_price, (int, float)) and isinstance(end_price, (int, float))):
            st.warning(f"Non-numeric price data for {index_name}.")
            return None, None, None
        if not (pd.notna(start_price) and pd.notna(end_price)):
            st.warning(f"Missing price data for {index_name}.")
            return None, None, None
        
        # Calculate returns
        returns = None
        if start_price != 0:
            returns = ((end_price - start_price) / start_price) * 100
        
        # Calculate ATH and ATL
        ath = data['Close'].max()
        atl = data['Close'].min()
        
        # Validate ATH and ATL
        if not (pd.notna(ath) and pd.notna(atl)):
            st.warning(f"Invalid ATH/ATL for {index_name}.")
            return returns, None, None
        
        return returns, ath, atl
    except Exception as e:
        st.error(f"Error calculating metrics for {index_name}: {e}")
        return None, None, None

def plot_indices(selected_indices, start_date, end_date):
    """Plot the selected indices and display metrics."""
    fig, ax = plt.subplots(figsize=(12, 6))
    metrics = {}
    
    for index_name in selected_indices:
        ticker = indices.get(index_name)
        if not ticker:
            st.warning(f"Invalid index: {index_name}")
            continue
        
        data = fetch_data(ticker, start_date, end_date)
        
        if data is not None:
            # Normalize data to start at 100 for comparison
            start_price = data['Close'].iloc[0]
            if pd.notna(start_price) and start_price != 0:
                normalized_data = (data['Close'] / start_price) * 100
                ax.plot(normalized_data.index, normalized_data, label=index_name)
            
            # Calculate metrics
            returns, ath, atl = calculate_metrics(data, index_name)
            metrics[index_name] = {
                'Returns (%)': round(returns, 2) if returns is not None else 'N/A',
                'ATH': round(ath, 2) if ath is not None else 'N/A',
                'ATL': round(atl, 2) if atl is not None else 'N/A'
            }
    
    # Plot customization
    ax.set_title(f"Normalized Index Performance ({start_date} to {end_date})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Value (Base = 100)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    plt.close(fig)
    
    # Display metrics
    if metrics:
        st.subheader("Performance Metrics")
        metrics_df = pd.DataFrame(metrics).T
        st.dataframe(metrics_df)
    else:
        st.warning("No valid data to display metrics.")

def main():
    """Main function to run the Streamlit app."""
    st.title("Indian Indices Performance Dashboard")
    
    # Date input
    st.subheader("Select Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime(2023, 1, 1))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now().date())
    
    # Index selection
    st.subheader("Select Indices")
    selected_indices = st.multiselect(
        "Choose indices to compare",
        options=list(indices.keys()),
        default=['NIFTY 50', 'SENSEX']
    )
    
    if st.button("Generate Plot"):
        if not selected_indices:
            st.warning("Please select at least one index.")
        elif start_date >= end_date:
            st.warning("Start date must be before end date.")
        else:
            plot_indices(selected_indices, start_date, end_date)

if __name__ == "__main__":
    main()
