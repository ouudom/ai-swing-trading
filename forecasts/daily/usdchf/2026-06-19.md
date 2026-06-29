---
type: daily_validation
instrument: usdchf
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
zone_confluence_score: 8.5
e0_pattern: none
anchor_type: zone_50pct
anchor_price: 0.00
h4_atr: 0.00246
d1_atr: 0.00583
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
adx_val: 25.5
---

# Validation — 2026-06-19 (W25 Friday close)

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 0.80580 | — |
| DXY 20d slope | +1.646 | strong USD — WITH USDCHF bulls, against SHORT zone |
| H4 ATR | 0.00246 | — |
| D1 ATR | 0.00583 | median 0.00494 → EXPANDING |
| VIX | 18.44 | NO VIX VETO/SCORE for USDCHF (washout) |
| ADX(14) D1 | 25.5 | TRENDING (borderline) |

## Q1+Q2 — Hard Blocks

### PRIMARY SHORT 0.8005–0.8025
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close above 0.8042 (invalidation level) | ❌ BREACH | D1 close = 0.80580 > 0.8042 |
| V1b | 2 consec H4 closes above 0.80290 | ❌ BREACH | H4 closes: 0.80496, 0.80580 — both > threshold 0.80290 |

→ ❌ **INVALIDATED** — both V1 and V1b triggered. D1 close (0.80580) exceeded zone top (0.8025) AND invalidation level (0.8042). Price broke out above resistance — short thesis dead. Remove from _HOT.md.

> Note: DXY slope20 = +1.646 (strong uptrend) and D1 BOS UP @ 0.80152 on 06-18 confirm the breakout. The DXY 20d slope was the live macro for USDCHF — it has now reversed to strongly bullish USDCHF, confirming the short thesis no longer holds. SNB held rates on 06-18.

## Q3 — Re-Forecast Check
DXY slope flip: was falling (supported short), now +1.646 (strongly against short). This is a T5-style drift / T2-style DXY move. Re-forecast needed for W26: bias must flip to NEUTRAL or BULLISH USDCHF given DXY reversal. Action: WARN_LOG (end of W25, W26 weekly will address).

## Q4 — Entry Confluence
Zone invalidated. No scoring.

## Result
❌ INVALIDATED — PRIMARY SHORT 0.8005–0.8025: V1b breach (H4 closes 0.80496, 0.80580 both above threshold 0.80290) + V1 breach (D1 close 0.80580 > invalidation level 0.8042). Remove from tracking. W26 bias must reset — DXY slope reversal undermines the short thesis.
