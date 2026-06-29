---
type: daily_validation
instrument: gbpusd
date: 2026-06-19
week: 2026-W25
active_zone: NONE
v1_structure_intact: false
v1b_intact: false
v3_news_clear: true
vix_veto: false
vix_stale: true
reforecast_action: NONE
reforecast_triggers: []
e0_entry_confirmation: false
e1: false
e2: false
e3: false
e4: false
e5: false
entry_confluence_score: 0.0
zone_confluence_score: 6.5
e0_pattern: none
anchor_type: zone_50pct
anchor_price: 0.00
h4_atr: 0.00392
d1_atr: 0.00809
d1_atr_compressed: false
sl_distance: 0.00
offset: 0.00
order_limit: INVALIDATED
limit_price: 0.00
limit_direction: N/A
limit_expires: 2026-06-19 21:00 UTC
tp1_price: 0.00
tp2_price: 0.00
be_trigger_r: 1.5
dfii10_now: 2.23
dfii10_baseline: 2.16
dfii10_slope: 0.10
dxy_slope: 1.646
adx_val: 19.3
---

# Validation — 2026-06-19 (W25 Friday close)

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 1.32016 | — |
| DGS2 | 4.20% | baseline 4.05%, drift +0.15% |
| DXY jump | +0.746 | WITH SHORT zones (USD strength) |
| H4 ATR | 0.00392 | — |
| D1 ATR | 0.00809 | median 0.00754 → expanding |
| VIX | 18.44 | stale (06-17) |
| ADX(14) D1 | 19.3 | RANGING |

## Q1+Q2 — Hard Blocks

### PRIMARY SHORT 1.3440–1.3465
| | Block | Result | Note |
|---|---|---|---|
| V1b | 2 consec H4 closes above 1.3471 | ✅ | Closes 1.32011, 1.32016 — far below zone |

No approach (spot 1.32016, ~190 pips below zone floor). BoE held yesterday — cable fell hard.

### COUNTER LONG 1.3304–1.3330
| | Block | Result | Note |
|---|---|---|---|
| V1b | 2 consec H4 closes below 1.3298 | ❌ BREACH | H4 closes: 1.32011, 1.32016 — both < 1.32980 |

→ ❌ **INVALIDATED** — V1b breach. Price pushed below support. Remove from _HOT.md.

## Q3 — Re-Forecast Check
DGS2 +0.15 borderline T5. DXY jump WITH the SHORT zone (not a block). No mandatory re-forecast.

## Q4 — Entry Confluence
No approach on PRIMARY SHORT. No score.

## Result
❌ NO TRADE — PRIMARY SHORT 1.3440–1.3465: no zone approach (spot 1.32016, ~190 pips below zone). W25 closes today.
❌ INVALIDATED — COUNTER LONG 1.3304–1.3330: V1b breach (2 consecutive H4 closes below 1.3298). Remove from tracking.
