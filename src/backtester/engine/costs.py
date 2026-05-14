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
    

    