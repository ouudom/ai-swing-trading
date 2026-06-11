# _HOT — Session State
*Always current. Updated at end of every session.*
*RULE: hard cap **120 lines**. Current state + last session only. History lives in
`forecasts/daily|weekly/*`, `decisions.md`, `_INDEX.md` — link, don't repeat. Prune every session.*

## System Status — v2 ACTIVE (2026-06-02)
Structured + AI-analysis entry-signal generation. Markdown-only (no DB). Unit = **Trading Zone**
(max 3/wk, ≤1 counter), Zone Confluence R1 + Entry Confluence R2 (max 10, floor 5, E0 confirm 3pt).

## Instruments — 10 ACTIVE (D024 expansion COMPLETE)
| Inst | Status | Character | Key docs |
|---|---|---|---|
| XAUUSD | active | momentum (pro-trend), real-yield macro | wiki/system/xauusd/ |
| EURUSD | active | mean-reversion fade, H4-centric; DXY-jump/US2Y/VIX gate (D021) | wiki/system/eurusd/ |
| GBPUSD | active | mean-reversion fade, D1-reversal+H1; same macro gate | wiki/system/gbpusd/ |
| EURGBP | active | cross, mean-reversion fade, macro 0.5 tilt, NO VIX-veto, EU event blocks | wiki/system/eurgbp/ |
| AUDUSD | active | mean-reversion fade, H4-centric; 🔑 DXY-jump DEAD, VIX LEVEL inverted, NO vetoes except ADX>30; RBA/AU/China events | wiki/system/audusd/ |
| NZDUSD | active | mean-reversion fade, macro-light squeeze-led; 🔑 US2Y+DXY DEAD, VIX level weak inverted; weakest edges (≈½ AUD) → fewer zones; RBNZ/NZ events; antipodean advisory | wiki/system/nzdusd/ |
| USDCAD | active | **USD-base** mean-reversion fade; 🔑 polarity flips (US2Y rising=bullish, VIX>20→SHORT bias t≈3.9, COT 6C inverted); 🛢 oil tilt weak; H1 long-side rich; BoC/CAD events (12:30 overlap!) | wiki/system/usdcad/ |
| USDCHF | active | **USD-base** mean-reversion fade, H1-centric; 🔑 DXY 20d slope = live macro (t=2.3, only pair beyond EUR/GBP), VIX WASHOUT (no gate/score), COT 6S inverted; H1 short-fade machine (t 4.5–5.5); ⚠ SNB regime — shorts near 0.78–0.80 cap MEDIUM, SNB days hard block | wiki/system/usdchf/ |
| USDJPY | active | **USD-base, FIRST JPY pair** (pip 0.01, 3dp, TICK 650 static); 🔑 **ASYMMETRIC carry-drift, NOT fade**: LONG = squeeze/calm/dip/NY-drift (t 3.3–4.7), SHORT = D1/H4 extremes only, **H1-only shorts PROHIBITED** (anti −3.3); DXY 20d slope live (t=2.2), VIX washout, US2Y dead, COT 6J inverted; ⚠ MoF regime — longs ≥158 cap MEDIUM, BoJ/MoF days hard block (spot 160.5 IN band) | wiki/system/usdjpy/ |
| EURJPY | active | **FIRST cross-JPY** (pip 0.01, 3dp, TICK 650 static); 🔑 **symmetric mean-reversion + calm-drift** on long-drift floor (D1 LNG 55.6%): buy washouts (Stoch<20 t=3.1), fade extension (Keltner-high t=3.4, H1 W%R t=4.2 — H1 fade WORKS, unlike usdjpy), NEVER chase (C26 anti −4.2); **macro NONE** (first 100% price-driven — ECB anti, VIX dead, no USD leg); sessions two-sided: London fade-short t=2.8 / NY drift-long t=3.0; COT XRATE direct but THIN (OI 21k); ⚠ MoF slams hit crosses — BoJ/MoF + ECB hard block, record-high longs cap MEDIUM (spot 185.2) | wiki/system/eurjpy/ |
| GBPJPY | active | **cross-JPY #2, LAST pair** (pip 0.01, 3dp, TICK 650 static, V1b 0.05 — highest ATR: D1 med 151p); 🔑 **extension-fade SHORT-dominant** on strongest long-drift floor (D1 LNG 56.7%): fade spikes (Keltner-high t=4.64/4.01, BB-upper 63%win +0.42%), buy washouts (RSI<35 t=2.4, 73%win); **NO calm engine** (only JPY pair without), **macro NONE** (SONIA ns, VIX dead), NEVER chase (C26 anti −5.0); sessions NY long-only (overlap t=4.2; SHORT 13–15 UTC = ANTI −3.84); **COT DISABLED** (no CFTC cross contract); ⚠ MoF slams largest of crosses — BoJ/MoF + BoE hard block, record-high longs cap MEDIUM (spot 214.6) | wiki/system/gbpjpy/ |

