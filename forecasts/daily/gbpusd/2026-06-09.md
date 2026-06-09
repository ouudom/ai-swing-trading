---
type: daily_validation
instrument: gbpusd
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
e1_d1_osc_extreme: false
e2_h1_osc_extreme: true
e3_non_trending: true
e4_structure_intact: true
e5_compression: true
entry_confluence_score: 4.5
zone_confluence_score: 8.0
e0_pattern: none
anchor_type: zone_50pct
order_limit: NO_TRADE
limit_direction: N/A
limit_expires: 2026-06-09 21:00 UTC
h4_atr: 0.00351
d1_atr: 0.00698
d1_atr_compressed: true
dgs2_now: 4.170
dgs2_baseline: 4.170
dgs2_slope: 0.270
dxy_jump: -0.321
adx_val: 24.9
---

# Validation — 2026-06-09 (PRIMARY + SECONDARY SHORT zones from [[2026-W24]])

*Scheduled NY-session `/validate all` run (data pulled 2026-06-09 13:41 UTC, computed 13:47 UTC). Supersedes the 05:36 UTC run. **GBP has now rallied INTO the primary short zone** — the closest any FX zone has come to triggering. Missing only a confirmed bearish reversal close (E0).*

## Market Snapshot
| | Value | vs Baseline |
|---|---|---|
| Spot | 1.33963 | rallied into the **PRIMARY short zone (1.3400–1.3447)** — H1 high 1.34080 tagged it, pulling back |
| Last D1 close | 1.33346 | below both short-zone bottoms — zones intact |
| US 2Y (DGS2) | 4.17% | 20d slope +0.270 (rising US rates support bearish GBP lean) |
| DXY 1d jump | −0.321 | < +0.5 → no DXY-short gate fired |
| H4 ATR | 0.00351 | — |
| D1 ATR | 0.00698 | median 0.00884 → compressed ✅ |
| VIX | 18.92 | fresh (06-08), <35, 1d −2.59 → no LONG veto |
| ADX(14) D1 | 24.9 | just below 25 — non-trending guard holds (barely) |
| RSI D1 / H4 / H1 | 41.6 / 43.0 / **87.3** | H1 deeply overbought into resistance = textbook fade setup, but D1 not extreme |

## Q1+Q2 — Hard Blocks (all pass)
| | Block | Result | Note |
|---|---|---|---|
| V1 | D1 close beyond zone | ✅ | D1 close 1.33346 below short-zone bottoms. Intact (no D1 close above 1.3447/1.3390). |
| V1b | 2 consec H4 closes >6pip past zone | ✅ | H4 close 1.33963 inside/below primary zone, not past the 1.3447 extreme. Intact. |
| V3 | Hard news within 2h London/NY | ✅ | No US tier-1 / BoE today. **US CPI Wed 06-10 12:30 UTC = tomorrow's hard block.** |
| VETO | VIX spike>3 / >35 → longs | ✅ | VIX 18.92 fresh, calming → no LONG veto (and these are SHORT zones anyway). |
| Macro flip | DGS2/DXY vs baseline | ✅ | DGS2 flat; DXY 1d −0.321 (no >0.5 jump). No flip. |

## Q3 — Re-Forecast Check
Triggers fired: none (T1 small; T2 DXY −0.321; T3 GBP rally ~0.5% < 1.5%; T4 no shock; T5 flat). **Action: NONE.**

## Q4 — Entry Confluence (PRIMARY short zone — price is here)
| | Condition | Pts | Result | Note |
|---|---|---|---|---|
| E0 | Reversal turn AT zone (close-confirmed) | 3.0 | ❌ | Price in zone & H1 overbought, but last CLOSED H1 (12:00) is a small bear bar — not a pin (uw 1.2×body) or engulfing. 13:00 bar still forming. **No confirmed reversal yet.** |
| E1 | D1 oscillator still extreme | 2.5 | ❌ | D1 RSI 41.6 — not beyond fade threshold (>65). |
| E2 | H1 oscillator extreme (fade side) | 1.5 | ✅ | H1 RSI 87.3 (> 65) — strong overbought at resistance. |
| E3 | Still non-trending (ADX<25) | 1.0 | ✅ | D1 ADX 24.9 < 25 (marginal). |
| E4 | Structure / band intact (D1 close) | 1.0 | ✅ | 20d extreme not broken on D1 close. |
| E5 | Compression holds | 1.0 | ✅ | D1 ATR 0.00698 < median 0.00884. |
| | **Total** | **4.5 / 10.0** | | < 5.0 floor — **0.5 short, missing E0** |

## Result
```
NO TRADE — score 4.5 < 5.0: price has rallied into the primary short zone with H1 RSI 87.3, but no confirmed bearish H1 reversal close. A close-confirmed 1H pin/engulf or 15M CHoCH down at ~1.340 adds E0 (+3.0) → 7.5 → ORDER LIMIT. Zone held PENDING.
```
> [!important] **WATCH (intraday):** This is the trigger candidate. If a bearish H1 reversal closes near 1.3400–1.3447 before 21:00 UTC, GBP flips to ORDER LIMIT (SELL fade). Next scheduled `/validate` will re-check; an off-cycle confirmation could be acted on manually.

**FX netting (D022):** no FX order placed today → no concentration gate engaged. *Note: if GBP triggers SHORT while EUR is flat, GBP short = clean single USD-leg long-USD bet — no netting conflict yet.* SECONDARY zone (1.3370–1.3390): price now above it → NO TRADE.

Sources: [Trading Economics — US/UK calendar](https://tradingeconomics.com/united-states/calendar)
