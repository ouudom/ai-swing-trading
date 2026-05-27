---
type: system
updated: 2026-05-27
confidence: low
tags: [eurusd, constitution, reforecast, invalidation]
related: [macro_drivers.md, confluence_criteria.md]
---

# EURUSD Constitution Addendum

> **STATUS: SCAFFOLD — define before running /weekly eurusd.**
> Universal rules live in `wiki/system/constitution.md` (risk, stop formula, R calc, V1/V1b).
> This file contains EURUSD-specific overrides and additions only.

## Risk (inherited from constitution)
$2,000/trade — same as all instruments.

## Stop Formula (inherited from constitution)
`avg(0.5 × D1_ATR14, H4_ATR14_trading, structural_dist)` — same formula.
All values in price units (e.g. 0.0050 = 50 pips).
`H4_ATR14_trading`: filter bars with range < 0.0005 (5 pips) to drop weekend/holiday flatline.

## Lot Sizing
`lots = floor($2,000 / (stop_distance × 10,000))`
See `profile.md` for pip value details.

## Re-Forecast Triggers (TODO — define T1-T5 equivalent)

See `macro_drivers.md` for trigger concepts. Thresholds TBD:
- T1: ECB inter-meeting action OR rate differential 1-day jump > X% (TBD)
- T2: DXY 1-day jump > 1.0% (same threshold as XAUUSD T2)
- T3: EUR/USD D1 counter-move > X% against weekly bias (TBD — XAUUSD uses 2.5%)
- T4: unscheduled macro shock (same T4-X/T4-Y framework as constitution)
- T5: rate differential cumulative drift > X% from baseline (TBD)

## Hard Preconditions (inherited from constitution)
Same 5 preconditions as XAUUSD re-forecast gate.

## Scheduled Event Hard Blocks (V3 additions)
Standard: NFP, FOMC, CPI, US Retail Sales (same as XAUUSD)
EURUSD-specific additions:
- ECB rate decision
- EU HICP (CPI flash and final)
- German CPI
- EU/German PMI flash
- ECB press conference

## Invalidation (inherited from constitution)
- V1: D1 close beyond zone — same rule
- V1b: 2 consecutive H4 closes beyond zone — threshold: > 5 pips past extreme (TBD)
- Macro reversal: rate differential flips against trade direction
