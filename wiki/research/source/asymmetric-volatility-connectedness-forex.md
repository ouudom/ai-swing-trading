---
type: paper_review
paper: 1607.08214v1.pdf
title: "Asymmetric Volatility Connectedness on Forex Markets"
authors: "Jozef Baruník, Evžen Kočenda, Lukáš Vácha"
year: 2016
venue: "arXiv 1607.08214 (q-fin) / Journal of Financial Economics"
tier: 2
updated: 2026-05-31
confidence: medium
tags: [volatility, spillover, asymmetry, semivariance, regime, eurusd, macro]
related: [global-vrp-fx-predictability, atr-compression, macro-regime]
---

# Asymmetric Volatility Connectedness on Forex

**One-liner**: "Bad" (downside) volatility spills across FX pairs more than "good" volatility; spillover sign tracks macro events (debt crisis = negative, monetary/commodity shifts = positive).

## Why we kept it
Volatility-regime context for FX, incl. EUR. Reinforces that downside vol is the dangerous, contagious kind — relevant to our ATR/vol gates and risk-off behaviour.

## Method
- Market / instrument: 6 most-traded currencies incl. EUR, JPY, CHF, GBP, AUD, CAD.
- Data range + N: high-frequency intraday, 2007–2015.
- Technique: realized semivariance (good/bad) + spillover/connectedness index; Spillover Asymmetry Measure (SAM) with bootstrap CIs.

## Key values
- Spillovers are **asymmetric**: bad volatility dominates good.
- Negative spillover asymmetry ↔ European sovereign debt crisis (fiscal).
- Positive spillover asymmetry ↔ subprime crisis, divergent central-bank policy, commodity moves (monetary + real-economy).
- Total spillover index co-moves with Fed funds rate, TED spread, VIX (their Fig C.2).

## Apply to us
- During risk-off (rising VIX/TED), expect downside-vol contagion across pairs — tighten risk / lower conviction, consistent with our VIX context use.
- Good/bad semivariance split is a cleaner vol input than symmetric ATR — possible future feature for EURUSD vol gating.

## Caveats
- Intraday spillover study, not a trading strategy; no entry/exit, no PnL.
- 2007–2015 crisis-heavy sample; no gold.

**Verdict**: context only — informs how we read vol regimes, not a tradable rule.
