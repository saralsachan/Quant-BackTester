"""Quant backtester dashboard — Streamlit app."""

import sys
sys.path.insert(0, "src")

import streamlit as st
import pandas as pd

from backtester.data.loader import load_multiple_tickers, get_close_prices
from backtester.data.universes import NIFTY_50
from backtester.metrics.metrics import daily_returns, performance_report
from backtester.strategies.strategies import (
    buy_and_hold,
    moving_average_crossover,
    momentum_signal,
    positions_to_returns,
)
from backtester.engine.costs import apply_costs_to_returns


st.title("Quant Backtester")
st.write("A dashboard for evaluating trading strategies on Indian equities.")


@st.cache_data
def load_universe():
    """Cached data loader — only runs once per Streamlit session."""
    data = load_multiple_tickers(NIFTY_50, "2015-01-01", "2024-12-31")
    prices = get_close_prices(data).dropna(axis=1, how="all")
    return prices


def run_strategy(strategy_name, prices, apply_costs_flag, **params):
    """Run the chosen strategy and return its return series.
    
    strategy_name: which strategy to run.
    prices: the price DataFrame.
    apply_costs_flag: whether to subtract transaction costs.
    **params: strategy-specific parameters (top_n, ticker, etc.).
    
    Returns the daily return series (gross or net depending on apply_costs_flag).
    """
    asset_returns = daily_returns(prices)
    
    if strategy_name == "Buy & Hold":
        ticker = params["ticker"]
        positions = buy_and_hold(prices[ticker])
        gross_returns = positions_to_returns(positions, asset_returns[ticker])
    
    elif strategy_name == "Momentum top-N":
        positions = momentum_signal(
            prices,
            lookback_months=params["lookback_months"],
            top_n=params["top_n"],
        )
        shifted = positions.shift(1)
        gross_returns = (shifted * asset_returns).sum(axis=1)
    
    elif strategy_name == "MA Crossover":
        ticker = params["ticker"]
        positions = moving_average_crossover(
            prices[ticker],
            short_window=params["short_window"],
            long_window=params["long_window"],
        )
        gross_returns = positions_to_returns(positions, asset_returns[ticker])
    
    if apply_costs_flag:
        return apply_costs_to_returns(gross_returns, positions), positions
    else:
        return gross_returns, positions


# Sidebar
st.sidebar.header("Strategy Settings")

strategy_name = st.sidebar.selectbox(
    "Choose a strategy",
    ["Buy & Hold", "Momentum top-N", "MA Crossover"],
)

# Show parameters specific to each strategy
if strategy_name == "Buy & Hold":
    selected_ticker = st.sidebar.selectbox(
        "Stock",
        options=["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ITC.NS"],
    )

elif strategy_name == "Momentum top-N":
    top_n = st.sidebar.slider("Top N stocks", min_value=3, max_value=10, value=5)
    lookback_months = st.sidebar.slider("Lookback months", min_value=3, max_value=24, value=12)

elif strategy_name == "MA Crossover":
    selected_ticker = st.sidebar.selectbox(
        "Stock",
        options=["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "ITC.NS"],
    )
    short_window = st.sidebar.slider("Short window (days)", min_value=10, max_value=100, value=50)
    long_window = st.sidebar.slider("Long window (days)", min_value=50, max_value=300, value=200)

apply_costs = st.sidebar.checkbox("Apply transaction costs", value=True)



# Main area
st.subheader("Universe")

with st.spinner("Loading data..."):
    prices = load_universe()
    
    # Collect parameters based on strategy
if strategy_name == "Buy & Hold":
    params = {"ticker": selected_ticker}
elif strategy_name == "Momentum top-N":
    params = {"top_n": top_n, "lookback_months": lookback_months}
elif strategy_name == "MA Crossover":
    params = {
        "ticker": selected_ticker,
        "short_window": short_window,
        "long_window": long_window,
    }

# Run the strategy
with st.spinner("Running strategy..."):
    strategy_returns, positions = run_strategy(strategy_name, prices, apply_costs, **params)

# Show some basic info
st.subheader("Strategy Returns")
# Performance report
st.subheader("Performance Metrics")
report = performance_report(strategy_returns.dropna())

# Convert to a DataFrame for nicer display
report_df = pd.DataFrame.from_dict(report, orient="index", columns=["Value"])
report_df["Value"] = report_df["Value"].apply(lambda v: f"{v:.4f}")
st.dataframe(report_df)
st.write(f"Number of return days: {strategy_returns.dropna().shape[0]}")
st.write(f"First valid date: {strategy_returns.first_valid_index().date()}")

st.write(f"Loaded **{prices.shape[1]} stocks** from {prices.index.min().date()} to {prices.index.max().date()}")