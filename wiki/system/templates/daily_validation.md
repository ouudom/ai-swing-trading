---
type: system
updated: 2026-05-24
confidence: high
tags: [template, validation, daily]
related: [constitution, weekly_forecast]
---

# Daily Validation Template

File: `forecasts/daily/YYYY-MM-DD.md` — one per day, append-style.
Runs 07:30 UTC before London open. Setup params (zone/score/TP anchor) never change — stop_distance + entry_offset + limit_price + SL + lots recompute daily.

---

## Frontmatter

```yaml
---
type: daily_validation
date: YYYY-MM-DD
week: YYYY-WNN
active_setup: A | B | C | NONE
# Hard blocks
v1_structure_intact: true | false
v3_news_clear: true | false
g4_session: true | false
# Validation score
g1_mtf_structure: true | false   # 3.5 pts
g3_dfii10_slope: true | false    # 3.5 pts
g2_atr_compressed: true | false  # 2.0 pts
v2_macro_drift: true | false     # 1.0 pts
validation_score: 0.0            # max 10.0
# Entry
h1_trigger_present: true | false
weekly_confluence_score: 0.0
stop_distance: 0.00      # avg of three
entry_offset: 0.00       # (10 − score) × 0.2 × stop_distance, OUTWARD
order_limit: PLACED | WATCH | NO_TRADE | INVALIDATED
limit_price: 0000.00
limit_direction: BUY | SELL | N/A
limit_expires: YYYY-MM-DD 21:00 UTC
h4_atr: 00.00
d1_atr: 00.00
d1_atr_compressed: true | false
dfii10_slope: 0.000
dfii10_drift: 0.000
---
```

---

## Body Skeleton

```markdown
# Validation — YYYY-MM-DD (Setup <A|B|C> from [[YYYY-WNN]])

## Market Snapshot

| | Value | vs Baseline |
|---|---|---|
| Spot | $xxxx.xx | — |
| DFII10 | x.xx% | baseline x.xx%, drift ±x.xxx% |
| DXY | xxx.x | baseline xxx.x |
| H4 ATR | $xx.xx | — |
| D1 ATR | $xx.xx | median $xx.xx → compressed? ✅/❌ |
| DFII10 20d slope | x.xxx | negative=bullish / positive=bearish |

_Mon only:_ Weekend gap ±x.xxx% → noise / note / warning / re-forecast

## Hard Blocks (any fail = stop)

| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone | ✅/❌ | ❌ = INVALIDATED, remove setup |
| V3 | Hard news within 2h London/NY open | ✅/❌ | ❌ = NO TRADE, cancel limits |
| G4 | Session 08:00–17:00 UTC | ✅/❌ | always ✅ at 07:30 |

## Validation Score (max 10.0)

| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| G1 | H4+H1 structure aligned | 3.5 | ✅/❌ | |
| G3 | DFII10 slope supports direction | 3.5 | ✅/❌ | Setup C: always ✅ |
| G2 | D1 ATR compressed (< 20d median) | 2.0 | ✅/❌ | |
| V2 | DFII10 drift < 0.10% against direction | 1.0 | ✅/❌ | drift ±x.xxx% |
| | **Total** | **x.x / 10.0** | | ≥ 6.0 to proceed |

## H1 Trigger

H1 pin bar / engulfing / B&R inside zone? **YES / NO** — <one line description>
_(Confirmation only — does not change weekly score or offset)_

## Order Limit Calc _(only if score ≥ 6.0)_

```
structural_dist = last pivot low/high within 20 H4 bars = $xx.xx
H4_ATR14        = $xx.xx (trading-day filter: range>=$1)
0.5 × D1_ATR14  = $xx.xx
stop_distance   = avg(0.5×D1_ATR, H4_ATR, structural_dist) = $xx.xx     ← arithmetic mean
cap check       = structural_dist $xx.xx < 3 × H4_ATR $xx.xx? ✅/❌

entry_offset    = (10 − score) × 0.2 × stop_distance = $xx.xx
limit_price     = zone_top + offset (short) | zone_bottom − offset (long)   ← OUTWARD
SL              = limit_price ± stop_distance = $xxxx.xx
TP              = $xxxx.xx (locked from weekly — = x.xR)
lots            = $2000 / ($xx.xx × 100) = x.xx → x.xx lots
```

## Result

### ✅ ORDER LIMIT _(score ≥ 6.0 + H1 trigger present)_
```
ORDER LIMIT: BUY/SELL $xxxx.xx | x.xx lots | SL $xxxx.xx | TP $xxxx.xx | expires 21:00 UTC
Validation: x.x/10  (G1:✅ G2:✅ G3:✅ V2:✅) | H1 trigger: ✅
Stop: $xx.xx [structural / d1_floor / h4_floor / fallback] | Risk: $2,000 | R:R x.xx
"If price reaches $xxxx.xx, order triggers. Cancel if not hit by 21:00 UTC."
```

### 👁 WATCH _(score ≥ 6.0, no H1 trigger)_
```
WATCH — x.x/10  (G1:✅ G2:✅ G3:✅ V2:✅)
"Await H1 pin bar / engulfing / B&R inside $xxxx–$xxxx. If trigger forms before 17:00 UTC → set limit at $xxxx.xx."
```

### ❌ NO TRADE
```
NO TRADE — [hard block / score x.x < 6.0]: <specific reason>
[INVALIDATED if V1 fail — remove from _HOT.md]
```
```

---

## Rules
- First gate/check fail → stop, output NO TRADE, note which gate
- V1 fail = setup invalidated → remove from _HOT.md (not just HOLD)
- Limit price = zone_extreme + outward_offset (recomputed daily via (10−score)×0.2×stop_distance). stop_distance/SL/lots recompute daily. TP anchor never changes.
- Order expires 21:00 UTC — never carry forward
- Multiple setups: validate independently, observe $4000/week cap
