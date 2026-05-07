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