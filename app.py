"""Quant backtester dashboard — Streamlit app."""

import sys
sys.path.insert(0, "src")

import streamlit as st

from backtester.data.loader import load_multiple_tickers, get_close_prices
from backtester.data.universes import NIFTY_50


st.title("Quant Backtester")
st.write("A dashboard for evaluating trading strategies on Indian equities.")

# Sidebar
st.sidebar.header("Strategy Settings")

strategy_name = st.sidebar.selectbox(
    "Choose a strategy",
    ["Buy & Hold", "Momentum top-5", "MA Crossover"],
)

apply_costs = st.sidebar.checkbox("Apply transaction costs", value=True)

# Main area
st.write(f"Strategy: **{strategy_name}**")
st.write(f"Apply costs: **{apply_costs}**")

# Load data
st.write("---")
st.subheader("Universe")

@st.cache_data
def load_universe():
    """Cached data loader — only runs once per Streamlit session."""
    data = load_multiple_tickers(NIFTY_50, "2015-01-01", "2024-12-31")
    prices = get_close_prices(data).dropna(axis=1, how="all")
    return prices

with st.spinner("Loading data..."):
    prices = load_universe()

st.write(f"Loaded **{prices.shape[1]} stocks** from {prices.index.min().date()} to {prices.index.max().date()}")
st.dataframe(prices.head()) #A great method that let's user to sort, view, scroll the dataset| USER-FRIENDLY
