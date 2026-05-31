---
type: research
updated: 2026-05-31
tags: [index, research-papers, literature]
related: [paper_review]
---

# Research Papers — Reviewed Literature

Each PDF has a sibling `.md` summary (precise values, not full text) using the
`wiki/system/templates/paper_review.md` format. Reference summaries, open PDF only when needed.

Pruned 2026-05-31: 16 off-domain papers deleted (institutional-block "swing", SEC §16(b) insider law,
dealer microstructure / WMR fix, retail-loss behavioral, intraday ML/RL/sentiment bots). 12 kept below.

## Tier 1 — study now, hits core methods

| Summary | Paper | Topic | Feeds |
|---|---|---|---|
| [mathematics-for-risk-management-in-forex.md](mathematics-for-risk-management-in-forex.md) | Math for Risk Management in Forex | Closed-form sizing, SL/TP, multi-position global TP/SL | constitution risk rules |
| [opening-gaps-swing-intraday.md](opening-gaps-swing-intraday.md) | Opening gaps in swing/intraday | Big gap → mean-revert; gaps ↔ gold/USD | `weekend_gap_pct` use |
| [swing-trading-risk-magnitude.md](swing-trading-risk-magnitude.md) | Swing-Trading Risk Magnitude (STRM) | Vol-vector × autocorrelation risk scalar | cross-instrument risk rank |
| [deep-sector-rotation-swing-trading.md](deep-sector-rotation-swing-trading.md) | Deep sector-rotation swing | Weekly swing, +12.6% excess CAGR, Sharpe 1.39 | backtest metrics template |
| [fx-trading-strategy-evolution.md](fx-trading-strategy-evolution.md) | Lessons from FX strategy evolution (Fed) | Adaptive markets; FX edges real but decay/rotate | edge-decay + re-validation |
| [global-vrp-fx-predictability.md](global-vrp-fx-predictability.md) | Global VRP & FX predictability | VIX/VRP predicts FX OOS (EURUSD +2.44%) | G5 VIX gate, EURUSD |

## Tier 2 — useful, partial fit

| Summary | Paper | Topic | Feeds |
|---|---|---|---|
| [asymmetric-volatility-connectedness-forex.md](asymmetric-volatility-connectedness-forex.md) | Asymmetric vol connectedness FX | Bad vol contagion > good; tracks VIX/TED | vol-regime reading |
| [forex-price-overreactions.md](forex-price-overreactions.md) | Price overreactions in Forex | Overreaction day → next-day reversal (EURUSD) | contrarian/fade signal |
| [swing-allocation-lazy-portfolio.md](swing-allocation-lazy-portfolio.md) | Swing + alloc + lazy + risk filter | Uncorrelated blend halves drawdown | multi-instrument breadth |
| [fundamentalist-fx-trading.md](fundamentalist-fx-trading.md) | Fundamentalist FX trading | PPP weak; carry works but crisis left-skew | EURUSD macro drivers |
| [twitter-breakpoint-prediction.md](twitter-breakpoint-prediction.md) | Break-points via Twitter | Relearn-on-regime-break beats static | re-forecast trigger |
| [cointegration-pairs-walk-forward.md](cointegration-pairs-walk-forward.md) | Cointegration pairs + WFO | Walk-forward cuts drawdown vs fixed params | param-sweep discipline |

## Read order (Tier 1)
mathematics-for-risk-management-in-forex (risk math) → opening-gaps-swing-intraday (gaps) → fx-trading-strategy-evolution (edge decay) → global-vrp-fx-predictability (VIX gate).
