---
type: daily_validation
instrument: eurgbp
date: 2026-06-25
week: 2026-W26
active_zone: PRIMARY
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
e3: true
e4: true
e5: false
entry_confluence_score: 2.0
zone_confluence_score: 8.0
e0_pattern: none
anchor_type: N/A
anchor_price: 0.00
h4_atr: 0.00117
d1_atr: 0.00272
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

# Validation — 2026-06-25 (PRIMARY SHORT zone from [[2026-W26]])
*Automated run 10:14 UTC*

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 0.86184 | — |
| EUR−GBP rate diff | −1.479 | baseline −1.479 (stable) |
| Rate diff 20d slope | +0.25 | EUR−GBP narrowing (weak EUR-bullish tilt) |
| H4 ATR (trading) | 0.00117 | — |
| D1 ATR | 0.00272 | median 0.00261 → EXPANDING ❌ |
| VIX | 19.49 (2026-06-23) | stale · no VIX veto for eurgbp |
| ADX(14) D1 | 15.6 | RANGING ✅ (< 25) |

US events note: PCE+GDP @ 12:30 UTC = CAUTION ONLY for eurgbp (no USD leg). Forward-carry case applies: if ORDER LIMIT issued, flatten_time = 11:30 UTC. Moot — EC below floor (see below).

## Q1+Q2 — Hard Blocks
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close above 0.8715 | ✅ | close 0.86247 — below zone, not breached |
| V1b | 2 H4 closes above 0.87190 | ✅ | last H4 closes 0.86144/0.86184 |
| V3 | ECB/BoE decisions or EZ/UK tier-1 | ✅ clear | US events = caution only |
| VETO | D1 ADX>30 against fade | ✅ | ADX 15.6 |
| Macro flip | Rate diff stable | ✅ | macro = tilt only (EG2) |

## Q3 — Re-Forecast Check
Rate diff slope +0.25 (gradual EUR narrowing) — tilt context only, not a gate. No T3 counter-move.
**Action: NONE.**

## Q4 — Entry Confluence (PRIMARY SHORT 0.8682–0.8715)
Spot 0.86184 — below zone (zone not reached).

| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| E0 | 1H pin/engulf/band-reclaim toward SHORT | 3.0 | ❌ | SHORT-confirm: none fired. LONG-confirm active (stoch-reclaim, bull pin). |
| E1 | D1 oscillator SHORT extreme (RSI>65/CCI>+100/Stoch>80) | 2.5 | ❌ | D1 RSI 42.9, Stoch 17.7, CCI −108.3 — OVERSOLD, opposite side |
| E2 | H1 oscillator SHORT extreme (RSI>65/Stoch>80) | 1.5 | ❌ | H1 RSI 43, Stoch 25 — not overbought |
| E3 | Non-trending ADX<25 | 1.0 | ✅ | D1 ADX 15.6 |
| E4 | Zone structure intact (20d extreme/band not broken) | 1.0 | ✅ | Donchian upper 0.8682 = zone bottom; zone at top of recent range; intact |
| E5 | D1 ATR<20-day median | 1.0 | ❌ | D1 ATR 0.00272 > median 0.00261 (expanding) |
| | **Total** | **2.0/10** | | **< 5.0 floor** |

D1 oscillators are reading OVERSOLD (bullish territory) — eurgbp is currently at the bottom of its range, not the top. The SHORT zone (0.8682–0.8715) requires price to rally to resistance with D1 overbought readings. Conditions not present.

## Result

**PRIMARY SHORT (0.8682–0.8715):**
```
NO TRADE — EC 2.0/10 (< 5.0 floor): D1 oscillators oversold (RSI 42.9, Stoch 17.7, CCI −108.3) — opposite of SHORT extreme. No E0 confirm. Zone unreached (spot 0.86184 below 0.8682). Zone remains PENDING.
```


---
*Updated 13:40 UTC — V3 cleared (cross pair, US events caution-only). Re-scored.*

**PRIMARY SHORT (0.8682–0.8715) — EC 2.0/10:**
E0 ❌ spot 0.86129 ~52pp below zone · E1 ❌ D1 Stoch 17.7 OVERSOLD (need OB for SHORT) · E2 ❌ H1 neutral · E3 ✅ ADX 15.6 · E4 ✅ band intact · E5 ❌ ATR expanding
❌ NO TRADE — D1 oscillators deeply oversold; far from zone. Score 2.0/10 unchanged from 10:14 run.
