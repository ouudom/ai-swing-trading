# _HOT — Session State
*Always current. Updated at end of every session.*
*RULE: hard cap **120 lines**. Current state + last session only. History lives in
`forecasts/daily|weekly/*`, `decisions.md`, `_INDEX.md` — link, don't repeat. Prune every session.*

## System Status — v2 ACTIVE (2026-06-02)
Structured + AI-analysis entry-signal generation. Markdown-only (no DB). Unit = **Trading Zone**
(max 3/wk, ≤1 counter), Zone Confluence R1 + Entry Confluence R2 (max 10, floor 5, E0 confirm 3pt).

## Instruments — 9 ACTIVE
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
- **EXPANSION (D024, 2026-06-10):** all 7, sequential. ✅ W0 ledger + ✅ AUDUSD #1 + ✅ NZDUSD #2 +
  ✅ USDCAD #3 + ✅ USDCHF #4 + ✅ USDJPY #5 + ✅ **EURJPY #6 DONE** (first cross-JPY; scan GO
  symmetric; ACTIVE). ⏳ NEXT (LAST): **GBPJPY #7 — cross-JPY #2**: inherit eurjpy pattern
  (USD_BETA_SIGN=0, JPY pip 0.01/3dp/TICK 650, one-leg macro — live leg = SONIA IUDSOIA, JPY leg
  none; reuse the RATE_GBP=None one-leg branch with SONIA as the single series); high-ATR
  calibration (GBPJPY ≈ 1.5–2× EURJPY — recalc V1B_BUFFER from H4 ATR median); NO direct CFTC
  cross contract (2026 zip has only EUR/GBP + EUR/JPY XRATEs) → COT_ENABLED=False or 6B/6J
  derived; BoE + BoJ/MoF events. JPY carry-trend crosses may scan NO-GO → keep config+data+
  research, no confluence.
  Rulings: USD sizing no convert; netting ADVISORY only.

## Last Session
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
2026-06-11 (expansion, USDJPY #5 — FIRST JPY pair): 3 plumbing fixes — weekly_pull PRICE_DP now
config-overridable, check_v1b dp heuristic 3-tier (≥500→2dp / 20–500→3dp / else 5dp), backtest S1
big-figure now PIP_SIZE-driven (was hardcoded ×100). usdjpy config (PIP 0.01, 3dp, TICK 650 static,
V1b 0.04, RATE_FOREIGN=None BoJ, COT 6J). Backfill D1 4288 (2010→)/H4 9764/H1 39179/15min 60142
(2024→). Scan **GO — ASYMMETRIC, breaks fade template**: LONG = drift continuation (D1 TTM squeeze
t=3.27 +15.9pp, H4 calm t=4.51, H1 NY-overlap drift t=4.71, dip-at-20d-low 3.15, BB-breakout
CONTINUATION 3.08); SHORT = D1/H4 extremes only (RSI>65 2.66, CCI>+100 3.11); 🔑 **H1 fade = ANTI
(−3.3)**, London open FLAT (breaks 4-pair pattern — NY drift instead), no chasing extension (ADX>25
long anti −3.4). DXY 20d slope live (t=2.21, 3rd pair = USD-base havens), VIX washout, US2Y dead.
Spot 160.5 = INSIDE 2024 MoF intervention band → longs ≥158 cap MEDIUM, BoJ/MoF = hard block.
Direction-aware R1/R2 ACTIVE; wired weekly/validate/constitution (+USDJPY column). Smoke: pull W24
✅ (3dp, US2Y flipped label, COT −136.6k JPY = BULLISH USDJPY ⚠ INVERTED, lots 2000/(SL×650) ✓),
check_v1b ✅ 3dp intact, ledger usdjpy+usdchf+eurusd = +3.00u long USD flagged ✅, selftest PASS.
2026-06-11 (expansion, USDCHF #4 — USD-base clone): usdchf config (`_fx_usd_base` inherit, no oil
leg, RATE_FOREIGN=None SNB, COT 6S, V1b 4pip), registered weekly_pull + backtest_signals. Backfill
D1 4287 (2010→)/H4 9774/H1 39197/15min 60125 (2024→). Scan **GO**: mean-reverting fade, H1-centric
— H1 short-fade machine (W%R>−20 t=5.48, RSI>65 t=4.57, Keltner-high t=4.57), H1 long side TTM
squeeze t=3.20/calm t=3.03/near-20d-low t=2.92, London-open LONG drift t=2.70 (4th pair); H4 thin.
🔑 DXY 20d SLOPE live (t=2.32/2.34 — first pair beyond EUR/GBP); **VIX WASHOUT** (haven-vs-haven —
no gate/score, fade-USD regime does NOT transfer); US2Y flipped weak tilt; DXY-jump anti (−1.69).
Anti-edges: all H1 momentum continuation, H4 downtrend-cont −3.05. Profile (SNB intervention
regime + quarterly block; CHF pip ~25% OVER-size accepted) + confluence ACTIVE (Z3 DXY slope 2.0;
SNB short-cap 0.78–0.80 → MEDIUM), wired weekly/validate/constitution (USD-base column merged
CAD/CHF). Smoke: pull W24 ✅ (US2Y "bullish USDCHF" label, COT spec −33k CHF = BULLISH USDCHF
⚠ INVERTED), check_v1b ✅ intact, ledger eurusd-short+usdchf-long = +2.00u long USD flagged ✅.
2026-06-10 (expansion, USDCAD #3 + NZDUSD #2 + W0 + AUDUSD #1): USDCAD GO (first USD-base —
`_fx_usd_base.py`, U()-flip, W1–W6 oil rows); NZDUSD GO marginal; W0 fx_exposure ledger; AUDUSD GO.
Detail → `wiki/research/{pair}/signal-results.md` + `decisions.md` D024.
2026-06-10 (08:06 UTC, scheduled `/validate all` — 4 instruments): CPI day = V3 HARD BLOCK; all
zones ❌ NO TRADE, held PENDING, no orders. Detail → `forecasts/daily/*/2026-06-10.md`.
