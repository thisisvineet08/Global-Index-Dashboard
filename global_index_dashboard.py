import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# List of major indices (Yahoo Finance tickers)
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
    """Fetch historical data for all indices"""
    data = {}
    for name, ticker in indices.items():
        df = yf.download(ticker, start=start_date, end=end_date)['Adj Close']
        data[name] = df
    return pd.DataFrame(data).dropna()

def plot_indices(data, selected_indices):
    """Plot selected indices (normalized to 100 at start)"""
    plt.figure(figsize=(14, 7))
    for idx in selected_indices:
        if idx in data.columns:
            normalized = (data[idx] / data[idx].iloc[0]) * 100
            plt.plot(normalized, label=idx)
    plt.title('Indices Performance (Normalized to 100)')
    plt.xlabel('Date')
    plt.ylabel('Normalized Price')
    plt.legend()
    plt.grid()
    plt.show()

def calculate_returns(data, selected_indices):
    """Calculate and print returns for selected indices"""
    returns = {}
    for idx in selected_indices:
        if idx in data.columns:
            total_return = ((data[idx].iloc[-1] - data[idx].iloc[0]) / data[idx].iloc[0]) * 100
            returns[idx] = round(total_return, 2)
    return pd.Series(returns).rename('Total Return (%)')

def plot_correlation(data, selected_indices):
    """Plot correlation heatmap for selected indices"""
    corr = data[selected_indices].pct_change().corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Matrix of Selected Indices')
    plt.show()

# Example Usage
if __name__ == "__main__":
    # User inputs (customize these)
    start_date = '2023-01-01'
    end_date = '2024-01-01'
    selected_indices = ['Nifty 50', 'Sensex', 'S&P 500', 'NASDAQ', 'FTSE 100']
    
    # Fetch and process data
    data = fetch_data(start_date, end_date)
    
    # Plot performance
    plot_indices(data, selected_indices)
    
    # Calculate returns
    returns = calculate_returns(data, selected_indices)
    print("\nTotal Returns (%):")
    print(returns.to_string())
    
    # Plot correlation
    plot_correlation(data, selected_indices)
