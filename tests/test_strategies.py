"""Basic tests for the strategy framework."""

import sys
sys.path.insert(0, "src")

import pandas as pd

from backtester.strategies.strategies import (
    buy_and_hold,
    moving_average_crossover,
    positions_to_returns,
)


def test_buy_and_hold_is_always_one():
    """Buy and hold should produce all 1s."""
    prices = pd.Series([100, 110, 120, 130], 
                       index=pd.date_range("2024-01-01", periods=4))
    positions = buy_and_hold(prices)
    assert (positions == 1).all()


def test_positions_to_returns_shifts_correctly():
    """A position taken today should only affect tomorrow's return."""
    asset_returns = pd.Series([0.01, 0.01, 0.01, 0.01])
    # Position is 1 only on day 0; cash from day 1 onwards
    positions = pd.Series([1, 0, 0, 0])
    
    strategy_returns = positions_to_returns(positions, asset_returns)
    
    # Day 0: NaN (no previous position)
    # Day 1: previous position was 1, so return = 1 * 0.01 = 0.01
    # Day 2: previous position was 0, so return = 0
    # Day 3: previous position was 0, so return = 0
    assert pd.isna(strategy_returns.iloc[0])
    assert strategy_returns.iloc[1] == 0.01
    assert strategy_returns.iloc[2] == 0.0
    assert strategy_returns.iloc[3] == 0.0


def test_buy_and_hold_returns_match_asset_returns():
    """Buy-and-hold should give the same returns as the underlying asset."""
    prices = pd.Series([100, 110, 121, 120, 132],
                       index=pd.date_range("2024-01-01", periods=5))
    asset_returns = prices.pct_change()
    
    positions = buy_and_hold(prices)
    strategy_returns = positions_to_returns(positions, asset_returns)
    
    # Skip the first NaN, the rest should match
    pd.testing.assert_series_equal(
        strategy_returns.iloc[1:],
        asset_returns.iloc[1:],
        check_names=False,
    )


def test_ma_crossover_has_nan_during_warmup():
    """The first long_window - 1 days should be NaN (not enough history)."""
    # Make a simple upward-trending price series
    prices = pd.Series(range(100, 400), 
                       index=pd.date_range("2024-01-01", periods=300))
    positions = moving_average_crossover(prices, short_window=50, long_window=200)
    
    # First 199 days should be NaN (not enough data for 200-day MA)
    assert positions.iloc[:199].isna().all()
    # Later days should have a real value (0 or 1)
    assert positions.iloc[200:].notna().all()