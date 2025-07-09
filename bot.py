import yfinance as yf
data = yf.download("AAPL", start="2022-01-01", end="2023-12-31")
data.head()
import matplotlib.pyplot as plt
import seaborn as sns

data['Close'].plot(title='Closing Price Over Time')
plt.xlabel('Date')
plt.ylabel('Price')
plt.grid(True)
plt.show()
# Create SMAs
data['SMA20'] = data['Close'].rolling(window=20).mean()
data['SMA50'] = data['Close'].rolling(window=50).mean()

# Plot
plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Close Price')
plt.plot(data['SMA20'], label='20-Day SMA')
plt.plot(data['SMA50'], label='50-Day SMA')
plt.legend()
plt.title("Trading Strategy: SMA Crossover")
plt.show()
# Signal logic
data['Signal'] = 0
data['Signal'][data['SMA20'] > data['SMA50']] = 1  # Buy
data['Signal'][data['SMA20'] < data['SMA50']] = -1  # Sell

# Buy/Sell dates
data['Position'] = data['Signal'].diff()
buy = data[data['Position'] == 1]
sell = data[data['Position'] == -1]

plt.figure(figsize=(14, 7))
plt.plot(data['Close'], label='Close Price', alpha=0.5)
plt.plot(data['SMA20'], label='SMA20', alpha=0.75)
plt.plot(data['SMA50'], label='SMA50', alpha=0.75)
plt.scatter(buy.index, buy['Close'], label='Buy Signal', marker='^', color='green', s=100)
plt.scatter(sell.index, sell['Close'], label='Sell Signal', marker='v', color='red', s=100)
plt.title('Buy & Sell Signals')
plt.legend()
plt.grid(True)
plt.show()
data['Returns'] = data['Close'].pct_change()
data['Strategy_Returns'] = data['Returns'] * data['Signal'].shift(1)
cumulative_returns = (1 + data['Strategy_Returns']).cumprod()
cumulative_returns.plot(title='Cumulative Strategy Returns', figsize=(10,5))
import streamlit as st
st.title("Simple Trading Bot using SMA Strategy")
st.line_chart(data[['Close', 'SMA20', 'SMA50']])
