---
type: daily_validation
instrument: gbpusd
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
h4_atr: 0.00243
d1_atr: 0.00877
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

# Validation — 2026-06-25 (PRIMARY SHORT + COUNTER LONG zones from [[2026-W26]])
*Automated run 10:13 UTC*

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 1.31762 | — |
| DGS2 | 4.16% | baseline 4.20%, drift −0.04% (<0.15 threshold) |
| DXY 1d jump | −0.052 | against SHORT zone (GBPUSD = USD-quote; DXY down → slight LONG tilt) |
| DXY 20d slope | +2.538 | USD-bull trend intact |
| H4 ATR (trading) | 0.00243 | — |
| D1 ATR | 0.00877 | median 0.00754 → EXPANDING ❌ |
| VIX | 19.49 (2026-06-23) | stale · spike +2.21 (<3 veto threshold) |

## Q1+Q2 — Hard Blocks
| | Block | Result | Note |
|---|---|---|---|
| V1 (PRIMARY SHORT) | D1 close beyond 1.338 | ✅ | close 1.31657 — below zone, not breached |
| V1b (PRIMARY SHORT) | 2 H4 closes above 1.34210 | ✅ | last closes 1.31845/1.31762 |
| V1 (COUNTER LONG) | D1 close below 1.314 | ✅ | close 1.31657 — inside zone |
| V1b (COUNTER LONG) | 2 H4 closes below 1.31340 | ✅ | last closes 1.31845/1.31762 |
| **V3** | **Core PCE m/m + Final GDP @ 12:30 UTC** | **❌ BLOCK** | **within 2h of 13:00 NY open** |
| VETO | VIX spike >3 → LONG blocks | ✅ (spike 2.21) | stale; spike below threshold |
| Macro flip | DGS2 drift −0.04% | ✅ | <0.15% threshold |

## Q3 — Re-Forecast Check
DGS2 4.16 vs baseline 4.20: drift −0.04% (< threshold). DXY slope20 +2.538 (positive, no flip).
**Action: NONE.**

## Q4 — Entry Confluence
Not scored — V3 event window hard block.

## Result

**PRIMARY SHORT (1.338–1.3415):**
```
NO TRADE — V3 EVENT WINDOW: Core PCE m/m + Final GDP q/q @ 12:30 UTC. Zone unreached (spot 1.31762 vs zone 1.338). PENDING.
```

**COUNTER LONG (1.314–1.320):**
```
NO TRADE — V3 EVENT WINDOW: Core PCE m/m + Final GDP q/q @ 12:30 UTC. Note: spot 1.31762 is inside zone (replay shows RUNNING fill at +0.0R). Event window prevents new limit placement; existing replay fill continues per trade_outcome.py.
```


---
*Updated 13:40 UTC — V3 cleared (PCE/GDP 12:30 released). Re-scored all zones.*

**PRIMARY SHORT (1.3380–1.3415) — EC 1.0/10:**
E0 ❌ · E1 ❌ D1 OVERSOLD (Stoch 14.8/W%R −93.0/CCI −171.4), not at short extreme · E3 ❌ ADX 25.5 · E4 ✅ band intact · Others ❌
❌ NO TRADE — spot 1.31956 ~150pp below zone; D1 oscillators deeply oversold, not the short condition.

**COUNTER LONG (1.3140–1.3200) — EC 6.5/10 — ZONE RUNNING:**
E0 ✅ bull engulf 12:00 close 1.31760 · E1 ✅ D1 oversold extreme · E2 ❌ H1 neutral · E3 ❌ ADX 25.5 · E4 ✅ band intact
❌ NO TRADE — zone RUNNING (trade_outcome: filled Thu Jun 24 08:00 @ 1.31755, +0.58R live). No duplicate entry.
