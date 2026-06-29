---
type: daily_validation
instrument: eurusd
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
zone_confluence_score: 7.5
e0_pattern: none
anchor_type: zone_50pct
anchor_price: 0.00
h4_atr: 0.00288
d1_atr: 0.00636
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
adx_val: 24.2
---

# Validation — 2026-06-19 (W25 Friday close)

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 1.14552 | — |
| DGS2 | 4.20% | baseline 4.05%, drift +0.15% |
| DXY 20d slope | +1.646 | strong USD |
| H4 ATR | 0.00288 | — |
| D1 ATR | 0.00636 | median 0.00555 → expanding |
| VIX | 18.44 | stale (06-17) |
| ADX(14) D1 | 24.2 | TRANSITIONAL |

## Q1+Q2 — Hard Blocks

### PRIMARY LONG 1.1500–1.1520
| | Block | Result | Note |
|---|---|---|---|
| V1b | 2 consec H4 closes below 1.1495 | ❌ BREACH | H4 closes: 1.14579, 1.14552 — both < threshold 1.14950 |

→ ❌ **INVALIDATED** — V1b breach. Price pushed through support. Remove from _HOT.md.

### SECONDARY SHORT 1.1618–1.1640
| | Block | Result | Note |
|---|---|---|---|
| V1b | 2 consec H4 closes above 1.1645 | ✅ | H4 closes 1.14579, 1.14552 — far below zone |

No approach (spot 1.14552, ~160 pips below zone floor). No order limit possible.

## Q3 — Re-Forecast Check
DGS2 baseline drift: 4.05 → 4.20 = +0.15% (exactly at T5 threshold). DXY jump +0.746 (>0.5, WITH eurusd SHORT zone, not against). No mandatory re-forecast triggered for W25 (end of week). **W26 must rebase DGS2 to 4.20.**

## Q4 — Entry Confluence
No approach on SECONDARY SHORT. No score.

## Result
❌ INVALIDATED — PRIMARY LONG 1.1500–1.1520: V1b breach (2 consecutive H4 closes below 1.1495). Remove from tracking.
❌ NO TRADE — SECONDARY SHORT 1.1618–1.1640: no zone approach. W25 closes today.
