---
type: daily_validation
instrument: eurgbp
date: 2026-06-09
week: 2026-W24
active_zone: PRIMARY_LONG | SECONDARY_SHORT
v1_structure_intact: true
v1b_intact: true
v3_news_clear: true
vix_veto: false
vix_stale: false
reforecast_action: NONE
reforecast_triggers: []
e0_entry_confirmation: false
e1_d1_osc_extreme: false
e2_h1_osc_extreme: true
e3_non_trending: true
e4_structure_intact: true
e5_compression: true
entry_confluence_long: 4.5
entry_confluence_short: 3.0
zone_confluence_long: 8.0
zone_confluence_short: 7.5
e0_pattern: none
anchor_type: zone_50pct
order_limit: NO_TRADE
limit_direction: N/A
limit_expires: 2026-06-09 21:00 UTC
h4_atr: 0.00109
d1_atr: 0.00262
d1_atr_compressed: true
rate_diff_now: -1.731
rate_diff_baseline: -1.731
rate_diff_slope: -0.002
adx_val: 21.9
---

# Validation — 2026-06-09 (PRIMARY LONG + SECONDARY SHORT from [[2026-W24]])

*First `/validate eurgbp` (cross). Scheduled NY-session `/validate all` run (data pulled 2026-06-09 13:41 UTC). Cross = mean-reversion fade, macro-light (rate-diff is a 0.5 tilt, not scored at entry). **NO VIX veto** (risk-off bids EURGBP up). Spot sits mid-range — at neither zone.*

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 0.86329 | mid-range (0.8608–0.8682) — above LONG zone, below SHORT zone |
| Last D1 close | 0.86460 | inside range; neither zone broken |
| Rate diff (ECBDFR−SONIA) | −1.731 | 20d slope −0.002 → flat/dead (macro-light, informational only) |
| H4 ATR | 0.00109 | low-vol cross |
| D1 ATR | 0.00262 | median 0.00329 → compressed ✅ |
| VIX | 18.92 | **no veto for cross** (inverted polarity); 1d −2.59 |
| ADX(14) D1 | 21.9 | < 25 — non-trending, fade regime OK |
| RSI D1 / H4 / H1 | 43.7 / 45.9 / 24.7 | D1/H4 neutral; H1 24.7 oversold (favours LONG side, but price above LONG support) |

## Q1+Q2 — Hard Blocks (all pass)
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone | ✅ | D1 close 0.86460 inside range; neither zone broken. Intact. |
| V1b | 2 consec H4 closes >4pip past zone | ✅ | Price mid-range; no closes past either extreme. Intact. |
| V3 | ECB/BoE/UK/EZ tier-1 within 2h open | ✅ | No European tier-1 today. US CPI Wed = **caution only** for the cross (no USD leg), not a hard block. |
| VETO | (cross: none) | ✅ | No VIX veto for EURGBP. Hard veto only on D1 ADX>30 against the fade — ADX 21.9, n/a. |
| Macro | rate-diff drift | ✅ | Diff flat (−1.731, slope −0.002). Informational; not a flip gate for the cross. |

## Q3 — Re-Forecast Check
Triggers fired: none (cross counter-move < threshold; no European shock; macro flat). **Action: NONE.**

## Q4 — Entry Confluence
**PRIMARY LONG** (support 0.8608–0.8624 — price 0.86329 is ~9pip above it):
| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| E0 | Reversal turn AT zone | 3.0 | ❌ | Price not at the LONG support zone. |
| E1 | D1 oscillator still extreme | 2.5 | ❌ | D1 RSI 43.7 — not oversold (<30). |
| E2 | H1 oscillator extreme (fade side) | 1.5 | ✅ | H1 RSI 24.7 < 30 (oversold — supports a long), but away from zone. |
| E3 | Non-trending (ADX<25) | 1.0 | ✅ | D1 ADX 21.9. |
| E4 | Structure / band intact | 1.0 | ✅ | LONG support not broken on D1 close. |
| E5 | Compression holds | 1.0 | ✅ | D1 ATR 0.00262 < median 0.00329. |
| | **Total** | **4.5 / 10.0** | | < 5.0 floor |

**SECONDARY SHORT** (resistance 0.8664–0.8682 — price ~31pip below it):
E0 ❌ · E1 ❌ (RSI not >65) · E2 ❌ (H1 oversold = wrong side for short) · E3 ✅ · E4 ✅ · E5 ✅ → **3.0 / 10.0** < 5.0.

## Result
```
NO TRADE (both zones) — LONG 4.5 / SHORT 3.0, both < 5.0: spot mid-range, at neither zone. H1 oversold favours the long side but price is ~9pip above LONG support — wait for a tag of 0.8608–0.8624 with a bullish reversal close. Zones held PENDING.
```
**FX netting (D022):** EURGBP is the cross axis — would need to net vs any live eurusd/gbpusd order. None placed today → no conflict. Re-validate tomorrow.

Sources: [Trading Economics — UK/EZ calendar](https://tradingeconomics.com/united-kingdom/calendar)
