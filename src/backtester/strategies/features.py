"""Compute features for ML-based stock selection."""

import pandas as pd
import numpy as np


def compute_features(prices):
    """Compute monthly features for each stock from a price DataFrame.
    
    prices: DataFrame of daily prices, one column per stock, indexed by date.
    
    Returns a long-format DataFrame with columns:
      - date: month-end date
      - ticker: stock ticker
      - mom_12m, reversal_1m, mom_12_1, vol_6m, mom_3m: the 5 features
    """
    # Resample to month-end prices
    monthly_prices = prices.resample("ME").last()
    
    # Computing daily returns once (we use them for volatility)
    daily_returns = prices.pct_change()
    monthly_vol = daily_returns.resample("ME").std() * np.sqrt(21)
    # Why * sqrt(21)? Annualizing daily vol to monthly vol — there are ~21 trading days/month
    
    # Computing each feature as a DataFrame (one row per month, one column per stock)
    mom_12m = monthly_prices.pct_change(12)
    reversal_1m = monthly_prices.pct_change(1)
    mom_12_1 = monthly_prices.shift(1).pct_change(11) #shifts every row down by 1 month. So January 2024's row now contains December 2023's prices.computes change over 11 months on this shifted data. So January 2024's value becomes (Dec 2023 price / Jan 2023 price) - 1
    vol_6m = monthly_vol.rolling(window=6).mean()
    mom_3m = monthly_prices.pct_change(3)
    
    # Stacking each feature into long format: (date, ticker, value)
    features = pd.DataFrame({
        "mom_12m": mom_12m.stack(),
        "reversal_1m": reversal_1m.stack(),
        "mom_12_1": mom_12_1.stack(),
        "vol_6m": vol_6m.stack(),
        "mom_3m": mom_3m.stack(),
    })
    
    # Reset index to get date and ticker as columns
    features.index.names = ["date", "ticker"]
    features = features.reset_index()
    
    # Drop rows where any feature is NaN (insufficient history)
    features = features.dropna()
    
    return features

#computing the target variable
def compute_target(prices, features):
    """Compute the binary target: did each stock beat median next month?
    
    prices: DataFrame of daily prices (used to compute next-month returns).
    features: the features DataFrame (used to align dates and tickers).
    
    Returns the features DataFrame with a new 'target' column.
    """
    # Monthly prices and the NEXT month's return for each stock
    monthly_prices = prices.resample("ME").last()
    next_month_returns = monthly_prices.pct_change(1).shift(-1)
    
    # Convert to long format matching the features structure
    next_month_long = next_month_returns.stack().reset_index()
    next_month_long.columns = ["date", "ticker", "next_month_return"]
    
    # Merge with features
    df = features.merge(next_month_long, on=["date", "ticker"], how="left")
    
    # For each date, compute the median next-month return across all stocks
    df["median_return"] = df.groupby("date")["next_month_return"].transform("median")
    
    # Target: 1 if beat median, 0 otherwise
    df["target"] = (df["next_month_return"] > df["median_return"]).astype(int)
    
    # Drop the most recent month — no "next month" to predict from
    df = df.dropna(subset=["next_month_return"])
    
    return df

