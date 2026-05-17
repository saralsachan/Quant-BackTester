"""Basic tests for the cost functions."""

import sys #module that has access to system settings and files
sys.path.insert(0, "src")  #sys.path contains all files paths, we are inserting src at the 0 index of path lists, so first we check src folder 

import pandas as pd

from backtester.engine.costs import (
    compute_trades,
    compute_costs,
    apply_costs_to_returns,
)


def test_compute_trades_single_stock():
    """Buying 0.5, holding, then selling should give trades [NaN, 0.5, 0, 0, 0.5]."""
    positions = pd.Series([0, 0.5, 0.5, 0.5, 0])
    trades = compute_trades(positions)
    
    assert pd.isna(trades.iloc[0])
    assert trades.iloc[1] == 0.5
    assert trades.iloc[2] == 0.0
    assert trades.iloc[3] == 0.0
    assert trades.iloc[4] == 0.5


def test_compute_trades_multi_stock():
    """Rotating from one stock to another should be counted as 2 trades worth."""
    positions = pd.DataFrame({
        "A": [0.0, 0.5, 0.0],
        "B": [0.0, 0.0, 0.5],
    })
    trades = compute_trades(positions)
    
    assert trades.iloc[0] == 0.0 or pd.isna(trades.iloc[0]) #pandas DataFrame considers NaN to be 0 when using sum()
    assert trades.iloc[1] == 0.5   # Bought A
    assert trades.iloc[2] == 1.0   # Sold A (0.5) + Bought B (0.5) = 1.0


def test_compute_costs_uses_correct_rate():
    """A trade of 0.5 with default 0.15% rate should cost 0.00075."""
    positions = pd.Series([0, 0.5])
    costs = compute_costs(positions)
    
    assert abs(costs.iloc[1] - 0.00075) < 1e-9


def test_compute_costs_custom_rate():
    """Custom rates should override the default."""
    positions = pd.Series([0, 1.0])
    costs = compute_costs(positions, cost_per_trade=0.005)
    
    # Trade size 1.0 × rate 0.005 = 0.005
    assert abs(costs.iloc[1] - 0.005) < 1e-9


def test_apply_costs_subtracts_correctly():
    """Net return = gross return - cost."""
    gross_returns = pd.Series([0.01, 0.01, 0.01])
    positions = pd.Series([0, 0.5, 0.5])
    
    net = apply_costs_to_returns(gross_returns, positions)
    
    # Day 0: NaN trade, so NaN cost, so net is NaN
    # Day 1: trade 0.5, cost 0.00075, net = 0.01 - 0.00075 = 0.00925
    # Day 2: no trade, cost 0, net = 0.01
    assert pd.isna(net.iloc[0])
    assert abs(net.iloc[1] - 0.00925) < 1e-9
    assert abs(net.iloc[2] - 0.01) < 1e-9


def test_buy_and_hold_costs_only_on_entry():
    """Buy and hold should only incur cost on entry day."""
    # Position is 1 from day 1 onwards
    positions = pd.Series([0, 1, 1, 1, 1])
    costs = compute_costs(positions)
    
    # Day 0: NaN, Day 1: cost from entering, Days 2-4: no costs
    assert pd.isna(costs.iloc[0])
    assert costs.iloc[1] > 0
    assert costs.iloc[2] == 0
    assert costs.iloc[3] == 0
    assert costs.iloc[4] == 0
    
    
    """RUNNING THE TEST- uv run pytest tests/ -v"""