---
type: paper_review
paper: ssrn-1932844.pdf
title: "Lessons from the Evolution of Foreign Exchange Trading Strategies"
authors: "Christopher J. Neely, Paul A. Weller (Fed Reserve Bank of St. Louis)"
year: 2013
venue: "Fed St. Louis Working Paper 2011-021D"
tier: 1
updated: 2026-05-31
confidence: high
tags: [FX, technical-rules, adaptive-markets, carry, momentum, sharpe, edge-decay, eurusd]
related: [fundamentalist-fx-trading, macro-regime]
---

# Lessons from Evolution of FX Trading Strategies

**One-liner**: Under the Adaptive Markets Hypothesis, FX technical-rule edges are real but decay/rotate over time; an adaptive backtest-selected portfolio beats static rules and dramatically beats equities.

## Why we kept it
Authoritative (Fed) reality-check on whether technical FX edges persist — directly relevant to standing up the EURUSD system and to not over-trusting any single fixed confluence rule.

## Method
- Market / instrument: FX (major + emerging), carry trade, US equities.
- Data range + N: ~1973–2012 (rolling), hypothetical adaptive trader.
- Technique: out-of-sample "ex ante" backtesting picks optimal portfolio of technical rules (filters, channels, MAs, momentum) + carry; track rule prevalence over time.

## Key values
- Adaptive backtest selection **beats** non-adaptive static rules.
- **FX trading alone dramatically outperforms S&P 500** — much larger Sharpe over full sample.
- Little extra gain from combining FX + equity strategies (low diversification benefit).
- Rule prevalence **rotates** over decades (filter/channel/MA/momentum/carry wax and wane) — classic edge decay; rules that worked early erode as adopted.
- Rolling 1-yr Sharpe of top portfolios swings widely (≈ −3 to +4) — edges are regime-dependent, not constant.

## Apply to us
- Treat every confluence rule as **decaying**: schedule periodic re-validation, don't freeze weights forever.
- Expect regime-dependent Sharpe — our low-frequency edge will have long flat/negative stretches; size expectations accordingly.
- Supports adaptive/walk-forward parameter selection over fixed params (pairs with [[cointegration-pairs-walk-forward]] WFO).
- Evidence FX technical edges are genuine → reasonable to build EURUSD on technical+macro confluence.

## Caveats
- Pre-2013, broad-survey level; no XAUUSD specifically.
- "Outperforms equities" is historical and includes high-vol EM rules; survivorship/selection in rule universe.

**Verdict**: study deeply — frames our whole edge-decay + re-validation discipline.
