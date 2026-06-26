---
type: daily_validation
instrument: usdchf
date: 2026-06-25
week: 2026-W26
active_zone: PRIMARY, COUNTER
v1_structure_intact: true
v1b_intact: true
v3_news_clear: false
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
zone_confluence_score: 5.0
e0_pattern: none
anchor_type: N/A
anchor_price: 0.00
h4_atr: 0.00166
d1_atr: 0.00533
d1_atr_compressed: false
sl_distance: 0.00
offset: 0.00
order_limit: NO_TRADE
limit_price: 0.00
limit_direction: N/A
limit_expires: N/A
tp1_price: 0.00
tp2_price: 0.00
be_trigger_r: 1.5
---

# Validation — 2026-06-25 (PRIMARY LONG + COUNTER SHORT zones from [[2026-W26]])
*Automated run 10:14 UTC*

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 0.81187 | — |
| DGS2 | 4.16% | baseline 4.20%, drift −0.04% (polarity FLIPPED for usdchf) |
| DXY 20d slope | +2.538 | positive = USD-bullish = aligned with LONG usdchf |
| DXY 1d jump | −0.052 | anti-jump (DXY fade = slight usdchf fade) |
| H4 ATR (trading) | 0.00166 | — |
| D1 ATR | 0.00533 | median 0.00524 → EXPANDING ❌ |
| VIX | 19.49 (2026-06-23) | stale · no VIX row for usdchf |

Note: Yesterday's session flagged COUNTER SHORT hard-blocked (ADX 30.8). V3 window applies today regardless.

## Q1+Q2 — Hard Blocks
| | Block | Result | Note |
|---|---|---|---|
| V1 (PRIMARY LONG) | D1 close below 0.798 | ✅ | close 0.81263 — above zone, not breached |
| V1b (PRIMARY LONG) | 2 H4 closes below 0.79760 | ✅ | last H4 closes 0.81147/0.81187 |
| V1 (COUNTER SHORT) | D1 close above 0.813 | ✅ | close 0.81263 — inside zone |
| V1b (COUNTER SHORT) | 2 H4 closes above 0.81340 | ✅ | last closes 0.81147/0.81187 |
| **V3** | **Core PCE m/m + Final GDP @ 12:30 UTC** | **❌ BLOCK** | **within 2h of 13:00 NY open** |
| Macro flip | DXY slope20 +2.538 (same sign) | ✅ | no sign flip |

## Q3 — Re-Forecast Check
DGS2 drift −0.04% from 4.20 (FLIPPED polarity → falling DGS2 = slight USD-weak, but < threshold).
DXY slope20 +2.538: positive, no sign-flip → COUNTER SHORT not re-forecasted despite weak DXY drift.
**Action: NONE.**

## Q4 — Entry Confluence
Not scored — V3 event window hard block.

## Result

**PRIMARY LONG (0.798–0.801):**
```
NO TRADE — V3 EVENT WINDOW: Core PCE m/m + Final GDP q/q @ 12:30 UTC. Zone unreached (spot 0.81187 above zone 0.798–0.801). PENDING.
```

**COUNTER SHORT (0.809–0.813):**
```
NO TRADE — V3 EVENT WINDOW: Core PCE m/m + Final GDP q/q @ 12:30 UTC. Note: spot 0.81187 is inside zone. Additional block from 06-24: D1 ADX reading 30.8 (trending against fade) — verify today's ADX once event clears. PENDING.
```


---
*Updated 13:40 UTC — V3 cleared (PCE/GDP 12:30 released). Re-scored.*

**PRIMARY LONG (0.7980–0.8010) — EC 2.5/10:**
E0 ❌ · E1 ❌ H1 RSI 52 neutral · E2 ✅ DXY slope +2.282 · E3 ❌ TTM squeeze off · E4 ❌ ADX 32.7 · E5 ✅ structure intact
❌ NO TRADE — spot 0.81086 ~100pp ABOVE zone; pair in strong uptrend (D1 BOS UP, ADX 32.7). Zone unreachable this session.

**COUNTER SHORT (0.8090–0.8130) — EC 1.0/10:**
E0 ❌ · E1 ❌ H1 RSI 52 (not OB; need >65/W%R>−20) · E2 ❌ DXY slope AGAINST short · E3 ❌ · E4 ❌ ADX 32.7 · E5 ✅ structure intact
Note: D1 massively OB (RSI 72.4/Stoch 96.0/W%R −4.9) and above Keltner — SHORT thesis lives but H1 not at extreme and DXY works against. Score 1.0/10.
❌ NO TRADE — EC below floor and DXY aligned against.
