---
type: daily_validation
instrument: gbpjpy
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
e3: false
e4: true
e5: true
entry_confluence_score: 2.0
zone_confluence_score: 6.0
e0_pattern: none
anchor_type: N/A
anchor_price: 0.00
h4_atr: 0.396
d1_atr: 1.211
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

# Validation — 2026-06-25 (PRIMARY LONG zone from [[2026-W26]])
*Automated run 10:14 UTC*

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 213.203 | — |
| SONIA (context) | 3.729% | baseline 3.729 — stable (macro dead for gbpjpy) |
| H4 ATR (trading) | 0.396 | — |
| D1 ATR | 1.211 | median 0.95 → EXPANDING ❌ |
| VIX | 19.49 (2026-06-23) | stale · no VIX row for gbpjpy |
| ADX(14) D1 | 15.5 | RANGING ✅ |
| MoF watch | ACTIVE (Katayama 06-19) | spot 213.203 < 214 → CAUTION band (cap LONG MEDIUM) |

US events: PCE+GDP @ 12:30 UTC = CAUTION ONLY for gbpjpy (no USD leg). Moot — EC below floor.

## Q1+Q2 — Hard Blocks
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close below 212.0 | ✅ | close 212.976 — above zone bottom |
| V1b | 2 H4 closes below 211.950 | ✅ | last H4 closes 213.342/213.203 |
| V3 | BoJ/MoF decision or BoE decision | ✅ clear | jawboning regime active (caution) |
| MoF intervention | spot 213.203 vs 214 hard-block level | ✅ CAUTION | <214 = caution, cap MEDIUM; ≥214 = hard-block |

## Q3 — Re-Forecast Check
No T3 counter-move (>1.5%) — spot still above zone, ranging. T4 no shock.
**Action: NONE.**

## Q4 — Entry Confluence (PRIMARY LONG 212.0–212.9)
Spot 213.203 — above zone (zone not reached from above for a LONG entry).

| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| E0 | 1H RSI-reclaim/band-reclaim toward LONG | 3.0 | ❌ | LONG-confirm: none. SHORT-confirm: band-reclaim (Keltner-high re-entry). Instrument rule: E0 absent → no order. |
| E1 | Washout still present (Keltner-low/RSI<35/20d low) | 2.5 | ❌ | D1 RSI 42.7, H4 Stoch 36.7 — no washout readings; price above zone |
| E2 | Session: 12–16 UTC LONG (t=4.20) | 1.5 | ❌ | Current time 10:13 UTC (outside 12–16 window) |
| E3 | H1 timing structure (inside-bar break/near 20d low) | 1.0 | ❌ | Price not in zone |
| E4 | Zone structure intact | 1.0 | ✅ | V1b confirmed; D1 Donchian low 212.486 near zone |
| E5 | Not extended (ADX<25) | 1.0 | ✅ | D1 ADX 15.5 |
| | **Total** | **2.0/10** | | **< 5.0 floor + E0 absent rule** |

MoF CAUTION: even if EC met, conviction capped MEDIUM (spot 213.203 < 214).
Replay note: trade_outcome shows gbpjpy LONG RUNNING +0.9R (zone touched via D1 low 212.565 earlier this week).

## Result

**PRIMARY LONG (212.0–212.9):**
```
NO TRADE — EC 2.0/10 (< 5.0 floor): E0 absent (no LONG-confirm fired); washout readings not present at H1; price not at zone (spot 213.203 above zone). Instrument rule: E0 absent → no order. MoF CAUTION active (cap MEDIUM). Zone remains PENDING.
```


---
*Updated 13:40 UTC. MoF CAUTION (spot 213.498, band 210–214). Re-scored.*

**PRIMARY LONG (212.00–212.90) — E0 absent → NO ORDER (gbpjpy rule):**
Spot 213.498, zone 212.00–212.90. H1 dipped to 212.916 (low 11:00 bar) — 1.6pp above zone top 212.90.
Engulf fired (12:00 bull) but price did NOT clearly enter the zone.
gbpjpy E0 mandatory ("E0 absent → no order"). No valid zone entry confirmation.
E1 partial ✅ (D1 W%R −84.3 OVERSOLD) · E2 ✅ (12–16 UTC window) · E4 ✅ · E5 ✅ (ADX 15.5)
❌ NO TRADE — E0 absent; price bounced from just above the zone without a confirmed entry close inside.
MoF CAUTION: spot in intervention band 210–214 (cap MEDIUM on any future LONG).
ZONE RUNNING in trade_outcome: filled Wed Jun 24 14:00 @ 212.711, RUNNING +1.43R.
