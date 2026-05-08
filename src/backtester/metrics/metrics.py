"""Functions for computing performance metrics from price data."""

import numpy as np
import pandas as pd


def daily_returns(prices):
    """Convert a price series (or DataFrame) into daily returns.
    
    prices: a pandas Series or DataFrame of prices, indexed by date.
    
    Returns the same shape, but with daily percent changes.
    The first row will be NaN (no previous day to compare to).
    """
    return prices.pct_change()



"""Computing the total returns over a period of time"""
def total_returns(returns):
    """returns: pandas series contianing returns like 0.1, 0.05, 0.23 etc
    overall return does not add ,it compounds, use formula (1+r1)*(1+r2)*....-1"""
    
    return (1 + returns.dropna()).prod() - 1 #prod() multipies all values, drop NaN values


def annualized_returns_CAGR(returns, periods_per_year = 252):
    """Compute the annualized (per-year) return.
    
    returns: pandas Series of daily returns
    periods_per_year: number of return periods in a year (252 for daily data)
    
    Returns a single number — the average yearly return, compounded known as 
    CAGR(Compounded annual growth rate)."""
    
    cleaned = returns.dropna()
    total_growth = (1 + cleaned).prod()
    num_years = len(cleaned) / periods_per_year
    
    return total_growth**(1/num_years) - 1
    
    
def annualized_volatility(returns, periods_per_year = 252):
     """Compute the annualized standard deviation of returns.
    
    returns: a pandas Series of daily returns.
    periods_per_year: 252 for daily data (trading days in a year).
    
    Returns a single number. 0.20 means 20% annual volatility.
    """
     returns_clean = returns.dropna()
     daily_std = returns_clean.std()
     
     return daily_std * np.sqrt(periods_per_year)
     
       