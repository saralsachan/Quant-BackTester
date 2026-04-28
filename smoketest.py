import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Download Reliance Industries data
ticker = "RELIANCE.NS"  # .NS suffix for NSE-listed stocks
data = yf.download(ticker, start="2020-01-01", end="2025-12-31", auto_adjust=True)

print(data.head())
print(f"\nShape: {data.shape}")
print(f"Date range: {data.index.min()} to {data.index.max()}")

# Plot it
data["Close"].plot(figsize=(12, 6), title=f"{ticker} Adjusted Close")
plt.show()

# Compute daily returns
returns = data["Close"].pct_change().dropna()
print(f"\nMean daily return: {returns.mean():.4%}")
print(f"Annualized volatility: {returns.std() * np.sqrt(252):.2%}")