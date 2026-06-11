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
- **AUDUSD** [W24](forecasts/weekly/audusd/2026-W24.md) — BEARISH/MEDIUM. PRIMARY SHORT 0.7065–0.7110 (7.0)
  + COUNTER LONG 0.6940–0.6996 (7.0, MEDIUM cap). Spot 0.7010. ADX 28.4 trending → floor 6.0.
- **NZDUSD** [W24](forecasts/weekly/nzdusd/2026-W24.md) — NEUTRAL range. PRIMARY SHORT 0.5855–0.5890 (6.5)
  + COUNTER LONG 0.5750–0.5790 (7.5, MEDIUM cap). Spot 0.5799. Antipodean gate vs AUDUSD.
- **USDCAD** [W24](forecasts/weekly/usdcad/2026-W24.md) — BULLISH/MEDIUM. PRIMARY LONG 1.3885–1.3905 (7.0).
  SHORT side VETOED (ADX 32.3>30 up). Spot 1.3938. Abort long if VIX closes >20 (fade-USD flip).
- **USDCHF** [W24](forecasts/weekly/usdchf/2026-W24.md) — BULLISH/MEDIUM-HIGH. PRIMARY LONG 0.7945–0.7960
  (7.5) + COUNTER SHORT 0.8005–0.8030 (5.5). Spot 0.7985. ADX 23.5 → validate floor 6.5. SNB 06-18 W25.
- **USDJPY / EURJPY / GBPJPY** [W24](forecasts/weekly/usdjpy/2026-W24.md) — **⛔ NO ZONES: active MoF
  intervention regime** (Apr-30 intervention ~160.7, Mimura jawboning June; spot 160.5 in trigger zone;
  crosses slam in sympathy). Reassess after BoJ 06-15/16. [eurjpy](forecasts/weekly/eurjpy/2026-W24.md) ·
  [gbpjpy](forecasts/weekly/gbpjpy/2026-W24.md)
- FX strategy: sell bounce into resistance (USD strength); USD-stack note: usdcad+usdchf LONG +
  audusd+nzdusd+majors SHORT all = long USD → netting gate keeps best EC (D022, advisory).

## Open Position
None

## Live Order Limits — NONE (2026-06-10 08:06 UTC, CPI day = V3 HARD BLOCK)
XAUUSD limits expired 06-09 21:00 UTC, NOT re-placed (CPI block + spot ~$200 below zone). 0 FX orders.

## Week Status
- Week: 2026-W24 | Trades: 0 | Risk allocated: $0 | weekly_reforecast_count: 0

## Pending Actions
- **/validate daily 07:30 UTC** — no limits live; re-validate each morning.
- **PPI TODAY 06-11 12:30 UTC = HARD ±2h** (US-event instruments). AU jobs Fri 01:30 UTC (audusd
  hard, nzdusd caution). UMich Fri 14:00 caution. W25: BoJ 06-15/16, FOMC 06-16/17, SNB+BoE 06-18.
- **T5 drift watch:** DFII10 2.21 vs baseline 2.11 = +0.10 (WITH bias); >0.15 total forces re-forecast.
- **GBPUSD watch:** closest USD fade — fresh rally into 1.3400 + H1 OB + bearish E0 → ~7.5 ORDER LIMIT.
- **EURGBP watch:** primary LONG 0.8608–0.8624 — needs D1 oversold + in-zone + bullish E0.
- **FX netting gate (D022):** both majors ORDER LIMIT same day → keep higher EC, SKIP other.
- **EXPANSION (D024) ✅ COMPLETE:** all 7 pairs onboarded + first /weekly published 2026-06-11
  (all 10 instruments forecast for W24). Rulings: USD sizing no convert; netting ADVISORY only.
- **MoF watch:** JPY trio blocked all W24. Post-BoJ (06-15/16) washout = A+ setups for W25
  (eurjpy squeeze long 183–184; gbpjpy washout 211–213; usdjpy dip 158–159 if calm holds).

## Last Session
2026-06-11 PM (**first /weekly for all 7 new pairs — W24 mid-week**, operator request): pulls
refreshed; zones published audusd (SHORT 0.7065–0.7110 7.0 + counter LONG 0.6940–0.6996 7.0),
nzdusd (SHORT 0.5855–0.5890 6.5 + counter LONG 0.5750–0.5790 7.5), usdcad (LONG 1.3885–1.3905
7.0; short VETOED ADX 32.3), usdchf (LONG 0.7945–0.7960 7.5 + counter SHORT 0.8005–0.8030 5.5).
**JPY trio = NO ZONES — active MoF intervention regime** (web-confirmed: Apr-30 intervention
~160.7, Katayama + Mimura jawboning into June; usdjpy spot 160.5 in trigger zone; crosses hard-
blocked in sympathy). 🔧 **nzdusd bad tick repaired**: D1 2026-04-29 high 1.71632 → 0.58853
(provider error; ADX was falsely 79.6 → true 18.5 RANGING); pull recomputed. yield_environment
+FX-pairs section updated. All zones PENDING — /validate gates orders.
2026-06-11 (expansion, GBPJPY #7 — LAST, D024 COMPLETE): GO extension-fade SHORT-dominant; NO
calm engine; macro NONE; COT DISABLED (no cross contract); one-leg macro generalized (SONIA).
Detail → `wiki/research/gbpjpy/signal-results.md` + decisions.md D024.
2026-06-11 (expansion, EURJPY #6 — first cross-JPY): GO symmetric mean-reversion + calm-drift;
macro NONE; H1 fade works (unlike usdjpy); one-leg ECB branch built.
Detail → `wiki/research/eurjpy/signal-results.md`.
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
