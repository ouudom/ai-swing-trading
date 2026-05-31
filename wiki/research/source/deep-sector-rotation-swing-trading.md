---
type: paper_review
paper: ssrn-4280640.pdf
title: "Deep Sector Rotation Swing Trading"
authors: "Joel R. Bock, Akhilesh Maewal"
year: 2023
venue: "SSRN working paper"
tier: 1
updated: 2026-05-31
confidence: medium
tags: [swing, weekly, backtest, deep-learning, sharpe, drawdown, sector-rotation]
related: [r-target, cointegration-pairs-walk-forward]
---

# Deep Sector Rotation Swing Trading

**One-liner**: Weekly-cadence swing system over 11 US-sector ETFs using a multi-input/multi-output deep model beats buy-and-hold 2012–2022.

## Why we kept it
Same cadence as our `/weekly` (weekly decision, multi-day hold). Useful as a backtest-design and metric-reporting template (CAGR vs benchmark, Sharpe, max DD, alpha in a bad year).

## Method
- Market / instrument: 11 SPDR US sector ETFs.
- Data range + N: Jan 2012 – Dec 2022 (11 yr), weekly trades.
- Technique: deep learning, multi-input multi-output, predicts next-week relative sector performance; rotate into top sectors. Dropout-as-Bayesian for uncertainty.

## Key values

| Metric | Value |
|---|---|
| Annualized excess CAGR vs buy-hold | **+12.63%** mean (+7.63% median) |
| 2022 alpha (S&P −18% CAGR yr) | **α = +28.4%** |
| Avg Sharpe | **1.39** |
| Mean max drawdown | **10%** |

- Results **exclude trading costs** (authors flag cost analysis as prerequisite to deployment).
- Cites that naive business-cycle market-timing is "indistinguishable from random" — edge comes from the model, not calendar rotation.

## Apply to us
- Adopt their metric panel for our backtests: excess CAGR vs benchmark, Sharpe, max DD, and alpha in the worst regime year.
- Multi-output design = predict several instruments at once → supports multi-instrument breadth (our low per-instrument frequency rationale).
- Strongest result is in the hard year (2022) — test our edge specifically in adverse gold/USD regimes, not just the 2020–26 uptrend.

## Caveats
- ETFs, long-bias rotation — not gold/FX, not shorting.
- Costs excluded (could erode a weekly-rebalance edge materially).
- "Preliminary" per authors; deep model = overfit risk on 11-yr sample.

**Verdict**: study for backtest methodology + metrics; treat the returns as cost-free upper bound.
