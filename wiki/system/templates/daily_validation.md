---
type: system
updated: 2026-06-02
confidence: high
tags: [template, validation, daily]
related: [constitution, weekly_forecast]
---

# Daily Validation Template (v2)

File: `forecasts/daily/<instrument>/YYYY-MM-DD.md` — one per day, append-style. Claude writes
markdown directly (no DB). Runs 07:30 UTC before London open. Zone box/direction never change; Entry
Confluence + SL + offset + limit recompute daily. Instrument ∈ {xauusd, eurusd, gbpusd}.

The four questions: (1) forecast still valid? (2) bias flipped? (3) re-forecast? (4) order limit?

---

## Frontmatter
```yaml
---
type: daily_validation
instrument: xauusd | eurusd | gbpusd
date: YYYY-MM-DD
week: YYYY-WNN
active_zone: PRIMARY | SECONDARY | COUNTER | NONE
# Q1/Q2 hard blocks
v1_structure_intact: true | false
v1b_intact: true | false
v3_news_clear: true | false
vix_veto: true | false             # xauusd: VIX>35 blocks SHORTs | FX: VIX>35 or spike>3 blocks LONGs
vix_stale: true | false
# Q3 re-forecast
reforecast_action: NONE | WARN_LOG | REFORECAST_NOW
reforecast_triggers: []            # e.g. [T1, T3]
# Q4 entry confluence (max 10.0, floor 5.0) — E1–E5 meaning differs by instrument (see confluence_criteria R2)
e0_entry_confirmation: true | false   # 3.0  (xauusd: continuation | FX: reversal turn into zone)
e1: true | false                      # 2.5  xauusd H4 structure | FX oscillator still extreme
e2: true | false                      # xauusd 2.0 DFII10 slope | FX 1.5 band/H1 oscillator
e3: true | false                      # 1.0  xauusd macro drift | FX non-trend ADX<25
e4: true | false                      # 1.0  ATR compression (both) | FX structure/band intact
e5: true | false                      # xauusd 0.5 DXY slope | FX 1.0 compression holds
entry_confluence_score: 0.0
# Entry
zone_confluence_score: 0.0         # carried from weekly
e0_pattern: 1H_engulf | 1H_pin | 15M_choch | none
anchor_type: confirmation_close | zone_50pct
anchor_price: 0000.00
h4_atr: 00.00
d1_atr: 00.00
d1_atr_compressed: true | false
sl_distance: 0.00                  # v2: H4ATR floor, blended w/ 0.5×D1ATR only if 0.5×D1>H4
offset: 0.00                       # max(SL/3, (10−score)×0.2×SL)
order_limit: PLACED | NO_TRADE | INVALIDATED
limit_price: 0000.00
limit_direction: BUY | SELL | N/A
limit_expires: YYYY-MM-DD 21:00 UTC
tp1_price: 0000.00                 # 2.5R manual
tp2_price: 0000.00                 # 3.0R limit
be_trigger_r: 1.5
dfii10_now: 0.000
dfii10_baseline: 0.000
dfii10_slope: 0.000
dxy_slope: 0.000
adx_val: 00.0
---
```

---

## Body Skeleton
```markdown
# Validation — YYYY-MM-DD (<PRIMARY|SECONDARY|COUNTER> zone from [[YYYY-WNN]])

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | $xxxx.xx | — |
| DFII10 | x.xx% | baseline x.xx%, drift ±x.xxx% |
| DFII10 20d slope | x.xxx | neg=bullish / pos=bearish |
| DXY 20d slope | x.xxx | neg=bullish / pos=bearish |
| H4 ATR (trading) | $xx.xx | — |
| D1 ATR | $xx.xx | median $xx.xx → compressed? ✅/❌ |
| VIX | xx.xx | veto>35? stale? |
| ADX(14) D1 | xx.x | trending/transitional/ranging |

_Mon only:_ Weekend gap ±x.xxx% → noise / note / warning / re-forecast

## Q1+Q2 — Hard Blocks (any fail = stop)
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone | ✅/❌ | ❌ = INVALIDATED |
| V1b | 2 consec H4 closes >$5 past zone | ✅/❌ | ❌ = INVALIDATED, cancel limit |
| V3 | Hard news within 2h London/NY | ✅/❌ | ❌ = NO TRADE |
| VETO | VIX>35 (fresh) → shorts | ✅/❌ | VIX xx.xx |
| Macro flip | DFII10/DXY vs baseline | ✅/❌ | drift ±x.xxx% |

## Q3 — Re-Forecast Check
Triggers fired: <none / T1,T3...> → action: NONE / WARN_LOG / REFORECAST_NOW

## Q4 — Entry Confluence (max 10.0, floor 5.0)
| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| E0 | Entry confirmation (1H engulf / 1H pin / 15M CHoCH toward dir) | 3.0 | ✅/❌ | <pattern, time> |
| E1 | H4 structure aligned | 2.5 | ✅/❌ | |
| E2 | DFII10 slope supports | 2.0 | ✅/❌ | |
| E3 | Macro drift OK | 1.0 | ✅/❌ | ±x.xxx% |
| E4 | D1 ATR compressed | 1.0 | ✅/❌ | |
| E5 | DXY slope supports | 0.5 | ✅/❌ | |
| | **Total** | **x.x / 10.0** | | ≥ 5.0 to place |

## Order Limit Calc _(only if score ≥ 5.0)_
```
H4_ATR14       = $xx.xx (trading-day filter)
0.5 × D1_ATR14 = $xx.xx
SL             = H4_ATR if 0.5×D1 < H4 else avg(0.5×D1, H4) = $xx.xx
anchor         = <confirmation close $xxxx / 50% zone midpoint $xxxx>
offset         = max(SL/3, (10 − score) × 0.2 × SL) = $xx.xx
limit_price    = anchor − offset (long) | anchor + offset (short) = $xxxx.xx
SL price       = limit ± SL = $xxxx.xx
TP1 (2.5R)     = $xxxx.xx (manual) | TP2 (3.0R) = $xxxx.xx (limit) | BE @ +1.5R
```

## Result
### ✅ ORDER LIMIT _(score ≥ 5.0)_
```
ORDER LIMIT: BUY/SELL $xxxx.xx | SL $xxxx.xx | TP1 2.5R $xxxx (manual) | TP2 3.0R $xxxx (limit) | BE @1.5R | expires 21:00 UTC
Entry Confluence: x.x/10 (E0:✅ E1:✅ E2:✅ E3:✅ E4:✅ E5:✅)
Anchor: <confirmation close / 50% zone> | SL $xx.xx | offset $xx.xx | R:R x.xx
"If price reaches $xxxx.xx, order triggers. Cancel if not hit by 21:00 UTC."
```
### ❌ NO TRADE
```
NO TRADE — [hard block / score x.x < 5.0]: <reason>
[INVALIDATED if V1/V1b fail — remove from _HOT.md]
```
```

---

## Rules
- First hard block fail → stop, output NO TRADE/INVALIDATED, note which.
- No E0 confirmation but score ≥ 5.0 → ORDER LIMIT anchored at 50% zone midpoint.
- 15M CHoCH must break structure in the zone's direction — against-direction CHoCH does not count.
- SL/offset/limit recompute daily. TP anchor fixed from weekly. Order expires 21:00 UTC.
- Validate every PENDING zone independently.
