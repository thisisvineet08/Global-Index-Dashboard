import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from datetime import datetime

# -------- Settings --------
start_date = "2020-01-01"
end_date = "2024-12-31"

# -------- 10 Major Indices with Yahoo Tickers --------
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

# -------- Download Data --------
data = yf.download(list(index_dict.values()), start=start_date, end=end_date)['Adj Close']
data.columns = index_dict.keys()

# -------- Normalize and Plot --------
normalized = data / data.iloc[0] * 100  # Base 100
plt.figure(figsize=(14, 8))
for column in normalized.columns:
    plt.plot(normalized[column], label=column)
plt.title('Index Performance (Normalized)')
plt.xlabel('Date')
plt.ylabel('Normalized Price (Base 100)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# -------- Calculate Returns --------
returns = (data.iloc[-1] / data.iloc[0] - 1) * 100
returns = returns.sort_values(ascending=False)
print("Returns over selected period:")
print(returns.round(2))

# Plot Returns
fig = go.Figure(data=[go.Bar(x=returns.index, y=returns.values, marker_color='indigo')])
fig.update_layout(title="Returns (%) from {} to {}".format(start_date, end_date),
                  yaxis_title="Return (%)", xaxis_title="Index")
fig.show()

# -------- Correlation Matrix --------
daily_returns = data.pct_change().dropna()
correlation = daily_returns.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix of Daily Returns")
plt.tight_layout()
plt.show()
