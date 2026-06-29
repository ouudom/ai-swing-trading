---
type: daily_validation
instrument: xauusd
date: 2026-06-25
week: 2026-W26
active_zone: PRIMARY, SECONDARY
v1_structure_intact: true
v1b_intact: true
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
e5: true
entry_confluence_score: 6.0
zone_confluence_score: 8.5
e0_pattern: none
anchor_type: midpoint
anchor_price: 4320.00
h4_atr: 44.81
d1_atr: 130.79
d1_atr_compressed: false
sl_distance: 55.10
offset: 44.08
order_limit: ORDER_LIMIT
limit_price: 4364.08
limit_direction: SHORT
limit_expires: 2026-06-25T21:00Z
tp1_price: 4226.33
tp2_price: 4198.78
be_trigger_r: 1.5
---

# Validation — 2026-06-25 (PRIMARY + SECONDARY SHORT zones from [[2026-W26]])
*Automated run 10:13 UTC (V3-blocked) · Updated 13:40 UTC (V3 cleared post-PCE/GDP)*

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | $4015.01 | — |
| DFII10 | 2.29% | baseline 2.23; 20d slope +0.19 → bearish drift intact |
| DXY 20d slope | +2.282 | positive — no sign flip vs baseline (+1.65) |
| DXY 1d jump | −0.118 | USD softened on PCE data (DXY reversal, < 0.5 no block) |
| H4 ATR (trading) | $44.81 | — |
| D1 ATR | $130.79 | median $111.96 → EXPANDING ❌ |
| VIX | 18.63 (2026-06-24) | stale but <35; spike −0.86 |
| ADX(14) D1 | 47.4 | TRENDING — continuation bias intact |

## Q1+Q2 — Hard Blocks
| | Block | Result | Note |
|---|---|---|---|
| V1 (PRIMARY) | D1 close above zone top 4235 | ✅ | close $4010.20 — not above zone |
| V1b (PRIMARY) | 2 H4 closes above 4240 | ✅ | last H4 closes 3980.17 / 4015.01 |
| V1 (SECONDARY) | D1 close above zone top 4340 | ✅ | clear |
| V1b (SECONDARY) | 2 H4 closes above 4345 | ✅ | clear |
| V3 | PCE + GDP @ 12:30 UTC ±30min window | ✅ CLEARED | event released 12:30; no-trade ±30min = 12:00–13:00; now 13:40 UTC |
| VETO | VIX>35 → all SHORTs | ✅ | VIX 18.63, stale but well below threshold |
| Macro flip | DFII10 drift |2.29−2.23|=0.06 < 0.15% | ✅ | no re-forecast |

PCE data (released 12:30 UTC): Core PCE annual 3.4% (as anticipated). GDP final 2.1%. USD softened on "meets expectations" read — DXY −0.118 today.

## Q3 — Re-Forecast Check
- T1 (DFII10 drift): 0.06 < 0.15 → NO
- T2 (DXY 1d jump): −0.118 < 0.5 → NO
- T3 (counter-move): price at 4015 vs week open 4172 = −3.8% — BELOW 2.5% in BEARISH direction (continuation) → NO
- T5 (cumulative drift): DGS2 4.16 vs baseline 4.20 = −0.04 → NO
**Action: NONE.**

## Q4 — Entry Confluence

### PRIMARY SHORT (4200–4235) — EC 6.0/10
| # | Signal | Score | Note |
|---|---|---|---|
| E0 | Entry confirm (1H engulf/pin/CHoCH toward SHORT) | 0 | No trigger; spot 4015 far below zone |
| E1 | H4 LH+LL structure | 2.5 ✅ | H4 BOS DOWN, state DOWN; LH+LL confirmed |
| E2 | DFII10 slope still supports (>0 for SHORT) | 2.0 ✅ | slope +0.19 → bearish signal intact |
| E3 | Macro drift OK (\|DFII10−baseline\|<0.10) | 1.0 ✅ | 0.06 < 0.10 |
| E4 | ATR compressed | 0 ❌ | D1 ATR 130.79 > median 111.96 — expanding |
| E5 | DXY slope supports (>0 for SHORT) | 0.5 ✅ | 20d slope +2.282 — still rising |
| **Total** | | **6.0/10** | ≥ 5.0 floor → ORDER LIMIT |

