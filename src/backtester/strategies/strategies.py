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