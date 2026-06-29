---
type: daily_validation
date: 2026-06-08
week: 2026-W24
active_zone: PRIMARY | SECONDARY
v1_structure_intact: true
v1b_intact: true
v3_news_clear: true
vix_veto_short: false
vix_stale: false
reforecast_action: NONE
reforecast_triggers: []
e0_entry_confirmation: false
e1_h4h1_structure: true
e2_dfii10_slope: true
e3_macro_drift_ok: true
e4_atr_compressed: false
e5_dxy_slope: true
entry_confluence_score: 6.0
zone_confluence_score: 9.5
e0_pattern: none
anchor_type: zone_50pct
anchor_price: 4378.50
h4_atr: 48.86
d1_atr: 98.84
d1_atr_compressed: false
sl_distance: 49.14
offset: 39.31
order_limit: PLACED
limit_price: 4417.81
limit_direction: SELL
limit_expires: 2026-06-08 21:00 UTC
tp1_price: 4294.96
tp2_price: 4270.39
be_trigger_r: 1.5
dfii10_now: 2.110
dfii10_baseline: 2.110
dfii10_slope: 0.150
dxy_slope: 1.603
adx_val: 0.0
---

# Validation — 2026-06-08 (PRIMARY + SECONDARY zones from [[2026-W24]])

*Scheduled NY-session `/validate` run (data pulled 2026-06-08 13:20 UTC). Supersedes the 08:06 UTC London-session run. Both zones re-validated and limits recomputed on fresh bars.*

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | $4324.02 | falling — well below both SHORT zones |
| DFII10 | 2.11% | baseline 2.11%, drift 0.000% |
| DFII10 20d slope | +0.150 | pos = bearish (supports SHORT) |
| DXY 20d slope | +1.603 | pos = bearish (supports SHORT) |
| H4 ATR (trading) | $48.86 | down from $51.08 prior run |
| D1 ATR | $98.84 | median $98.59 → compressed? ❌ (98.84 > 98.59) |
| VIX | 15.40 | veto>35? no. stale? no |
| ADX(14) D1 | — | strong downtrend (visual: LH+LL on H4/D1) |

_Mon:_ Weekend gap minor / in-bias (gold continued lower) → note-only, no re-forecast.

## Q1+Q2 — Hard Blocks (all pass)
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone | ✅ | Last D1 close $4324.02 — below both zone tops ($4390 / $4485). Intact. |
| V1b | 2 consec H4 closes >$5 past zone | ✅ | Price far below zones; no breach above. |
| V3 | Hard news within 2h London/NY | ✅ | CPI is **Wed 06-10**, not today. No NFP/FOMC/CPI 06-08. |
| VETO | VIX>35 (fresh) → shorts | ✅ | VIX 15.40, fresh, no veto. |
| Macro flip | DFII10/DXY vs baseline | ✅ | DFII10 drift 0.000%; DXY ~99.9 vs 100.07 baseline — within band. |

## Q3 — Re-Forecast Check
Triggers fired: none (T1 DFII10 0 drift · T2 DXY drift small · T3 gold moved further in-bias, not counter · T4 no shock · T5 cumulative minimal) → action: **NONE**. Continue.

Macro context unchanged: BEARISH MEDIUM-HIGH, conviction HIGH. NFP-shock repriced cuts out; real yields rising, DXY firm near 100, Warsh-hawkish Fed. Gold at 2026 low. CPI Wed 06-10 = key bear-thesis risk (cool print → short-squeeze bounce — which is exactly what these resting SHORT limits are designed to sell into).

## Q4 — Entry Confluence (both zones identical macro → both 6.0/10)
| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| E0 | Entry confirmation | 3.0 | ❌ | Price $4324 far below zones; no 1H/15M confirmation at zone. |
| E1 | H4+H1 structure aligned | 2.5 | ✅ | H4 clean LH+LL downtrend (4476→4352→4338; lows 4335→4268). |
| E2 | DFII10 slope supports | 2.0 | ✅ | +0.150 (pos = supports SHORT). |
| E3 | Macro drift OK | 1.0 | ✅ | \|2.11 − 2.11\| = 0.000 < 0.10. |
| E4 | D1 ATR compressed | 1.0 | ❌ | 98.84 > median 98.59 — not compressed. |
| E5 | DXY slope supports | 0.5 | ✅ | +1.603 (pos = supports SHORT). |
| | **Total** | **6.0 / 10.0** | | ≥ 5.0, no E0 → midpoint anchor |

## Order Limit Calc
```
H4_ATR14       = $48.86 (trading-day filter)
0.5 × D1_ATR14 = $49.42
SL             = avg(49.42, 48.86) = $49.14   (0.5×D1 ≥ H4 → blended)
offset         = max(49.14/3=16.38, (10−6.0)×0.2×49.14=39.31) = $39.31
```
**PRIMARY** — zone $4367–$4390, midpoint anchor $4378.50:
```
limit  = 4378.50 + 39.31 = $4417.81
SL px  = 4417.81 + 49.14 = $4466.95
TP1 2.5R = $4294.96 (manual) | TP2 3.0R = $4270.39 (limit) | BE @1.5R = $4344.10
```
**SECONDARY** — zone $4450–$4485, midpoint anchor $4467.50:
```
limit  = 4467.50 + 39.31 = $4506.81
SL px  = 4506.81 + 49.14 = $4555.95
TP1 2.5R = $4383.96 (manual) | TP2 3.0R = $4359.39 (limit) | BE @1.5R = $4433.10
```

## Result
### ✅ ORDER LIMIT — PRIMARY
```
ORDER LIMIT: SELL $4417.81 | SL $4466.95 | TP1 2.5R $4294.96 (manual) | TP2 3.0R $4270.39 (limit) | BE @1.5R $4344.10 | expires 2026-06-08 21:00 UTC
Entry Confluence: 6.0/10 (E0:❌ E1:✅ E2:✅ E3:✅ E4:❌ E5:✅)
Anchor: 50% zone midpoint $4378.50 | SL $49.14 | offset $39.31 | R:R 3.0
"If price reaches $4417.81, order triggers. Cancel if not hit by 21:00 UTC."
```
### ✅ ORDER LIMIT — SECONDARY
```
ORDER LIMIT: SELL $4506.81 | SL $4555.95 | TP1 2.5R $4383.96 (manual) | TP2 3.0R $4359.39 (limit) | BE @1.5R $4433.10 | expires 2026-06-08 21:00 UTC
Entry Confluence: 6.0/10 (E0:❌ E1:✅ E2:✅ E3:✅ E4:❌ E5:✅)
Anchor: 50% zone midpoint $4467.50 | SL $49.14 | offset $39.31 | R:R 3.0
"If price reaches $4506.81, order triggers. Cancel if not hit by 21:00 UTC."
```

**Week status:** 2 zones open. 0 trades filled.
**⚠️ CPI Wed 2026-06-10 = HARD BLOCK (V3):** cancel any unfilled limit within 2h of London (08:00) / NY (13:00) open. Both limits rest well above spot ($4324) — fill only on a strong bounce into resistance.
