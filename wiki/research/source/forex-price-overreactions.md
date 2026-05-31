---
type: paper_review
paper: ssrn-3362142.pdf
title: "Price Overreactions in the Forex and Trading Strategies"
authors: "Guglielmo Maria Caporale, Alex Plastun"
year: 2019
venue: "Brunel Univ. Econ & Finance WP 19-09 / SSRN"
tier: 2
updated: 2026-05-31
confidence: medium
tags: [overreaction, mean-reversion, anomaly, intraday, eurusd, abnormal-returns, contrarian]
related: [opening-gaps-swing-intraday, session-timing]
---

# Price Overreactions in Forex

**One-liner**: After a daily overreaction, FX continues in the overreaction direction that day but reverses the next day — a tradable contrarian anomaly.

## Why we kept it
Direct EUR/USD mean-reversion edge with a defined trigger. Candidate confluence/contrarian signal and pairs with the gap-fade idea ([[opening-gaps-swing-intraday]]).

## Method
- Market / instrument: EURUSD, USDJPY, USDCAD, AUDUSD, EURJPY.
- Data range + N: daily + intraday (hourly), 01.01.2008–31.12.2018.
- Technique: dynamic-trigger detection of overreaction days; cumulative abnormal returns (CAR); compare overreaction-day vs normal-day intraday paths. Tested H1/H2/H3.

## Key values
- H1 supported: intraday hourly-return behaviour on overreaction days **differs significantly** from normal days.
- Within overreaction day: price moves **in** the overreaction direction.
- **Next day: price moves in the opposite direction** (reversal) — the exploitable part.
- Reported trading strategies generate **abnormal profits** → evidence of market inefficiency.
- Reference samples: ~58 overreaction-hour obs vs ~2500 normal — CAR tables per hour, both positive and negative overreactions.

## Apply to us
- Build a "day-after-overreaction fade" contrarian signal for EURUSD; define overreaction via dynamic vol-scaled trigger (their method) not a fixed %.
- Useful as a counter-trend confluence input distinct from our momentum bias — flag when a setup is fighting a likely next-day reversal.

## Caveats
- Daily/intraday horizon, not our weekly→H4 swing; needs re-test at our cadence.
- 2008–2018; abnormal profits before realistic costs/spreads.

**Verdict**: borrow the overreaction-fade signal for EURUSD; validate at swing horizon.
