---
type: daily_validation
instrument: eurgbp
date: 2026-06-10
week: 2026-W24
active_zone: PRIMARY | SECONDARY
v1_structure_intact: true
v1b_intact: true
v3_news_clear: true
vix_veto: none
reforecast_action: NONE
reforecast_triggers: []
e0_entry_confirmation: false
e1_d1_oscillator_extreme: false
e2_h1_oscillator: false
e3_non_trending: true
e4_structure_intact: true
e5_compression: true
entry_confluence_score: 3.0
zone_confluence_score: 8.0
order_limit: NO_TRADE
limit_price: null
limit_direction: BUY
rate_diff_now: -1.731
rate_diff_baseline: -1.731
adx_val: 22.6
spot: 0.86296
---

# Validation — 2026-06-10 EURGBP (PRIMARY LONG + SECONDARY SHORT zones from [[2026-W24]])

*London-session `/validate eurgbp` (cross; data pulled 2026-06-10 08:07 UTC; supersedes the 02:14 run). US CPI = **caution only** for the cross (no USD leg → not a hard block); no UK/EZ tier-1 event today; no VIX veto. Spot 0.86296 sits ~6 pips ABOVE the primary LONG support zone — closest setup but not in-zone, and the mandatory D1 oscillator is not extreme. Both zones held PENDING, no orders.*

## Market Snapshot
| | Value | Note |
|---|---|---|
| Spot | 0.86296 | ~6 pips above PRIMARY LONG zone top (0.8624); well below SECONDARY SHORT (0.8664) |
| Last D1 close | 0.86258 | above long-zone top → long zone intact (invalidation = close BELOW 0.8608) |
| RSI D1 / H4 / H1 | 41.3 / 24.0 / 60.5 | **D1 (mandatory) NOT extreme**; H4 deeply oversold (supportive); H1 leaning up |
| ADX(14) D1 / H1 | 22.6 / 28.8 | D1 <30 — non-trending (no cross trend-veto; supports a fade) |
| Cross rate-diff (ECBDFR−SONIA) | −1.731 | flat vs baseline; macro = low-weight tilt only (EG2: thin/dead) |
| VIX | 18.92 (06-08, stale) | **No veto for the cross** (risk-off bids EURGBP up — inverted vs majors) |
| D1 ATR | 0.00252 vs median 0.00329 | compressed |

## Q1+Q2 — Hard Blocks
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone | ✅ | Close 0.86258 above LONG zone top — intact (invalidation = close BELOW 0.8608). |
| V1b | 2 consec H4 closes past extreme | ✅ | No closes past zone extremes. Intact. |
| V3 | Hard event within 2h London/NY | ✅ | US CPI = caution only for cross (no USD leg). No ECB/BoE/UK/EZ tier-1 today. |
| VETO | (cross) D1 ADX>30 against fade | ✅ | ADX D1 22.6 (<30) — no trend veto. No VIX veto for cross. |
| Macro | rate-diff drift (informational) | ✅ | −1.731 flat; not a flip gate for the cross. |

## Q3 — Re-Forecast Check
No re-forecast triggers fire (no UK/EZ shock; cross macro flat; no 1.5% counter-move). **Action: NONE.** Bias unchanged: NEUTRAL/range — fade both edges.

## Q4 — Entry Confluence (cross mean-reversion; D1 oscillator mandatory)
**PRIMARY LONG (0.8608–0.8624):**
| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| E0 | Bullish reversal confirm at support | 3.0 | ❌ | Price ~6 pips above zone; no in-zone confirmation. |
| E1 | D1 oscillator still extreme (<30) | 2.5 | ❌ | RSI D1 41.3 — not oversold (mandatory row fails). |
| E2 | H1 oscillator extreme | 1.5 | ❌ | H1 RSI 60.5 — leaning up, not oversold. |
| E3 | Non-trending (ADX<25) | 1.0 | ✅ | ADX D1 22.6. |
| E4 | Structure/band intact | 1.0 | ✅ | Long support structure intact; H4 RSI 24 supportive. |
| E5 | Compression holds | 1.0 | ✅ | D1 ATR compressed. |
| | **Total** | **3.0 / 10.0** | | < 5.0 → NO TRADE. |

**SECONDARY SHORT (0.8664–0.8682):** spot 0.86296 well below — not at resistance, no OB extreme → EC ~2.0 → NO TRADE.

## Result
### ❌ NO TRADE — PRIMARY LONG (0.8608–0.8624) — EC 3.0; not in-zone + D1 osc not extreme + no E0. Held PENDING.
### ❌ NO TRADE — SECONDARY SHORT (0.8664–0.8682) — price far below; no fade. Held PENDING.

**FX netting:** no FX orders placed → cross axis not engaged.
**Next:** WATCH primary LONG — needs price INTO 0.8608–0.8624 + D1 oscillator oversold (<30) + bullish E0. H4 already deeply oversold (RSI 24) but the mandatory D1 read isn't there yet.

Sources: [Trading Economics — UK calendar](https://tradingeconomics.com/united-kingdom/calendar) · [Trading Economics — Euro Area calendar](https://tradingeconomics.com/euro-area/calendar)
