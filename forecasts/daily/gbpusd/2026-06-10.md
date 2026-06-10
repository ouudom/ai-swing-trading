---
type: daily_validation
instrument: gbpusd
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
zone_confluence_score: 8.0
order_limit: NO_TRADE
limit_price: null
limit_direction: SELL
dgs2_now: 4.150
dgs2_baseline: 4.150
dgs2_slope: 0.200
dxy_jump: -0.106
adx_val: 25.1
spot: 1.33836
---

# Validation — 2026-06-10 GBPUSD (PRIMARY + SECONDARY SHORT zones from [[2026-W24]])

*London-session `/validate gbpusd` (data pulled 2026-06-10 08:07 UTC; supersedes the 02:14 run). **CPI day — V3 HARD BLOCK** (US May CPI 12:30 UTC, within 2h NY open). Spot 1.33836 sits inside the SECONDARY short zone (1.3370–1.3390) and just below PRIMARY (1.3400), but the earlier overbought bounce has faded — no current OB extreme, no E0. Both zones held PENDING, no orders.*

## Market Snapshot
| | Value | Note |
|---|---|---|
| Spot | 1.33836 | **inside** SECONDARY zone (1.3370–1.3390); ~16 pips below PRIMARY (1.3400) |
| Last D1 close | 1.33708 | at lower edge of secondary zone; short zones intact |
| RSI D1 / H4 / H1 | 41.0 / 62.6 / 46.6 | H1 OB bounce faded (was 87 on 06-09); H4 firm but not >65; no fade extreme now |
| ADX(14) D1 / H1 | 25.1 / 33.6 | D1 just above 25 (mildly trending) — borderline for fade |
| US 2Y (DGS2) | 4.15% | 20d slope +0.20 (USD-supportive = pair-bearish) |
| DXY | 1d jump −0.106 | within band; no DXY-jump short trigger, no flip |
| VIX | 18.92 (06-08, stale) | <35, falling; no long veto |
| D1 ATR | 0.00689 vs median 0.00870 | compressed |

## Q1+Q2 — Hard Blocks
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone | ✅ | Close 1.33708 inside/below zones; not closed ABOVE any zone top → intact. |
| V1b | 2 consec H4 closes past extreme | ✅ | No closes past upper extremes. Intact. |
| V3 | Hard event within 2h London/NY | ❌ **BLOCK** | US May CPI 12:30 UTC within 2h of NY open. NO TRADE. |
| VETO | VIX spike>3 → longs | ✅ | VIX falling and stale; no LONG veto. |
| Macro flip | DXY jump / DGS2 drift | ✅ | DXY 1d −0.106 (<0.5); DGS2 flat. No flip. |

## Q3 — Re-Forecast Check
**Precondition fails (CPI ~4.5h out).** T1 DGS2 ~0; T2 DXY −0.106; T3 no 1.5% counter-move; T4 no shock; T5 no drift. **Action: NONE.** Bias unchanged: BEARISH (sell the bounce into resistance).

## Q4 — Entry Confluence (mean-reversion short fade)
| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| E0 | Bearish reversal confirm at resistance | 3.0 | ❌ | No confirmed bearish H1 reversal close; bounce already faded. |
| E1 | Oscillator still extreme (OB) | 2.5 | ❌ | RSI D1 41.0 / H4 62.6 — not OB extreme. |
| E2 | H1 oscillator extreme | 1.5 | ❌ | H1 RSI 46.6 — neutral (faded from 87). |
| E3 | Non-trending (ADX<25) | 1.0 | ❌ | ADX D1 25.1 — just above threshold. |
| E4 | Structure/band intact | 1.0 | ✅ | Short structure intact; price at resistance. |
| E5 | Compression holds | 1.0 | ✅ | D1 ATR compressed (0.00689 < 0.00870). |
| | **Total** | **2.0 / 10.0** | | < 5.0 → NO TRADE (V3 also blocks). |

## Result
### ❌ NO TRADE — PRIMARY SHORT (1.3400–1.3447) — EC 2.0; V3 block. Held PENDING.
### ❌ NO TRADE — SECONDARY SHORT (1.3370–1.3390) — price in-zone but no OB/E0; EC 2.0; V3 block. Held PENDING.

**FX netting:** no FX orders placed → gate not engaged.
**Next:** re-validate post-CPI / tomorrow AM. GBP is the closest USD-pair fade — WATCH for a fresh rally into 1.3400 with H1 OB (>65) + a close-confirmed bearish H1 pin/engulf → E0 +3.0 → ORDER LIMIT.

Sources: [BLS CPI schedule](https://www.bls.gov/schedule/news_release/cpi.htm) · [Trading Economics — US calendar](https://tradingeconomics.com/united-states/calendar)
