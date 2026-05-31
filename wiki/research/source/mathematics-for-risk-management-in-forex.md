---
type: paper_review
paper: ssrn-6184238.pdf
title: "Mathematics for Risk Management in the Forex Market"
authors: "Gerson Justiniano"
year: 2026
venue: "SSRN working paper"
tier: 1
updated: 2026-05-31
confidence: high
tags: [risk, position-sizing, stop-loss, take-profit, leverage, margin, portfolio]
related: [constitution, swing-trading-risk-magnitude]
---

# Math for Risk Management in Forex

**One-liner**: Closed-form formulas for leverage/margin, lot sizing, SL/TP price levels, and aggregating many open positions into one global TP/SL target.

## Why we kept it
Pure mechanics layer for our constitution risk rules. Maps to $2000/trade sizing, stop-distance → lot conversion, and (most useful) collapsing multiple open setups into ONE portfolio-level TP/SL — relevant when XAUUSD + EURUSD both live.

## Method
- Market / instrument: generic leveraged FX (broker margin model).
- Data range + N: none — analytical derivation, no backtest.
- Technique: algebra on leverage, margin, pip value, lot size; Python reference class `risk_management` with `global_TpSl()` aggregation + matplotlib viz.

## Key values
- Leverage example: 1:10 on $100 controls $1,000 notional; higher leverage → closer liquidation.
- Provides closed forms for: position size from risk budget, margin per position, global TP and global SL price across a basket of mixed buy/sell orders (volume- and margin-weighted).
- Worked code example: leverage 500, standard_lot 100,000, 3 open positions → computes global TP/SL.
- No performance metrics (not a strategy paper).

## Apply to us
- Use the global TP/SL aggregation formula to express combined risk when >1 instrument/setup is open simultaneously — single dollar-risk view instead of per-trade only.
- Cross-check our stop-distance → lot sizing against its margin/pip-value math.
- Reference classes (Hull, Murphy, Kaufman) confirm it's textbook-standard, safe to lift.

## Caveats
- Educational; no edge, no backtest. It's a calculator, not a strategy.
- Broker margin conventions vary — verify pip value / contract size for XAUUSD (gold lot ≠ FX lot).

**Verdict**: borrow the formulas (sizing + multi-position global TP/SL); ignore as a strategy.
