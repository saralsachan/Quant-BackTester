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
     

def sharpe_ratio(returns, risk_free_rate=0.06, periods_per_year=252):
    """Compute the annualized Sharpe ratio.
    
    returns: a pandas Series of daily returns.
    risk_free_rate: annual risk-free rate (default 6%, roughly Indian T-bill yield).
    periods_per_year: 252 for daily data.
    
    Returns a single number. Higher is better. 1.0+ is good.
    """
    annual_return = annualized_returns_CAGR(returns)
    annual_volatility = annualized_volatility(returns)
    
    if(annual_volatility == 0):  # guard against division by zero. If volatility is somehow exactly zero (e.g., a flat-line price series in test data), return 0 instead of crashing. Real stocks never have zero volatility, but defensive coding catches edge cases.
        return 0
    
    return (annual_return - risk_free_rate) / annual_volatility       

def max_drawdown(returns):
     """Compute the maximum peak-to-trough drawdown.
    
    returns: a pandas Series of daily returns.
    
    Returns a single number, always <= 0.   -0.30 means a 30% drawdown.
    """
     returns_clean = returns.dropna()
     
     #building the equity curve (cumulative product of 1+r)
     
     equity_curve = (1+returns_clean).cumprod()
     
      #running peak for each day
     
     running_peak = equity_curve.cummax()
     
     #drwadown each day
     
     drawdown = (equity_curve - running_peak) / running_peak # element-wise subtraction and division. Pandas does this for the whole series at once. The result is the drawdown at each day.
     
     return drawdown.min()