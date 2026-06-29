---
type: daily_validation
instrument: audusd
date: 2026-06-19
week: 2026-W25
active_zone: NONE
v1_structure_intact: true
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
zone_confluence_score: 6.5
e0_pattern: none
anchor_type: zone_50pct
anchor_price: 0.00
h4_atr: 0.00213
d1_atr: 0.00536
d1_atr_compressed: true
sl_distance: 0.00
offset: 0.00
order_limit: NO_TRADE
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
adx_val: 31.5
---

# Validation — 2026-06-19 (W25 Friday close)

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 0.70093 | — |
| DGS2 | 4.20% | context only (DXY-jump dead for AUD) |
| H4 ATR | 0.00213 | — |
| D1 ATR | 0.00536 | median 0.00556 → COMPRESSED ✅ |
| VIX | 18.44 | stale (06-17); NO VIX VETO for AUD (inverted) |
| ADX(14) D1 | 31.5 | TRENDING — just crossed 30 (fade-veto zone) |

## Q1+Q2 — Hard Blocks

### PRIMARY SHORT 0.7065–0.7110
| | Block | Result | Note |
|---|---|---|---|
| V1b | 2 consec H4 closes above 0.71140 | ✅ | Closes 0.70130, 0.70093 — below zone |
| ADX veto | D1 ADX>30 trending against fade | N/A | ADX 31.5 trending DOWN = WITH the SHORT zone (not against) |

No approach (spot 0.70093, ~72 pips below zone floor 0.7065). Price needs rally to reach zone.

### COUNTER LONG 0.6980–0.7000
| | Block | Result | Note |
|---|---|---|---|
| V1b | 2 consec H4 closes below 0.69760 | ✅ | Closes 0.70130, 0.70093 — above threshold |
| ADX veto | D1 ADX>30 trending AGAINST the LONG fade | ❌ VETO | ADX 31.5>30 trending DOWN = against the LONG → HARD BLOCK |

→ ADX 31.5 > 30 with D1 trending DOWN = veto on COUNTER LONG.

## Q3 — Re-Forecast Check
No triggers for AUD (no DXY/US2Y macro gates). Action: NONE.

## Q4 — Entry Confluence
PRIMARY SHORT: no approach. COUNTER LONG: ADX veto before scoring.

## Result
❌ NO TRADE — PRIMARY SHORT 0.7065–0.7110: no zone approach (spot 0.70093, ~72 pips below floor). W25 closes today.
❌ NO TRADE — COUNTER LONG 0.6980–0.7000: D1 ADX 31.5 > 30 trending DOWN = hard veto against LONG fade. Spot also above zone top (0.70093 > 0.70000).

Note: W25 PRIMARY SHORT order expired 06-15 (recorded in trade table). Zone structurally intact but W25 window closing. W26 will reassess. ADX 31.5 borderline — if it retreats below 30 in W26 with compression, SHORT fade becomes viable again.
