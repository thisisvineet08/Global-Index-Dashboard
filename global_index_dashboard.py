import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st

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

def fetch_data(index_ticker, start_date, end_date):
    """Fetch historical data for a given index."""
    try:
        data = yf.download(index_ticker, start=start_date, end=end_date, progress=False)
        if data.empty:
            return None
        return data
    except Exception as e:
        st.error(f"Error fetching data for {index_ticker}: {e}")
        return None

def calculate_metrics(data, index_name):
    """Calculate returns, ATH, and ATL for the data."""
    if data is None or data.empty:
        return None, None, None
    
    # Calculate returns
    start_price = data['Close'].iloc[0]
    end_price = data['Close'].iloc[-1]
    returns = ((end_price - start_price) / start_price) * 100
    
    # Calculate ATH and ATL
    ath = data['Close'].max()
    atl = data['Close'].min()
    
    return returns, ath, atl

def plot_indices(selected_indices, start_date, end_date):
    """Plot the selected indices and display metrics."""
    plt.figure(figsize=(12, 6))
    
    metrics = {}
    
    for index_name in selected_indices:
        ticker = indices[index_name]
        data = fetch_data(ticker, start_date, end_date)
        
        if data is not None:
            # Normalize data to start at 100 for comparison
            normalized_data = (data['Close'] / data['Close'].iloc[0]) * 100
            plt.plot(normalized_data.index, normalized_data, label=index_name)
            
            # Calculate metrics
            returns, ath, atl = calculate_metrics(data, index_name)
            metrics[index_name] = {
                'Returns (%)': round(returns, 2) if returns else 'N/A',
                'ATH': round(ath, 2) if ath else 'N/A',
                'ATL': round(atl, 2) if atl else 'N/A'
            }
    
    # Plot customization
    plt.title(f"Normalized Index Performance ({start_date} to {end_date})")
    plt.xlabel("Date")
    plt.ylabel("Normalized Value (Base = 100)")
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)
    
    # Display metrics
    st.subheader("Performance Metrics")
    metrics_df = pd.DataFrame(metrics).T
    st.dataframe(metrics_df)

def main():
    """Main function to run the Streamlit app."""
    st.title("Indian Indices Performance Dashboard")
    
    # Date input
    st.subheader("Select Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime(2023, 1, 1))
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
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
