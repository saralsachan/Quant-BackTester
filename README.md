# Quant Backtester

A Python-based backtesting engine for systematic equity trading strategies, with a focus on correctness, realistic transaction costs, and rigorous out-of-sample evaluation.

## Project Goals

- Build a production-quality backtester from scratch to deeply understand both software engineering and quantitative finance.
- Test classic strategies (momentum, mean-reversion, moving average crossover) on Indian and US markets.
- Document what works, what doesn't, and why — with honest reporting on overfitting and bias.

## Status

Week 0: Environment setup — in progress.
### Week 2, Day 1
- Created metrics module with daily_returns function (wraps pct_change)
- Learned: simple vs log returns. Simple multiply over time, log add.
- Plotted Reliance prices and returns side by side. Prices trend; returns look like noise.
- Realization: the chart of returns is humbling — most days are tiny moves; the "interesting" stuff is rare.

### Week 2, Day 2
- Wrote total_return: (1 + r).prod() - 1 — uses compounding, not summing
- Learned: returns multiply over time, not add. +10% then -10% loses you 1%, not 0.
- Wrote annualized_return: total_growth ^ (1/years) - 1 — also called CAGR
- Reliance: ~X% total over 5 years, ~Y% annualized
- Top Nifty 50 performer: [stock] at Z% annualized — surprisingly large gap from worst
- Cross-checked function results against manual computation. Matched.
- Realization: annualization makes vastly different time periods comparable

### Week 2, Day 3

- Built annualized_volatility function (std of returns * sqrt(252))
- Realization: looking at returns alone is misleading. The same return with half the volatility is a much better investment.

### Week 2, Day 4

- Built sharpe ratio function which computer how much extra return (compared to risk free returns) you get per unit risk.
- Tested it on Reialnce and various other stocks.
- Analysed portfolio of a few stocks with sharpe, volatility and returns.

### Week 2, Day 5

- Built maxDropDown Function that tells the maximum peak-to-trough loss in the journey
- Tested it on various stocks
### Week 2, Day 6
- Built a function that computes the report of stock's returns. 
- Consolidated the metric sfucntions into a single function to save time and minimize redundency of calling each and every metric function.
## Tech Stack

Python 3.12, pandas, NumPy, yfinance, Plotly, Streamlit (planned).

## Roadmap

- [ ] Week 1: Data ingestion layer
- [ ] Week 2: Performance metrics
- [ ] Week 3: Strategy framework
- [ ] Week 4: Execution engine
- [ ] Week 5: Walk-forward analysis
- [ ] Week 6: Visualization and dashboard
- [ ] Week 7: Advanced strategy
- [ ] Week 8: Documentation and writeup

## Author

Saral Sachan — IIT Bombay, [Chemical Engineering]