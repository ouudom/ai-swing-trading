---
type: system
updated: 2026-05-28
confidence: medium-low
tags: [eurusd, constitution, reforecast, invalidation, swing]
related: [confluence_criteria.md, macro_drivers.md, profile.md]
---

# EURUSD Constitution Addendum

> Same architecture as XAUUSD: weekly forecast (`/weekly eurusd`) → daily validation
> (`/validate eurusd`) → outward-offset limit. Universal rules in `wiki/system/core/constitution.md`.
> This file = EURUSD-specific overrides only. All thresholds in PIPS (0.0001).

## Risk & Sizing
- Risk/trade: $2,000 (shared account weekly $4,000 / monthly $10,000 caps).
- `lots = floor($2,000 / (stop_distance_price × 100000))`. TICK_MULTIPLIER=100000 (config; fixed from 10000 bug 2026-05-28).

## Stop Formula (inherited, pip-scaled)
`stop_distance = avg(0.5×D1_ATR14, H4_ATR14_trading, structural_dist)` — arithmetic mean.
- H4_ATR14_trading: filter H4 bars with range ≥ **5 pips (0.0005)** to drop weekend/holiday flatline
  (gold uses $1; 5 pips is the EUR-scale equivalent).
- structural_dist: nearest fractal pivot within last 5 trading days (`scripts/structure.py`).
- cap: structural_dist > 3×H4_ATR → NO TRADE. floor: < 0.5×H4_ATR → reuse-yesterday / 2-component fallback.

## Outward-Offset Limit (the live edge — kept)
`entry_offset = (10 − score) × 0.25 × stop_distance`, OUTWARD beyond zone extreme. Same coefficient
as XAUUSD. This is the live-execution edge; not tuned away by backtest.

## Re-Forecast Triggers (EUR-scaled)
| Trigger | EUR threshold | Source |
|---|---|---|
| T1 — rate-diff 1d jump | \|Δ(DGS2−ESTR)\| > 0.10 | FRED DGS2, ESTR |
| T2 — DXY 1d jump | > 0.75 ICE points | data/yahoo/DXY.csv |
| T3 — EUR D1 counter-move | > **1.0%** against weekly bias (calibrated p97 of 6.4yr daily \|%move\|; D1 ATR ≈0.6% so this is a rare ~1.7×ATR reversal) | 1day.csv |
| T4 — unscheduled shock (X or Y) | T4-X structured news OR T4-Y VIX +5 | news / VIXCLS |
| T5 — rate-diff cumulative drift | \|now − baseline\| > 0.15 | DGS2−ESTR vs weekly frontmatter |
Hard preconditions + decision tree: same as constitution. Forward-only 12h event gate. Week-scoped.

## News / V3 Hard Blocks (within 2h of London 08:00 or NY 13:00 open)
- US: NFP, FOMC, CPI, Retail Sales, PCE/GDP
- EU: ECB rate decision + press conference, EU HICP (flash/final), German CPI, EU/German PMI flash
- T4-X structured-news scan: same schema (`data/news_events/[DATE]_t4x.json`).

## Invalidation (inherited)
- V1: D1 close beyond zone.
- V1b: 2 consecutive H4 closes > **7 pips** past zone extreme (calibrated 0.3×median H4 range ≈7p; was 5p).
- Macro reversal: rate differential + DXY both flip against trade direction.

## Weekend Gap Gate (Monday) — EUR-calibrated (E5; gold's % are ~10× too big for EUR)
6.4yr Fri→next-open \|gap%\| distribution: median 0.05%, p90 0.22%, p99 0.61%.

| \|gap_pct\| | Action |
|---|---|
| < 0.05% | Noise. Log only. |
| 0.05–0.20% | NOTE in Monday /validate. No bias change. |
| 0.20–0.50% | **WARNING** — re-examine bias / redraw zones before /validate. |
| > 0.50% | **Hard re-forecast** — re-run /weekly Monday; Sunday forecast voided. |

## Correlation Guard (shared)
USD_BETA_SIGN = −1 (EUR inverse USD, same as gold). Gold-long + EUR-long = stacked short-USD →
halve/reject per constitution Correlation Guard.

## Calibration — DONE (E5, 2026-05-28, `scripts/calibrate_eurusd.py`, 6.4yr)
- T3 counter-move = 1.0% (p97). Weekend-gap tiers EUR-scaled (above). V1b = 7 pips. G6 cutoff = 35 pips.
- Reference: D1 ATR14 ≈ 69 pips, H4 ATR14 ≈ 27 pips. H4 5-pip flatline filter confirmed.
- Open: 6E volume-profile depth quality (verify at first live /weekly eurusd).