Onboarding history (P1–P5 majors, EG0–EG5 cross), signal scans, sizing decisions → `decisions.md`
(D021/D022/D023) + `wiki/research/{pair}/signal-results.md`. Sizing all pairs: USD, no quote-CCY
convert (operator). FX netting: `scripts/fx_exposure.py` gate at /validate (D022).
Known: backfill forward catch-up throws non-fatal "No data available" at weekend edge — data lands fine.

## Active Forecasts — 2026-W24
- **XAUUSD** [W24](forecasts/weekly/xauusd/2026-W24.md) — BEARISH/MEDIUM-HIGH, conviction HIGH.
  PRIMARY SHORT $4367–$4390 (9.5), SECONDARY SHORT $4450–$4485 (9.5), no counter. Spot ~$4162,
  ADX 48 — zones ~$200 OTM, re-anchor likely Sunday. Invalidate: D1 close > zone top.
- **EURUSD** [W24](forecasts/weekly/eurusd/2026-W24.md) — SHORT 1.1618–1.1640 (7.5) + 1.1574–1.1593 (6.5). Spot 1.1549.
- **GBPUSD** [W24](forecasts/weekly/gbpusd/2026-W24.md) — SHORT 1.3400–1.3447 (8.0) + 1.3370–1.3390 (6.5). Spot 1.3384.
- **EURGBP** [W24](forecasts/weekly/eurgbp/2026-W24.md) — NEUTRAL/range. LONG 0.8608–0.8624 (8.0) +
  SHORT 0.8664–0.8682 (7.5). Spot 0.8630. Fade both edges; no VIX-veto; netting ledger required.
- FX strategy: sell bounce into resistance (USD strength); both majors SHORT → if both fill = 2× long
  USD → netting gate keeps best EC, skips other (D022).

## Open Position
None

## Live Order Limits — NONE (2026-06-10 08:06 UTC, CPI day = V3 HARD BLOCK)
XAUUSD limits expired 06-09 21:00 UTC, NOT re-placed (CPI block + spot ~$200 below zone). 0 FX orders.

## Week Status
- Week: 2026-W24 | Trades: 0 | Risk allocated: $0 | weekly_reforecast_count: 0

## Pending Actions
- **/validate daily 07:30 UTC** — no limits live; re-validate each morning.
- **CPI TODAY 06-10 12:30 UTC = V3 HARD BLOCK** (US-event instruments). PPI Thu, UMich Fri caution.
  Re-validate post-CPI; watch cool-print squeeze (oversold all TFs) — sell bounce, don't chase.
