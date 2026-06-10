---
type: daily_validation
instrument: eurusd
date: 2026-06-10
week: 2026-W24
active_zone: PRIMARY | SECONDARY
v1_structure_intact: true
v1b_intact: true
v3_news_clear: false
vix_veto_long: false
vix_stale: true
reforecast_action: NONE
reforecast_triggers: []
e0_entry_confirmation: false
e1_oscillator_extreme: false
e2_h1_oscillator: false
e3_non_trending: false
e4_structure_intact: true
e5_compression: true
entry_confluence_score: 2.0
zone_confluence_score: 7.5
order_limit: NO_TRADE
limit_price: null
limit_direction: SELL
dgs2_now: 4.150
dgs2_baseline: 4.150
dgs2_slope: 0.200
dxy_jump: -0.106
adx_val: 39.6
spot: 1.15490
---

# Validation — 2026-06-10 EURUSD (PRIMARY + SECONDARY SHORT zones from [[2026-W24]])

*London-session `/validate eurusd` (data pulled 2026-06-10 08:07 UTC; supersedes the 02:14 run). **CPI day — V3 HARD BLOCK** (US May CPI 12:30 UTC, within 2h NY open — shared US event). Spot 1.15490, below both SHORT zones — no overbought fade setup. Both zones held PENDING, no orders.*

## Market Snapshot
| | Value | Note |
|---|---|---|
| Spot | 1.15490 | **below** both SHORT zones (1.1618 / 1.1574) — not at resistance |
| Last D1 close | 1.15339 | below both zone tops; short zones intact |
| RSI D1 / H4 / H1 | 32.7 / 56.6 / 49.0 | D1 oversold (not OB); H4/H1 mid — no short-fade extreme |
| ADX(14) D1 / H1 | 39.6 / 42.2 | strongly trending (down) — anti-fade for mean-reversion |
| US 2Y (DGS2) | 4.15% | 20d slope +0.20 (USD-supportive = pair-bearish) |
| DXY | 1d jump −0.106 | within band; no DXY-jump short trigger, no flip |
| VIX | 18.92 (06-08, stale) | <35, falling; no long veto (and stale → suspended) |
| D1 ATR | 0.00552 vs median 0.00569 | compressed (mild) |

## Q1+Q2 — Hard Blocks
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone | ✅ | Close 1.15339 below short zones — intact (invalidation = close ABOVE zone top). |
| V1b | 2 consec H4 closes past extreme | ✅ | Price below zones; no closes past upper extremes. Intact. |
| V3 | Hard event within 2h London/NY | ❌ **BLOCK** | US May CPI 12:30 UTC within 2h of NY open. NO TRADE. |
| VETO | VIX spike>3 → longs | ✅ | VIX −2.59 (falling) and stale; no LONG veto (no long zones anyway). |
| Macro flip | DXY jump / DGS2 drift | ✅ | DXY 1d −0.106 (<0.5); DGS2 flat vs baseline. No flip. |

## Q3 — Re-Forecast Check
**Precondition fails (CPI ~4.5h out).** T1 DGS2 1d ~0; T2 DXY −0.106; T3 no 1.5% counter-move; T4 no shock; T5 no macro drift vs baseline. **Action: NONE.** Bias unchanged: BEARISH (sell bounces into resistance).

## Q4 — Entry Confluence (mean-reversion short fade)
| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| E0 | Bearish reversal confirm at resistance | 3.0 | ❌ | Price below zones — no setup. |
| E1 | Oscillator still extreme (OB) | 2.5 | ❌ | RSI D1 32.7 oversold, not OB. |
| E2 | H1 oscillator extreme | 1.5 | ❌ | H1 RSI 49.0 — neutral. |
| E3 | Non-trending (ADX<25) | 1.0 | ❌ | ADX D1 39.6 — strongly trending. |
| E4 | Structure/band intact | 1.0 | ✅ | Short structure intact. |
| E5 | Compression holds | 1.0 | ✅ | D1 ATR mildly compressed. |
| | **Total** | **2.0 / 10.0** | | < 5.0 → NO TRADE (V3 also blocks). |

## Result
### ❌ NO TRADE — PRIMARY SHORT (1.1618–1.1640) — EC 2.0; V3 block. Held PENDING.
### ❌ NO TRADE — SECONDARY SHORT (1.1574–1.1593) — EC 2.0; V3 block. Price below zone. Held PENDING.

**FX netting:** no FX orders placed → gate not engaged.
**Next:** re-validate post-CPI / tomorrow AM. Need price to rally INTO a short zone with an OB extreme + bearish E0.

Sources: [BLS CPI schedule](https://www.bls.gov/schedule/news_release/cpi.htm) · [Trading Economics — US calendar](https://tradingeconomics.com/united-states/calendar)
