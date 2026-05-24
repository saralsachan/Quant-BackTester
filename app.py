"""Quant backtester dashboard — Streamlit app."""

import sys
sys.path.insert(0, "src")

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
    """Run the chosen strategy and return its return series."""
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


# --- Sidebar ---
st.sidebar.header("Strategy Settings")

strategy_name = st.sidebar.selectbox(
    "Choose a strategy",
    ["Buy & Hold", "Momentum top-N", "MA Crossover"],
)

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


# --- Universe section ---
st.subheader("Universe")

with st.spinner("Loading data..."):
    prices = load_universe()

st.write(
    f"Loaded **{prices.shape[1]} stocks** from "
    f"{prices.index.min().date()} to {prices.index.max().date()}"
)


# --- Strategy parameters ---
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


# --- Run strategy ---
with st.spinner("Running strategy..."):
    strategy_returns, positions = run_strategy(strategy_name, prices, apply_costs, **params)


# --- Metrics + info side by side ---
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Performance Metrics")
    report = performance_report(strategy_returns.dropna())
    report_df = pd.DataFrame.from_dict(report, orient="index", columns=["Value"])
    report_df["Value"] = report_df["Value"].apply(lambda v: f"{v:.4f}")
    st.dataframe(report_df, use_container_width=True)

with col2:
    st.subheader("Strategy Info")
    st.write(f"**Strategy:** {strategy_name}")
    st.write(f"**Costs applied:** {apply_costs}")
    st.write(f"**Number of trading days:** {strategy_returns.dropna().shape[0]}")
    st.write(f"**First valid date:** {strategy_returns.first_valid_index().date()}")
    st.write(f"**Last date:** {strategy_returns.last_valid_index().date()}")


# --- Compute equity curve, drawdown, and benchmark ---
returns_clean = strategy_returns.dropna()
equity_curve = (1 + returns_clean).cumprod()
running_peak = equity_curve.cummax()
drawdown = (equity_curve - running_peak) / running_peak

asset_returns_for_benchmark = daily_returns(prices)

if strategy_name == "MA Crossover":
    ticker = params["ticker"]
    benchmark_returns = asset_returns_for_benchmark[ticker]
    benchmark_label = f"Buy & Hold {ticker}"
else:
    benchmark_returns = asset_returns_for_benchmark.mean(axis=1)
    benchmark_label = "Equal-weight basket"

benchmark_equity = (1 + benchmark_returns.dropna()).cumprod()


# --- Equity curve chart with benchmark ---
st.subheader("Equity Curve vs Benchmark")

fig_equity = go.Figure()
fig_equity.add_trace(
    go.Scatter(
        x=equity_curve.index,
        y=equity_curve.values,
        mode="lines",
        name=strategy_name,
        line=dict(color="steelblue", width=2),
    )
)
fig_equity.add_trace(
    go.Scatter(
        x=benchmark_equity.index,
        y=benchmark_equity.values,
        mode="lines",
        name=benchmark_label,
        line=dict(color="gray", width=1.5, dash="dash"),
    )
)
fig_equity.update_layout(
    title=f"Value of ₹1 invested — {strategy_name} vs {benchmark_label}",
    xaxis_title="Date",
    yaxis_title="Value (₹)",
    hovermode="x unified",
    height=450,
)
st.plotly_chart(fig_equity, use_container_width=True)


# --- Drawdown chart ---
st.subheader("Drawdown")

fig_dd = go.Figure()
fig_dd.add_trace(
    go.Scatter(
        x=drawdown.index,
        y=drawdown.values,
        mode="lines",
        name="Drawdown",
        line=dict(color="red", width=1),
        fill="tozeroy",
        fillcolor="rgba(255, 0, 0, 0.2)",
    )
)
fig_dd.update_layout(
    title=f"Drawdown over time — {strategy_name}",
    xaxis_title="Date",
    yaxis_title="Drawdown",
    yaxis_tickformat=".0%",
    hovermode="x unified",
    height=300,
)
st.plotly_chart(fig_dd, use_container_width=True)