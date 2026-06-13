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
convert (operator). FX netting: `scripts/fx_exposure.py` gate at /validate (D022). Known: backfill
catch-up throws non-fatal "No data available" at weekend edge — data lands fine.

## Active Forecasts — 2026-W24
- **XAUUSD** [W24](forecasts/weekly/xauusd/2026-W24.md) — BEARISH/MEDIUM-HIGH, conviction HIGH.
  PRIMARY SHORT $4367–$4390 (9.5), SECONDARY SHORT $4450–$4485 (9.5), no counter. Spot ~$4080
  (fell further), ADX 42 — zones now ~$309–404 OTM, unreachable, re-anchor at next /weekly.
  Invalidate: D1 close > zone top (not breached).
- **EURUSD** [W24](forecasts/weekly/eurusd/2026-W24.md) — SHORT 1.1618–1.1640 (7.5) + 1.1574–1.1593 (6.5). Spot 1.1549.
- **GBPUSD** [W24](forecasts/weekly/gbpusd/2026-W24.md) — SHORT 1.3400–1.3447 (8.0). Spot 1.3401 IN ZONE.
  ~~SECONDARY 1.3370–1.3390~~ **INVALIDATED 06-12 (V1: D1 close 1.34144 > top)**.
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

## Live Order Limits — 1 (2026-06-12 07:30 UTC, `/validate all`)
**USDCHF: BUY LIMIT 0.79477 | 8.23 lots | SL 0.79234 | TP1 0.80085 (2.5R man) | TP2 0.80206 (3.0R
limit) | BE @1.5R | expires 06-12 21:00 UTC.** EC 6.5/10 at floor 6.5 (E0 1H pin 0.79647 off zone
top, DXY slope live; E1/E3 absent — marginal). Structural anchor 0.80063 = 2.41R (< TP1, operator
option). Netting: INDEPENDENT. All other zones ❌ NO TRADE; gbpusd SECONDARY ❌ INVALIDATED (V1).
> [!warning] **ECB HIKED 25bp → 2.25% on 06-11** (first since 2023, Iran-war inflation; ~fully
> priced, EUR muted). Cycle reversal = EUR-bullish vs W24 SHORT bias → **eurusd conviction capped
> MEDIUM** (Contradiction Protocol); eurgbp LONG side favored. Reassess EUR bias at next /weekly.
> [!warning] **XAUUSD T3 RE-FORECAST TRIGGERED 06-12**: +4.21% 1d counter (4049→4220, Iran
> safe-haven) vs BEARISH bias. Zones 187–270 OTM. **Re-run /weekly xauusd before any gold order.**

## Week Status
- Week: 2026-W24 | Trades: 0 | Risk allocated: $0 | weekly_reforecast_count: 0

## Pending Actions
- **USDCHF BUY 0.79477 live** — cancel if unfilled by 21:00 UTC (Friday, no weekend carry). If
  filled: BE +1.5R, TP1 2.5R manual; structural anchor 0.80063 (2.41R) = alt full exit.
- **xauusd: T3 re-forecast required** before any gold order (+4.21% counter, zones unreachable).
- **usdcad: VIX abort watch** — last close 22.22 >20 (stale 06-10). VIX>20 at next fresh print →
  INVALIDATE the 1.3885–1.3905 LONG at /weekly. Zone 78p OTM, D1 RSI 74.
- UMich today 14:00 UTC caution. W25: BoJ 06-15/16, FOMC 06-16/17, SNB+BoE 06-18 — heavy CB week,
  expect V3 blocks Mon–Thu.
- **T5 drift watch:** DFII10 2.21 vs baseline 2.11 = +0.10 (WITH bias); >0.15 forces re-forecast.
- **GBPUSD watch:** spot IN primary zone 1.3400–1.3447, H4 Stoch 83 — bearish E0 → 6.0 ≥ floor → order.
- **EURGBP watch:** ECB hike favors LONG 0.8608–0.8624 — needs zone touch + D1 oversold + bullish E0.
- **MoF watch:** JPY trio no zones W24. Post-BoJ (06-15/16) washout = A+ W25 setups (eurjpy 183–184;
  gbpjpy 211–213; usdjpy 158–159 if calm holds).
