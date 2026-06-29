---
type: daily_validation
instrument: eurgbp
date: 2026-06-19
week: 2026-W25
active_zone: NONE
v1_structure_intact: false
v1b_intact: true
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
zone_confluence_score: 6.0
e0_pattern: none
anchor_type: zone_50pct
anchor_price: 0.00
h4_atr: 0.00131
d1_atr: 0.00233
d1_atr_compressed: true
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
adx_val: 12.9
---

# Validation — 2026-06-19 (W25 Friday close)

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 0.86764 | — |
| Rate diff (EUR−GBP) | context only | ECB hiked to 2.25% (06-11), BoE held (06-18) |
| H4 ATR | 0.00131 | — |
| D1 ATR | 0.00233 | median 0.00283 → COMPRESSED ✅ |
| VIX | 18.44 | stale (06-17); NO VIX VETO (cross) |
| ADX(14) D1 | 12.9 | RANGING |

## Q1+Q2 — Hard Blocks

### PRIMARY LONG 0.8608–0.8625
| | Block | Result | Note |
|---|---|---|---|
| V1b | 2 consec H4 closes below 0.86040 | ✅ | Closes 0.86795, 0.86764 — far above zone |

No approach (spot 0.86764, ~140 pips above zone top). Price moved away from this zone.

### SECONDARY SHORT 0.8660–0.8682
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone top | ❌ BREACH | D1 close 06-18 = 0.86795 > zone top 0.8682 |
| V1b | 2 consec H4 closes above 0.86860 | ✅ | H4 closes 0.86795 < 0.86860 (V1b intact, V1 takes precedence) |

→ ❌ **INVALIDATED** — V1 breach. D1 closed above zone top on 06-18 (0.86795 > 0.8682). Price broke out above resistance; short thesis dead. Remove from _HOT.md.

> Note: Though spot today (0.86764) is back below 0.8682, the V1 rule applies to the D1 close on 06-18 which was above the zone. Today's pullback is a retracement within the now-broken structure, not a sweep. Zone is invalidated.

## Q3 — Re-Forecast Check
No macro triggers (cross, macro dead). Price-driven only. T3 counter-move: ~0.7% from range low to 0.868 — below 1.5% threshold. Action: NONE.

D1 CHoCH UP @ 0.86567 (06-18) — market structure has shifted bullish on D1. H4 BOS UP @ 0.86645. W26 forecast will need to reassess: the SHORT edge at the range top may remain valid but the D1 CHoCH shifts bias more bullish. ECB hike (2.25%) post-BoE hold = EUR-leg strong.

## Q4 — Entry Confluence
No valid approach zones. SECONDARY SHORT invalidated. PRIMARY LONG: no approach.

## Result
❌ NO TRADE — PRIMARY LONG 0.8608–0.8625: no zone approach. W25 closes today.
❌ INVALIDATED — SECONDARY SHORT 0.8660–0.8682: V1 breach (D1 close 06-18 = 0.86795 > 0.8682). Remove from tracking.