> [!note] Zone already triggered WIN_TP1 this week (fill ~4210 Mon Jun 22, trade replay). Setting ORDER LIMIT as second-touch opportunity; operator may choose to skip. Resting SELL LIMIT 4261.58 requires ~246pt rally from 4015.

### SECONDARY SHORT (4300–4340) — EC 6.0/10
| # | Signal | Score | Note |
|---|---|---|---|
| E0 | Entry confirm | 0 | Spot far below zone |
| E1 | H4 LH+LL | 2.5 ✅ | same as PRIMARY |
| E2 | DFII10 slope | 2.0 ✅ | same |
| E3 | Macro drift OK | 1.0 ✅ | same |
| E4 | ATR compressed | 0 ❌ | same |
| E5 | DXY slope | 0.5 ✅ | same |
| **Total** | | **6.0/10** | ≥ 5.0 → ORDER LIMIT |

W26 high 4216.38 < zone bottom 4300 — zone has NOT been touched this week. Clean setup.

## Result

**PRIMARY SHORT (4200–4235):**
```
⚠ ORDER LIMIT: SELL 4261.58 | SL 4316.68 | TP1 2.5R 4123.83 (manual) | TP2 3.0R 4096.28 (limit) | BE @1.5R | expires 2026-06-25 21:00 UTC
Entry Confluence: 6.0/10 (E0:❌ E1:✅ E2:✅ E3:✅ E4:❌ E5:✅)
Anchor: 50% zone midpoint 4217.50 | SL 55.10 | offset 44.08
NOTE: Zone already WIN_TP1 this week (replay). Second-touch; operator discretion.
```

**SECONDARY SHORT (4300–4340):**
```
✅ ORDER LIMIT: SELL 4364.08 | SL 4419.18 | TP1 2.5R 4226.33 (manual) | TP2 3.0R 4198.78 (limit) | BE @1.5R | expires 2026-06-25 21:00 UTC
Entry Confluence: 6.0/10 (E0:❌ E1:✅ E2:✅ E3:✅ E4:❌ E5:✅)
Anchor: 50% zone midpoint 4320.00 | SL 55.10 | offset 44.08
Zone untouched this week (W26 high 4216 < 4300). Clean first-touch opportunity.
```

---
*Updated 14:13 UTC — Hourly re-validation. Both ORDER LIMITs HELD (D032 anchor lock until 17:51 UTC).*

Spot 4018.27 (14:00 bar). All gates intact: V1b clear (H4 closes 3980/4018 vs thresholds 4240/4345), V3 cleared (PCE/GDP released 12:30), VIX 18.63, DFII10 drift 0.06% < 0.15%. EC 6.0 unchanged. DXY 20d slope +2.373 (positive). DB corruption note: `news`/`ohlc` table-count pages malformed — OHLC instrument reads intact, indicators unaffected; trade_outcome.py replay partial (crashed on eurgbp D1 page). Live fills from cached table: 7 filled (2 running).

> [!note] Anchor locked until 17:51 UTC (EC 6.0) — resting SELL 4364.08 (SECONDARY) + SELL 4261.58 (PRIMARY) unchanged.

---
*Updated 15:11 UTC — Hourly re-validation. Both ORDER LIMITs HELD (D032 anchor lock until 17:51 UTC).*

Spot 4017.22 (H4 close 12:00 / H1 15:00 bar). All gates intact: V1b clear (H4 closes 3980.17/4017.22 vs thresholds 4240/4345), V3 cleared, VIX 18.63, DFII10 2.29% drift 0.06% < 0.15%, DXY 20d slope +2.361 (positive). EC 6.0 unchanged — HOLD confirmed by ledger for both zones. CB calendar clear, no events remainder of session.

> [!note] Anchor locked until 17:51 UTC (EC 6.0) — resting SELL 4364.08 (SECONDARY) + SELL 4261.58 (PRIMARY) unchanged.
