---
type: paper_review
paper: ssrn-5068086.pdf
title: "Real-World Viability of Cointegration-Based Forex Pairs Trading with Walk-Forward Optimization"
authors: "Alexandre Landi, Tetiana Lemishko (Balanced Research)"
year: 2024
venue: "SSRN working paper"
tier: 2
updated: 2026-05-31
confidence: medium
tags: [walk-forward, WFO, cointegration, pairs, parameter-recalibration, drawdown, overfit]
related: [fx-trading-strategy-evolution, deep-sector-rotation-swing-trading]
---

# Cointegration Pairs Trading + Walk-Forward Optimization

**One-liner**: Re-calibrating strategy params with Walk-Forward Optimization (rolling train→test) preserves return AND cuts drawdown vs a single fixed parameter set.

## Why we kept it
The methodology is the point, not pairs trading. WFO is the disciplined antidote to backtest overfitting — directly applicable to validating our gate weights / offset coefficients over time.

## Method
- Market / instrument: FX pairs (cointegrated).
- Data range + N: 17-year history; prior paper used fixed params over whole period.
- Technique: cointegration filter (trade only if cointegrated in training window), then **WFO** — dynamically recalibrate params per rolling window; compare to static params.

## Key values
- WFO **did not worsen** historical return vs fixed params.
- WFO **reduced maximum drawdown** → improved risk-adjusted performance.
- Static "decent over whole 17yr" params were arbitrary/overfit; WFO adapts to evolving regimes.
- Explicitly cites backtest-overfitting literature (Bailey/López de Prado; Arian et al. 2024).

## Apply to us
- Adopt **walk-forward** for our parameter sweeps (offset_coef, gate weights, R-floor) instead of one global best — current sweeps (`sweep_entry.py`, `sweep_structure.py`) pick whole-sample optima = overfit risk.
- WFO's drawdown reduction is the metric to target, not just PnL.
- Pairs naturally with [[fx-trading-strategy-evolution]] adaptive-markets / edge-decay argument.

## Caveats
- Pairs trading (two-leg, mean-reverting) ≠ our single-instrument directional swing — borrow the WFO process only.
- Companion to ssrn-4771108 (the base cointegration strategy, not in our kept set).

**Verdict**: study the WFO process — apply it to our parameter validation; ignore the pairs strategy itself.
