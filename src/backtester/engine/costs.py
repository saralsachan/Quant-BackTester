"""Functions for modeling trading costs and slippage."""

import pandas as pd


def compute_trades(positions):
    """Compute the size of trades each day from a positions Series or DataFrame.
    
    positions: Series (single stock) or DataFrame (multi-stock) of daily positions.
    
    Returns the absolute change in position each day. For a DataFrame, this is
    summed across stocks to give total turnover.
    """
    # Daily change in position
    position_changes = positions.diff()
    
    # If multi-stock (DataFrame), sum absolute changes across stocks
    if isinstance(position_changes, pd.DataFrame): #if position_changes is a dataframe
        return position_changes.abs().sum(axis=1) #sum across columns for each row
    else:
        return position_changes.abs()
    

def compute_costs(positions, cost_per_trade=0.0015):
    """Compute the cost of trading each day.
    
    positions: Series (single stock) or DataFrame (multi-stock) of daily positions.
    cost_per_trade: cost as a fraction of trade size (default 0.15%).
    
    Returns a Series of daily costs (as fractions of portfolio value).
    """
    trades = compute_trades(positions)
    return trades * cost_per_trade    

def apply_costs_to_returns(gross_returns, positions, cost_per_trade=0.0015):
    """Subtract trading costs from gross strategy returns.
    
    gross_returns: Series of strategy returns BEFORE costs.
    positions: the positions that produced those returns.
    cost_per_trade: cost as a fraction of trade size.
    
    Returns the net strategy returns AFTER costs.
    """
    costs = compute_costs(positions, cost_per_trade)
    
    return gross_returns - costs