- **Shadow ledger:** /weekly MUST `zone_ledger.py add` per zone + `zone_outcomes.py --week` for prior
  week. ⚠ Verify RBNZ H2 + SNB Sep/Dec dates in cb_calendar JSON (estimated/TBC).

## Last Session
2026-06-13 PM (**indicator backtest, scoring audit**): ran `backtest_signals.py --all --tf D1 H4
--since 2015` on the 8 D025 indicators → `wiki/research/general/indicator-backtest-2026-06.md`.
Verdict: Stoch/W%R/CCI/Keltner ✅ confirmed (mean-rev FX, already scored); Donchian/Supertrend/PSAR
❌ anti-edge FX (already excluded); TTM marginal; gold D1 oscillators dead. 3 fix candidates → only 1
real: **usdjpy Z5 PSAR dropped** (2015+ t≈0.2, prior 2.36 not OOS) → engulf/pin. CCI/gold MOOT (already correct).
2026-06-13 PM (**TA engine + news store, D025**): closed rubric/engine mismatch — pull now COMPUTES
the confluence oscillators (Stoch/W%R/CCI/Keltner/Donchian/TTM-squeeze/PSAR/Supertrend, D1+H4) with
an EXTREMES line + **BOS/CHoCH market structure** (`structure.py structure_events`) + **time-at-price
VP substitute** for USD-base pairs (`time_at_price`). Were all eyeballed before. Plus **news store**
(`fetch_news` Finnhub → `data/news/headlines.csv`; `check_news.py` pair-filter; NEWS FEED block).
Wired Section 2/3/5 + template + docs. Verified: compute renders all blocks, Stoch cross-check exact
(31.4=31.4), usdjpy tap HTN 158.95. Collect+display only (weights need research scan). **Same
FINNHUB_KEY activates news + econ-cal.**
2026-06-13 (**3 upgrades shipped**): (A) **calibration layer** — `scripts/calibration.py` →
`wiki/system/core/calibration.md` (edge report by instrument/direction/R1/conviction/session, min-n
gated, `--json`); W24 = 1 LOSS (gbpusd SEC −1R) + 3 RUNNING + 11 PENDING → all edges UNPROVEN (n=1).
(B) **/weekly Step 2b Prior-Week Retrospective** (resolve last week + read last forecast + data
surprises → HELD/BROKE/UNTESTED; Section 0 in template) = narrative learning loop. (C) **data adds
#1–4**: econ-calendar `check_econ_calendar.py` (#1/#2 Finnhub, needs `FINNHUB_KEY`; `--retro`
surprises) + JPY `check_intervention_watch.py` (#4, `intervention_watch.json`) — both mandatory gates
in /weekly+/validate; AUD/NZD commodity intermarket (#3, copper/iron-ore/dairy, context-only).
Verified: compile + gates run; intervention HARD_BLOCKs usdjpy@160.5. **NOTE: add FINNHUB_KEY to
.env then `weekly_pull.py --force` to activate #1/#2.** No frontend/DB (deferred). Read calibration.md.
2026-06-12 07:30 UTC (**`/validate all` — 10 instruments**): pulls refreshed; CB calendar clear;
UMich 14:00 = caution only (first non-V3 day of W24). **✅ FIRST ORDER LIMIT: USDCHF BUY 0.79477**
(zone tagged + bounced, EC 6.5 at floor). ❌ NO TRADE: eurusd (ECB-hike conflict→MEDIUM cap),
gbpusd PRIMARY (in zone, no E0 — closest watch), eurgbp, audusd, nzdusd, usdcad (VIX>20 abort),
xauusd (**T3 re-forecast fired**, +4.21%). ❌ INVALIDATED: gbpusd SECONDARY (V1). JPY trio no zones
(MoF). VIX stale (06-10=22.22). Files: `forecasts/daily/*/2026-06-12.md` (all 10).
2026-06-11 PM (**shadow ledger + bad-tick guard + deep review/12 fixes**): `zone_ledger.py` +
`zone_outcomes.py` (W24 seeded 15 zones); `ohlc_store` bad-tick guard; sizing/0.01-lot/ISO-year/UTC/
gap-15M/closed-bars/CB-gate/VP-off-USD-base fixes — detail in `decisions.md` + `forecasts/daily/*/2026-06-11.md`.
