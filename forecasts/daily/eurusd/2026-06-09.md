---
type: daily_validation
instrument: eurusd
date: 2026-06-09
week: 2026-W24
active_zone: PRIMARY | SECONDARY
v1_structure_intact: true
v1b_intact: true
v3_news_clear: true
vix_veto_long: false
vix_stale: false
reforecast_action: NONE
reforecast_triggers: []
e0_entry_confirmation: false
e1_osc_extreme: false
e2_band_touch: false
e3_non_trending: false
e4_compression: true
e5_structure_intact: true
entry_confluence_score: 2.0
zone_confluence_score: 7.5
e0_pattern: none
anchor_type: zone_50pct
order_limit: NO_TRADE
limit_direction: N/A
limit_expires: 2026-06-09 21:00 UTC
h4_atr: 0.00265
d1_atr: 0.00564
d1_atr_compressed: true
dgs2_now: 4.170
dgs2_baseline: 4.170
dgs2_slope: 0.270
dxy_jump: -0.321
adx_val: 39.3
---

# Validation — 2026-06-09 (PRIMARY + SECONDARY SHORT zones from [[2026-W24]])

*Scheduled NY-session `/validate all` run (data pulled 2026-06-09 13:41 UTC). Supersedes the 05:36 UTC run. Mean-reversion fade system — short zones rest ABOVE spot as resistance; need price AT the zone with an overbought turn to fade.*

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 1.15645 | below BOTH short zones (1.1574–1.1593 / 1.1618–1.1640) — not at resistance |
| Last D1 close | 1.15289 | below both zone bottoms — zones intact |
| US 2Y (DGS2) | 4.17% | 20d slope +0.270 (rising US rates = USD bid = EUR pressure, supports bearish lean) |
| DXY 1d jump | −0.321 | < +0.5 → no DXY-short gate fired today |
| H4 ATR | 0.00265 | — |
| D1 ATR | 0.00564 | median 0.00575 → compressed ✅ |
| VIX | 18.92 | fresh (06-08), <35, 1d −2.59 → no LONG veto; risk calm |
| ADX(14) D1 | 39.3 | strongly trending — fade regime guard FAILS (E3) |
| RSI D1 / H4 / H1 | 36.0 / 37.2 / 73.7 | D1/H4 mid-low (not overbought); H1 73.7 overbought is a bounce, but well below resistance |

## Q1+Q2 — Hard Blocks (all pass)
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone | ✅ | D1 close 1.15289 below both short-zone bottoms. Intact. |
| V1b | 2 consec H4 closes >6pip past zone | ✅ | Price below zones; no closes past extreme. Intact. |
| V3 | Hard news within 2h London/NY | ✅ | No US tier-1 / ECB today. **US CPI Wed 06-10 12:30 UTC = tomorrow's hard block.** |
| VETO | VIX spike>3 / >35 → longs | ✅ | VIX 18.92 fresh, 1d −2.59 (calming) → no LONG veto. |
| Macro flip | DGS2/DXY vs baseline | ✅ | DGS2 flat vs baseline; DXY 1d −0.321 (no >0.5 jump). No flip. |

## Q3 — Re-Forecast Check
Triggers fired: none (T1 DGS2 jump small; T2 DXY −0.321 < 0.75; T3 EUR counter-move < 1.5%; T4 no shock; T5 macro flat). **Action: NONE.**

## Q4 — Entry Confluence (both SHORT zones)
| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| E0 | Reversal turn AT zone | 3.0 | ❌ | Price 1.15645 not at either short zone — no fade trigger. |
| E1 | H4 oscillator still extreme | 2.5 | ❌ | H4 RSI 37.2 — not overbought; nothing to fade. |
| E2 | Band touch (upper, fade side) | 1.5 | ❌ | Price near lows, not tagging upper band. |
| E3 | Still non-trending (ADX<25) | 1.0 | ❌ | D1 ADX 39.3 — strongly trending. |
| E4 | Compression holds | 1.0 | ✅ | D1 ATR 0.00564 < median 0.00575. |
| E5 | Structure / zone intact (D1 close) | 1.0 | ✅ | Short zones not broken to upside. |
| | **Total** | **2.0 / 10.0** | | < 5.0 floor |

## Result
```
NO TRADE — score 2.0 < 5.0: price well below both SHORT fade zones, no overbought extreme, D1 trending (ADX 39.3). Zones held PENDING (not invalidated).
```
Both short zones rest above spot; a fade needs price to rally INTO 1.1574–1.1640 with H4 overbought + a bearish reversal close. **FX netting: no FX order placed today → no concentration gate engaged.** Re-validate tomorrow (mind CPI hard block).

Sources: [Trading Economics — US calendar](https://tradingeconomics.com/united-states/calendar)
