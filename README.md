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