- **T5 drift watch:** DFII10 2.21 vs baseline 2.11 = +0.10 (WITH bias); >0.15 total forces re-forecast.
- **GBPUSD watch:** closest USD fade — fresh rally into 1.3400 + H1 OB + bearish E0 → ~7.5 ORDER LIMIT.
- **EURGBP watch:** primary LONG 0.8608–0.8624 — needs D1 oversold + in-zone + bullish E0.
- **FX netting gate (D022):** both majors ORDER LIMIT same day → keep higher EC, SKIP other.
- **EXPANSION (D024) ✅ COMPLETE 2026-06-11:** W0 ledger + all 7 pairs onboarded and ACTIVE
  (AUDUSD, NZDUSD, USDCAD, USDCHF, USDJPY, EURJPY, **GBPJPY #7 — LAST, scan GO**). All scans GO,
  10 instruments live. Rulings: USD sizing no convert; netting ADVISORY only.
  First /weekly for the 7 new pairs still pending (no zones yet).

## Last Session
2026-06-11 (expansion, GBPJPY #7 — LAST PAIR, D024 COMPLETE): gbpjpy config (eurjpy pattern:
USD_BETA_SIGN=0, JPY pip 0.01/3dp/TICK 650; V1b 0.05 = 10% median H4 ATR 54p; one-leg macro live
leg = SONIA via RATE_EUR slot; **COT DISABLED** — no CFTC cross contract). Pipeline: one-leg
branch GENERALIZED (cfg LIVE_LEG_LABEL/LIVE_LEG_CCY/BASELINE_LABEL, FLAT tie tolerance 0.005;
backtest X9/X10 label now series-driven) — eurgbp X-rows regression ✅. Backfill D1 4289 (2010→)/
H4 9793/H1 39248/15min 60260 (one DNS-failure retry mid-backfill, data complete). Scan **GO —
extension-fade SHORT-dominant** (template #4): SHORT Keltner-high t=4.64(H4)/4.01(D1), BB-upper
63%win +0.42%, RSI>65 all TFs; LONG washout RSI<35 2.43/2.26 73%win, Keltner-low 2.33/2.27;
🔑 carry-trend hypothesis REJECTED (all trend rows anti, C26 −5.0/−4.7); 🔑 **NO calm engine**
(D6 1.42, B11 −0.32 — only JPY pair without); 🔑 macro NONE (SONIA 0.58, VIX 0.89 — second 100%
price-driven pair); sessions NY long-only (overlap 4.20, NY-open SHORT ANTI −3.84, London DEAD);
seasonals: Sept short +2.34, turn-of-month long −2.99, Jan long −2.28. ATR D1 med 151p (now 93
compressed), H4 med 54p. Spot 214.6 record — BoJ/MoF + BoE hard blocks. R1/R2 ACTIVE (multi-TF
alignment 1.5 replaces calm row; SHORT E2: outside 12–16 = 0.75, inside 13–15 = 0); wired weekly/
validate/constitution (+GBPJPY column, baseline_sonia_rate). Smoke: pull W24 ✅ (3dp, SONIA block
FLAT, lots 8.24 = 2000/(0.373×650) ✓), check_v1b ✅ intact, ledger usdjpy+eurjpy+gbpjpy long =
−3.00u short JPY flagged ✅, selftest PASS.
2026-06-11 (expansion, EURJPY #6 — FIRST cross-JPY): eurjpy config (_fx_base + USD_BETA_SIGN=0 +
JPY pip 0.01/3dp/TICK 650, V1b 0.04 = 10% median H4 ATR 42p, COT "EURO FX/JAPANESE YEN XRATE"
DIRECT thin OI 21k, FRED +ECBDFR). Pipeline generalized for ONE-LEG cross: weekly_pull new
cross_rate_diff branch when RATE_GBP=None (ECB-only block, `baseline_ecb_rate`); backtest guards
load_fred(None) — eurgbp X-rows regression ✅. Backfill D1 4289 (2010→)/H4 9791/H1 39226/15min
60235 (2024→). Scan **GO — symmetric mean-reversion + calm-drift** on long-drift floor (D1 LNG
55.6%): LONG washout-buy (D1 Stoch<20 t=3.10 73%win, H1 Keltner-low 2.62, 20d-low 3.07) + calm/
squeeze (H4 D6 t=3.96, B11 2.71); SHORT extension-fade ALL TFs (Keltner-high 3.36/3.48/2.82,
H1 W%R>−20 t=4.21 — H1 fade WORKS, unlike usdjpy); 🔑 **macro NONE** (ECB leg ANTI −1.2/−1.3,
VIX DEAD 0.91 despite carry reputation — first 100% price-driven pair); sessions two-sided
(London fade-short 2.77 / NY-overlap drift-long 3.02); anti: C26 chase −4.24, calm-short −3.99,
turn-of-month −3.10. ATR D1 med 118p (now 76 compressed), H4 med 42p. Spot 185.2 record — MoF
slams hit crosses → BoJ/MoF + ECB hard blocks, record-high longs cap MEDIUM. R1/R2 ACTIVE
(extreme engine 2.5 both sides, NO macro/VIX rows); wired weekly/validate/constitution (+EURJPY
column). Smoke: pull W24 ✅ (3dp, one-leg macro block, COT +1,336 direct, lots 2000/(SL×650) ✓
11.35), check_v1b ✅ 3dp intact, ledger usdjpy+eurjpy long = −2.00u short JPY flagged ✅, selftest
PASS.
2026-06-11 (expansion, USDJPY #5): GO ASYMMETRIC (LONG drift / SHORT extremes; H1 fade ANTI);
3 plumbing fixes (PRICE_DP override, check_v1b dp heuristic, S1 PIP_SIZE). Detail →
`wiki/research/usdjpy/signal-results.md`.
2026-06-11 (expansion, USDCHF #4): GO H1-centric fade; DXY 20d slope live; VIX washout; SNB
regime. Detail → `wiki/research/usdchf/signal-results.md`.
2026-06-10 (expansion, USDCAD #3 + NZDUSD #2 + W0 + AUDUSD #1): USDCAD GO (first USD-base —
`_fx_usd_base.py`, U()-flip, W1–W6 oil rows); NZDUSD GO marginal; W0 fx_exposure ledger; AUDUSD GO.
Detail → `wiki/research/{pair}/signal-results.md` + `decisions.md` D024.
2026-06-10 (08:06 UTC, scheduled `/validate all` — 4 instruments): CPI day = V3 HARD BLOCK; all
zones ❌ NO TRADE, held PENDING, no orders. Detail → `forecasts/daily/*/2026-06-10.md`.
