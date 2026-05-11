"""function for converting strategy signals into portfolio returns"""
import pandas as pd
def positions_to_returns(positions, asset_returns):
    """Convert a position series and asset returns into strategy returns.
    
    positions: a Series of positions per day (0 to 1). (not hold/hold/partial hold)
    asset_returns: the actual daily returns of the underlying asset.
    
    Returns the strategy's daily returns — what you would have earned.
    """
    
    actual_positions = positions.shift(1)
    """shift positions by one day to prevent look-ahead-bias VERY IMPORTANT"""
    
    
    strategy_returns = asset_returns * actual_positions
    return strategy_returns


"""Simplest strategy- buy and hold forever"""
def buy_and_hold(prices):
    """Buy and hold: always invested at 100%.
    
    prices: a Series of daily prices.
    
    Returns a positions Series of all 1s."""
    
    positions = pd.Series(1, index = prices.index)
    return positions

def moving_average_crossover(prices, short_window = 50, long_window = 200):
    
    """Moving average crossover: be invested when short MA > long MA.
    
    prices: a Series of daily prices.
    short_window: lookback for the short moving average (default 50 days).
    long_window: lookback for the long moving average (default 200 days).
    
    Returns a positions Series of 0s and 1s.
    """
    #computing the two moving averages
    
    """.rolling(window=50) — pandas creates a "rolling window" object. It says: "for each row, give me the previous 50 rows."""
    
    short_MA = prices.rolling(window = short_window).mean()
    long_MA = prices.rolling(window = long_window).mean()
    
    positions = (short_MA>long_MA).astype(float) #short_MA > long_MA return a series of true/false->convert to 0 and 1
    
    # Set positions to NaN where either MA isn't yet available
    positions[short_MA.isna() | long_MA.isna()] = float("nan")
    
    return positions #series of 0 and 1 and NaN's
    