---
type: paper_review
paper: ssrn-1685150.pdf
title: "Predicting Break-Points in Trading Strategies with Twitter"
authors: "Arnaud Vincent, Margaret Armstrong"
year: 2010
venue: "SSRN working paper"
tier: 2
updated: 2026-05-31
confidence: low
tags: [regime-change, breakpoint, news, sentiment, relearning, eurusd, re-forecast-trigger]
related: [fx-trading-strategy-evolution, forex-price-overreactions]
---

# Predicting Break-Points with Twitter

**One-liner**: External news shocks (detected via Twitter buzz) cause regime breakpoints; a strategy that pauses and re-learns after a Twitter alert beats one that doesn't.

## Why we kept it
Maps to our re-forecast trigger concept: detect when the regime has changed and force a re-evaluation instead of blindly trading the old bias.

## Method
- Market / instrument: EUR/USD (hold USD or EUR, decide every 2 min).
- Data range + N: 5-month test window (short).
- Technique: genetic-algorithm trading rule as benchmark vs hybrid that halts + re-learns after each Twitter alert; compare performance.

## Key values
- Hybrid (relearn-on-alert) **significantly outperformed** the static GA benchmark over 5 months.
- "Twitter wave": a non-monotone relationship between reaction lag to an alert and performance — there's an optimal delay, not "react instantly."
- Authors stress 5 months is too short; preliminary.

## Apply to us
- Formalize a **re-forecast trigger**: on a detected macro/news regime break, invalidate pending setups and re-run the weekly rather than holding stale bias.
- "Twitter wave" lesson = don't necessarily react to news instantly; there may be an optimal lag before re-entering — test reaction timing.

## Caveats
- HFT-style 2-min EURUSD, genetic algo, 5-mo sample — far from our weekly swing; transfer is conceptual only.
- 2010 vintage; Twitter-as-signal infrastructure dated.

**Verdict**: context only — motivates a regime-break re-forecast trigger; method not portable.
