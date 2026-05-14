"""Basic tests for the data loader."""

import sys
sys.path.insert(0, "src")

from backtester.data.loader import load_ticker, get_close_prices


def test_load_ticker_returns_data():
    df = load_ticker("RELIANCE.NS", "2024-01-01", "2024-06-30")
    assert len(df) > 0
    assert "Close" in df.columns


def test_get_close_prices_returns_one_column_per_stock():
    data = {
        "RELIANCE.NS": load_ticker("RELIANCE.NS", "2024-01-01", "2024-03-31"),
        "TCS.NS": load_ticker("TCS.NS", "2024-01-01", "2024-03-31"),
    }
    prices = get_close_prices(data)
    assert prices.shape[1] == 2
    assert "RELIANCE.NS" in prices.columns
    assert "TCS.NS" in prices.columns