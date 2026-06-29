---
type: daily_validation
instrument: nzdusd
date: 2026-06-19
week: 2026-W25
active_zone: NONE
v1_structure_intact: true
v1b_intact: false
v3_news_clear: true
vix_veto: false
vix_stale: true
reforecast_action: NONE
reforecast_triggers: []
e0_entry_confirmation: false
e1: true
e2: true
e3: true
e4: false
e5: false
entry_confluence_score: 5.0
zone_confluence_score: 6.5
e0_pattern: none
anchor_type: zone_50pct
anchor_price: 0.00
h4_atr: 0.00211
d1_atr: 0.00550
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
adx_val: 22.4
---

# Validation — 2026-06-19 (W25 Friday close)

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 0.57494 | — |
| DGS2 | 4.20% | context only (dead for NZD) |
| H4 ATR | 0.00211 | — |
| D1 ATR | 0.00550 | median 0.00551 → COMPRESSED ✅ (borderline) |
| VIX | 18.44 | stale (06-17); NO VIX VETO for NZD |
| ADX(14) D1 | 22.4 | TRANSITIONAL → floor raised to 6.5 |

## Q1+Q2 — Hard Blocks

### PRIMARY SHORT 0.5855–0.5890
| | Block | Result | Note |
|---|---|---|---|
| V1b | 2 consec H4 closes above 0.58940 | ✅ | Closes 0.57557, 0.57494 — far below zone |

No approach (spot 0.57494, ~360 pips below zone floor).

### COUNTER LONG 0.5750–0.5790
| | Block | Result | Note |
|---|---|---|---|
| V1b | 2 consec H4 closes below 0.57460 | ❌ **BREACH** | H4 00:00 close 0.57369, H4 04:00 current 0.57256 — both below threshold 0.57460 |

> [!warning] **V1b INVALIDATED @ 05:11 UTC** — check_v1b.py exit 2. H4 00:00 closed at 0.57369 (confirmed). H4 04:00 bar currently at 0.57256 (bar closes 08:00 UTC). Price 20+ pips below threshold with D1/H4 state DOWN; recovery before bar close very unlikely. Zone removed from active tracking.

## Q4 — Entry Confluence — COUNTER LONG 0.5750–0.5790

| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| E0 | 1H reversal confirm (LONG turn) | 3.0 | ❌ | SHORT engulf fired; no LONG confirm |
| E1 | H4 oscillator still extreme (OVERSOLD) | 2.5 | ✅ | H4 Stoch 7.4, W%R -92.9, CCI -125.4 all OVERSOLD |
| E2 | H4 band touch (long) | 1.5 | ✅ | H4 close 0.57494 ≤ Donchian lower 0.57490 |
| E3 | Non-trending ADX<25 | 1.0 | ✅ | ADX 22.4 < 25 |
| E4 | Squeeze/compression holds | 1.0 | ❌ | TTM squeeze OFF (NZD's strongest signal absent) |
| E5 | Structure intact | 1.0 | ❌ | D1 BOS DOWN @ 0.57703 (06-18); H4 DOWN — bearish structure |
| | **Total** | **10.0** | **5.0/10** | |

Score = 5.0. Floor = **6.5** (transitional ADX 22.4 per pull guidance). 5.0 < 6.5 → NO TRADE.

## Q3 — Re-Forecast Check
No macro gates for NZD. D1 BOS DOWN 06-18 is a price trigger but only T3 (1.5% counter-move) or T4 shock force re-forecast. D1 drop ~1.0% from W25 high — below threshold. Action: NONE.

## Result
❌ NO TRADE — PRIMARY SHORT 0.5855–0.5890: no zone approach. W25 closes today.
❌ **INVALIDATED** — COUNTER LONG 0.5750–0.5790: V1b breach @ 05:11 UTC (H4 00:00 @ 0.57369 + H4 04:00 @ 0.57256, both below threshold 0.57460). Zone removed. W25 closes with 0 order limits and 5 total invalidations (eurusd PRIMARY LONG, gbpusd COUNTER LONG, eurgbp SECONDARY SHORT, usdchf PRIMARY SHORT + nzdusd COUNTER LONG).
