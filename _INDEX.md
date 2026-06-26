# Index — Claude Swing (v2)
*One line per file. Update after every create or significant rewrite.*

## Agent Docs
- `CLAUDE.md` — full operating manual (Claude Code native)
- `AGENTS.md` — Kimi Code CLI entry point; points to `CLAUDE.md`

## System — Core
- `wiki/system/core/constitution.md` — risk, SL/TP/offset, zone rules, re-forecast triggers (v2)
- `wiki/system/core/decisions.md` — key system choices belief log
- `wiki/system/core/currency_exposure.md` — FX currency-leg netting (Architecture A); per-factor risk cap; B roadmap (D022)
- `wiki/system/core/setup_library.md` — recurring zone patterns (grows with experience)
- `wiki/system/core/macro/yield_environment.md` — current Fed posture, real-yield trend, DXY structure
- `wiki/system/core/calibration.md` — AUTO-GEN edge performance (win%/R by instrument/direction/R1/conviction/session, min-n gated); ← `scripts/calibration.py`
- `wiki/system/core/frontend_plan.md` — frontend roadmap (FastAPI read-only over index.db → Next.js + lightweight-charts; localhost, poll 60s; phased Phase 0→5)

## System — XAUUSD
- `wiki/system/xauusd/xauusd_profile.md` — gold drivers, sessions, ATR ranges, sizing
- `wiki/system/xauusd/confluence_criteria.md` — Zone Confluence (R1) + Entry Confluence (R2) (v2, PROPOSED weights)

## System — EURUSD / GBPUSD (ACTIVE, mean-reversion — D021)
- `wiki/system/eurusd/eurusd_profile.md` — EUR drivers, ATR regimes, pip econ, sessions, V1b 5pip
- `wiki/system/eurusd/confluence_criteria.md` — EUR R1/R2, H4-centric fade + macro gate (ACTIVE)
- `wiki/system/gbpusd/gbpusd_profile.md` — GBP drivers, ATR regimes, pip econ, sessions, V1b 6pip
- `wiki/system/gbpusd/confluence_criteria.md` — GBP R1/R2, D1-reversal + H1 + macro gate (ACTIVE)

## System — EURGBP (cross, ACTIVE — onboarding complete, no zones yet)
- `wiki/system/eurgbp/eurgbp_profile.md` — cross profile: low-vol ATR, USD sizing (no convert), no VIX-veto, ECB/BoE event blocks
- `wiki/system/eurgbp/confluence_criteria.md` — EURGBP R1/R2 ACTIVE: mean-reversion fade, macro 0.5 tilt, H1 rows validated

## System — AUDUSD (ACTIVE — D024 pair #1, no zones yet)
- `wiki/system/audusd/audusd_profile.md` — AUD profile: H4-centric fade, NO VIX-veto (level inverted), NO DXY block, RBA/AU/China events, V1b 4pip
- `wiki/system/audusd/confluence_criteria.md` — AUDUSD R1/R2 ACTIVE: H4 fade + VIX-level/US2Y regime tilt

## System — NZDUSD (ACTIVE — D024 pair #2, no zones yet)
- `wiki/system/nzdusd/nzdusd_profile.md` — NZD profile: macro-light squeeze-led fade, weakest edges, NO VIX/DXY/US2Y gates, RBNZ/NZ/GDT events, V1b 4pip
- `wiki/system/nzdusd/confluence_criteria.md` — NZDUSD R1/R2 ACTIVE: squeeze 2.0 + H4 fade; antipodean advisory vs AUD

## System — USDCAD (ACTIVE — D024 pair #3, FIRST USD-base, no zones yet)
- `wiki/system/usdcad/usdcad_profile.md` — USD-base profile: polarity flips (US2Y/VIX/COT), oil tilt, ~28% under-sized CAD pip accepted, BoC/CAD events, V1b 5pip
- `wiki/system/usdcad/confluence_criteria.md` — USDCAD R1/R2 ACTIVE: H4 band/oscillator fade + VIX fade-USD regime; H1 long-side rich

## System — USDCHF (ACTIVE — D024 pair #4, USD-base, no zones yet)
- `wiki/system/usdchf/usdchf_profile.md` — USD-base profile: DXY-slope macro, VIX washout, SNB intervention regime + quarterly block, ~25% over-sized CHF pip accepted, V1b 4pip
- `wiki/system/usdchf/confluence_criteria.md` — USDCHF R1/R2 ACTIVE: H1-centric fade (short cluster t 4.5–5.5) + DXY 20d slope 2.0; H4 thin; SNB short-cap 0.78–0.80

## System — USDJPY (ACTIVE — D024 pair #5, USD-base, FIRST JPY pair, no zones yet)
- `wiki/system/usdjpy/usdjpy_profile.md` — JPY plumbing (pip 0.01, 3dp, TICK 650 static), DXY-slope macro, VIX washout, US2Y dead, NY-session drift, MoF/BoJ intervention regime ≥158, V1b 0.04
- `wiki/system/usdjpy/confluence_criteria.md` — USDJPY R1/R2 ACTIVE, **direction-aware**: LONG drift-continuation (squeeze/calm/dip/NY) / SHORT D1-H4 extreme fade; NO H1-only shorts; BoJ/MoF hard block

## System — EURJPY (ACTIVE — D024 pair #6, FIRST cross-JPY, no zones yet)
- `wiki/system/eurjpy/eurjpy_profile.md` — cross-JPY: pip 0.01/3dp/TICK 650, macro NONE (first 100% price-driven pair), two-sided sessions (London fade-short / NY drift-long), MoF slams hit crosses, COT XRATE direct but thin
- `wiki/system/eurjpy/confluence_criteria.md` — EURJPY R1/R2 ACTIVE: symmetric mean-reversion on long-drift floor — extreme engine 2.5 both sides; NO macro/VIX rows; BoJ/MoF + ECB hard blocks

## System — GBPJPY (ACTIVE — D024 pair #7 LAST, cross-JPY #2, no zones yet)
- `wiki/system/gbpjpy/gbpjpy_profile.md` — cross-JPY #2: pip 0.01/3dp/TICK 650, V1b 0.05 (highest ATR in book), macro NONE, NO calm engine, NY long-only sessions (short anti 13–15 UTC), COT DISABLED (no CFTC cross contract), MoF slams largest
- `wiki/system/gbpjpy/confluence_criteria.md` — GBPJPY R1/R2 ACTIVE: extension-fade SHORT-dominant — extreme engine 2.5, multi-TF alignment 1.5 (replaces dead calm row); NO macro/VIX/calm rows; BoJ/MoF + BoE hard blocks

## Templates
- `wiki/system/templates/weekly_forecast.md` — skeleton for forecasts/weekly/xauusd/YYYY-WNN.md (zones)
- `wiki/system/templates/daily_validation.md` — skeleton for forecasts/daily/xauusd/YYYY-MM-DD.md (entry confluence)
- `wiki/system/templates/paper_review.md` — research paper review template

## Research — EURUSD / GBPUSD (P3 signal scan)
- `wiki/research/eurusd/signal-results.md` — EUR edges: mean-reverting, H4-centric (+ raw scan)
- `wiki/research/gbpusd/signal-results.md` — GBP edges: mean-reverting, D1+H1 (+ raw scan)

## Research — EURGBP (EG3 go/no-go)
- `wiki/research/eurgbp/signal-results.md` — EURGBP cross: mean-reverting (same as majors), edge clears cost → **GO on D1**; macro placeholder dead (EG2 rebuild)

## Research — AUDUSD (D024 pair #1)
- `wiki/research/audusd/signal-results.md` — AUDUSD: mean-reverting H4-centric → **GO**; 🔑 DXY-jump DEAD, VIX LEVEL inverted (VIX>20→long t=6.14) (+ raw scan)

## Research — NZDUSD (D024 pair #2)
- `wiki/research/nzdusd/signal-results.md` — NZDUSD: mean-reverting → **GO marginal** (edges ≈½ AUD); 🔑 US2Y+DXY both DEAD, VIX level weak inverted; squeeze = strongest signal (+ raw scan)

## Research — USDCAD (D024 pair #3 — first USD-base)
- `wiki/research/usdcad/signal-results.md` — USDCAD: mean-reverting → **GO**; 🔑 VIX>20→SHORT (fade-USD t≈3.9), US2Y flipped works, WTI weak tilt, DXY dead; H1 long-side machine (+ raw scan)
- `wiki/research/usdchf/signal-results.md` — USDCHF: mean-reverting → **GO**; 🔑 DXY 20d slope LIVE (t=2.3, only pair beyond EUR/GBP), VIX WASHOUT; H1 short-fade machine (t 4.5–5.5), London LONG drift (+ raw scan)
- `wiki/research/usdjpy/signal-results.md` — USDJPY: **GO, ASYMMETRIC** — NOT the fade template: LONG drift (D1 squeeze t=3.27, H4 calm t=4.51, NY drift t=4.71) / SHORT D1-H4 extremes only; 🔑 H1 fade = ANTI (−3.3); DXY slope live, VIX washout, US2Y dead (+ raw scan)
- `wiki/research/eurjpy/signal-results.md` — EURJPY: **GO, symmetric mean-reversion + calm-drift** — H1 fade works (A9 t=4.21, unlike usdjpy), D1 dip-buy strong (Stoch<20 t=3.10); 🔑 macro NONE (ECB anti, VIX dead); London fade-short / NY drift-long (+ raw scan)
- `wiki/research/gbpjpy/signal-results.md` — GBPJPY: **GO, extension-fade SHORT-dominant** — Keltner-high fade t=4.64/4.01, strongest long-drift floor (D1 LNG 56.7%); 🔑 macro NONE (SONIA ns, VIX dead), NO calm engine (only JPY pair without), NY long-only; carry-trend hypothesis REJECTED — all trend rows anti (+ raw scan)

## Research — Cross-pair
- `wiki/research/general/e0-variants-backtest.md` — E0 trigger bake-off: **oscillator RECLAIM (RSI back through 35/65) beats current pin/engulf — avgR +0.104 vs +0.038, PF 1.15 vs 1.05, wins 7/11 pairs**; band_reclaim wins 2 (incl gold); pin/engulf wins only gbpusd + barely beats raw limit. **IMPLEMENTED D027** (reclaim primary per-pair, pin/engulf fallback; pull `ENTRY TRIGGERS` block via `weekly_pull.entry_triggers_block`; all R2 rows + constitution + validate.md updated) — PENDING live-ledger validation. Script `scripts/backtest_e0_variants.py`
- `wiki/research/general/entry-sim-backtest.md` — E0 Tier-2 entry-sim (MARKET vs offset-LIMIT vs LIMIT+E0; SL=ATR TP=2.5R): **offset beats market avgR/PF 9/11 pairs**, E0 adds on top ~6 pairs (flips audusd/usdcad +) at 22-25% fill. Validates offset+E0 on R (Tier-1 win-rate was blind). Gold/usdjpy fade-reading correctly underperforms. Script `scripts/backtest_entry_sim.py`. Keep as-is, no reweight
- `wiki/research/general/entry-confirm-backtest.md` — E0 (1H pin/engulf) conditional Tier-1: trigger adds **NO win-rate edge** (1 of 66 cells +, 6 −) → confirms "trigger alone no edge"; value is fill-price/R via offset (needs Tier-2 entry-sim). Script `scripts/backtest_entry_confirm.py`. Keep E0 as-is
- `wiki/research/general/indicator-backtest-2026-06.md` — 8-indicator validation (Stoch/W%R/CCI/Keltner ✅ keep, Donchian/Supertrend/PSAR ❌ anti-edge already-excluded, TTM marginal); 2015+ rescan all 11 pairs D1+H4. Applied: usdjpy Z5 PSAR dropped (t≈0.2 dead). CCI/gold gating MOOT (already correct)

## Research — XAUUSD
- `wiki/research/xauusd/_INDEX.md` — data sources, scripts, standards, pending research
- `wiki/research/xauusd/mtf-market-structure.md` — swing trend alignment (HH/HL pivots)
- `wiki/research/xauusd/stop-loss.md` — stop placement: structural vs ATR
- `wiki/research/xauusd/macro-regime.md` — FRED macro vs gold: DFII10, DXY, VIX
- `wiki/research/xauusd/atr-compression.md` — volatility cycle, expansion probability (82%)
- `wiki/research/xauusd/r-target.md` — TP ratio optimization
- `wiki/research/xauusd/session-timing.md` — hour/day/session effects
- `wiki/research/xauusd/independent-signal-results.md` — Phase 0b: gold = momentum; measured edges
- `wiki/research/xauusd/entry-confirmation.md` — H1 trigger ablation: pin+offset PF 3.38
- `wiki/research/xauusd/phase0b_signal_plan.md` — Phase 0b methodology

## Research — Source Papers
- `wiki/research/source/_INDEX.md` — external paper index

## Forecasts — EURUSD / GBPUSD / EURGBP
- `forecasts/weekly/eurusd/2026-W26.md` — BEARISH/MED-HIGH; COUNTER-LONG 1.1420–1.1455 (7.5, MED-LOW); no aligned short qualifies (oversold extreme). W25 dip-buy lost.
- `forecasts/weekly/gbpusd/2026-W26.md` — BEARISH/MED-HIGH; SHORT 1.3380–1.3415 (5.0) + COUNTER-LONG 1.3140–1.3200 (7.0, MED, 20d-low CCI−232). ADX 19 ranging.
- `forecasts/weekly/eurgbp/2026-W26.md` — NEUTRAL; SHORT 0.8682–0.8715 (8.0, MED, best) + LONG 0.8625–0.8645 (5.0). Range shifted up (CHoCH), TTM squeeze ON.
- `forecasts/weekly/eurusd/2026-W25.md` — NEUTRAL/MEDIUM; LONG 1.1500–1.1520 (7.5) + SHORT 1.1618–1.1640 (7.0). ECB hiked 2.25% → bias SHORT→NEUTRAL.
- `forecasts/weekly/gbpusd/2026-W25.md` — NEUTRAL/MEDIUM; SHORT 1.3440–1.3465 (6.5) + COUNTER LONG 1.3304–1.3330 (7.0). TTM squeeze ON; FOMC Wed + BoE Thu block.
- `forecasts/weekly/eurgbp/2026-W25.md` — NEUTRAL(long-tilt)/MEDIUM; LONG 0.8608–0.8625 (8.5, best) + SHORT 0.8660–0.8682 (6.0). ECB favors long; BoE Thu block.
- `forecasts/weekly/eurusd/2026-W24.md` — BEARISH/MEDIUM-HIGH; 2 SHORT fade zones (1.1618–1.1640, 1.1574–1.1593), conviction MEDIUM.
- `forecasts/weekly/gbpusd/2026-W24.md` — BEARISH/MEDIUM-HIGH; 2 SHORT fade zones (1.3400–1.3447, 1.3370–1.3390), conviction MEDIUM.
- `forecasts/weekly/eurgbp/2026-W24.md` — NEUTRAL/range (ADX 13.8); LONG 0.8608–0.8624 (ZC 8.0) + SHORT 0.8664–0.8682 (ZC 7.5), conviction MEDIUM. First eurgbp forecast.

## Forecasts — D024 pairs
- `forecasts/weekly/audusd/2026-W26.md` — BEARISH/MEDIUM; **NO ZONES** (ADX 31.5 trend starves fades; VIX neutral; watch-short 0.7065–0.7095). AU jobs Thu.
- `forecasts/weekly/nzdusd/2026-W26.md` — BEARISH(macro-dead)/LOW; LONG 0.5700–0.5730 (6.0, MED-LOW, deep OS floor). W25 long V1b-stopped → lower zone + reclaim.
- `forecasts/weekly/usdcad/2026-W26.md` — BULLISH/MED-HIGH; **NO ZONES** (RSI 85 blow-off, ADX 41 → short vetoed, long anti-edge; watch-short 1.4180–1.4220). CA CPI Mon.
- `forecasts/weekly/usdchf/2026-W26.md` — BULLISH/MEDIUM; LONG 0.7980–0.8010 (5.0, DXY slope flipped UP) + COUNTER-SHORT 0.8090–0.8130 (5.0). Broke above SNB band.
- `forecasts/weekly/usdjpy/2026-W26.md` — **NO ZONES**: spot 161.3 MoF HARD-BLOCK longs + Katayama jawboning; short lacks D1+H4 extreme.
- `forecasts/weekly/eurjpy/2026-W26.md` — **NO ZONES**: spot 185.1 MoF HARD-BLOCK longs; no short extension (RSI 48 mid); D1 TTM squeeze ON 20b.
- `forecasts/weekly/gbpjpy/2026-W26.md` — NEUTRAL/MED-LOW; LONG 212.00–212.90 (6.0, weak side, intervention CAUTION). Eased from 214.8 to 213.4.
- `forecasts/weekly/audusd/2026-W25.md` — BEARISH/MEDIUM; SHORT 0.7065–0.7110 (6.5) + COUNTER LONG 0.6980–0.7000 (7.0); ADX 28.9 (veto>30); RBA Tue + FOMC Wed block.
- `forecasts/weekly/nzdusd/2026-W25.md` — NEUTRAL; SHORT 0.5855–0.5890 (6.5) + COUNTER LONG 0.5750–0.5790 (6.5, best, D1 OS); squeeze OFF; FOMC Wed.
- `forecasts/weekly/usdcad/2026-W25.md` — BULLISH/MEDIUM; LONG 1.3830–1.3875 (6.0); SHORT ADX-vetoed (34.8>30); RSI 75 OB; FOMC Wed.
- `forecasts/weekly/usdchf/2026-W25.md` — BEARISH/MEDIUM; SHORT 0.8005–0.8025 (8.5, SNB-cap); DXY slope flipped down; FOMC Wed + SNB Thu block; reconcile W24 long.
- `forecasts/weekly/usdjpy/2026-W25.md` — **NO ZONES**: BoJ 06-16 + MoF zone (spot 160.2 >160 trigger) + FOMC.
- `forecasts/weekly/eurjpy/2026-W25.md` — **NO ZONES**: BoJ + MoF zone (185.5) + ECB caution; H4 record-high OB short setup waiting for W26.
- `forecasts/weekly/gbpjpy/2026-W25.md` — **NO ZONES**: BoJ + BoE + MoF zone (214.8, largest cross slams).
- `forecasts/weekly/{audusd,nzdusd,usdcad,usdchf,usdjpy,eurjpy,gbpjpy}/2026-W24.md` — prior week (BEARISH/NEUTRAL/BULLISH per pair; JPY trio NO ZONES). See git/file history.

## Forecasts — XAUUSD
- `forecasts/weekly/xauusd/2026-W26.md` — BEARISH/MED-HIGH; SHORT 4200–4235 (8.5, best, nearer-resistance fix) + SHORT 4300–4340 (7.5). Both macro legs aligned (real-yield↑ + DXY↑). Core PCE Thu.
- `forecasts/weekly/xauusd/2026-W25.md` — BEARISH/MEDIUM; SHORT 4360–4400 (7.5) + SHORT 4450–4485 (7.0). Spot 4215 (Iran bounce); conviction MEDIUM (real-yield vs safe-haven conflict).
- `forecasts/weekly/xauusd/2026-W24.md` — BEARISH/MEDIUM-HIGH; 2 SHORT zones ($4367–$4390, $4450–$4485), conviction HIGH. (renamed W23→W24: files now named by trade week, not run week)

## Daily Validations
- `forecasts/daily/{all 10}/2026-06-11.md` — **`/validate all`, ECB + PPI day, V3 HARD BLOCK** (ECB rate decision 12:15 UTC + US PPI 12:30 UTC, both <2h of NY open). 06:11 UTC run: ALL 10 instruments NO TRADE, all zones held PENDING (structure intact, none invalidated), no re-forecast (T1–T5 sub-threshold). 🔎 ECB decision was MISSED in W24 weekly — flagged. Gold $4080 (zones $309–404 OTM). JPY trio = NO ZONES (MoF). EUR pairs: re-validate after 12:45 presser.
- `forecasts/daily/{xauusd,eurusd,gbpusd,eurgbp}/2026-06-10.md` — **CPI day, V3 HARD BLOCK** (US May CPI 12:30 UTC). 08:06 UTC London run: ALL 4 instruments, ALL zones = NO TRADE, held PENDING, no orders. XAU spot $4162 EC 6.0 (V3 override); EUR 1.1549 EC 2.0; GBP 1.33836 EC 2.0 (in-zone, bounce faded); EURGBP 0.86296 EC 3.0 (above LONG support, D1 osc not extreme).
- `forecasts/daily/xauusd/2026-06-09.md` — both SHORT zones ORDER LIMIT, EC 6.0/10 (no E0, midpoint). 13:47 UTC NY run: SL $46.45, lots 0.43, limits $4415.66 / $4504.66. VIX fresh.
- `forecasts/daily/xauusd/2026-06-08.md` — both SHORT zones ORDER LIMIT, EC 6.0/10 (no E0, midpoint). SL $51.08, lots 0.39.
- `forecasts/daily/eurusd/2026-06-09.md` — both SHORT zones NO TRADE, EC 2.0/10 (price below resistance, ADX 39.3 trending).
- `forecasts/daily/gbpusd/2026-06-09.md` — both SHORT zones NO TRADE, EC 4.5/10 (price IN primary short zone, H1 RSI 87.3, only E0 missing — near-trigger, watch).
- `forecasts/daily/eurgbp/2026-06-09.md` — first EURGBP validate; both zones NO TRADE (LONG 4.5 / SHORT 3.0, spot mid-range).

## Scripts — Pipeline
- `scripts/backtest_signals.py` — multi-instrument signal edge backtest (P3 runner; extended catalogue)
- `scripts/weekly_pull.py` — orchestrator: cache gate → fetch → compute → weekly_pull txt
- `scripts/fetch.py` — network only: TD 15M + FRED → CSVs
- `scripts/compute.py` — indicators + snapshot from CSVs (aux VP/COT/GLD network only)
- `scripts/backfill_twelvedata.py` — one-off util (not in weekly pipeline): pull/update OHLC backward from TD
- `scripts/resample_twelvedata.py` — one-off util (not in weekly pipeline): M15 → H1/H4/D1
- `scripts/backfill_fred.py` — one-off util (not in weekly pipeline): pull/update FRED macro series
- `scripts/backup_db.py` — pg_dump-style gzipped SQL dump of index.db → `data/database/backups/`; `--keep N`; restore `gunzip -c <dump> | sqlite3 data/database/index.db`
- `scripts/db.py` — SQLite helpers: `read_table`/`write_table`/`read_ohlc`/`read_slice`/`sync_slice`/`sync_table`/`last_ohlc_dt`/`last_series_date`/`replace_ohlc_slice` (canonical store access). Connections: WAL + `busy_timeout=30s` + `synchronous=NORMAL` (corruption-hardened, D033)
- `scripts/db_guard.py` — **MANDATORY durability preflight** (Step 0b at /weekly + /validate): `checkpoint`→`check` (PRAGMA quick_check)→`backup` (consistent `VACUUM INTO` gzip, last 7); non-zero exit on corrupt image halts the command before it writes into a bad store. Supersedes `backup_db.py` for routine guarding (D033, after the 2026-06-26 corruption that lost `news` + crashed every replay)

## Scripts — Risk / Portfolio
- `scripts/fx_exposure.py` — FX currency-leg ledger, ADVISORY (D024): all 10 FX instruments / 8 currency legs; flags shared-leg concentration + suggests cleaner trade (highest EC); no caps, no auto-skip. `--selftest` / `--orders` / `--candidate`.

## Scripts — Shadow Ledger (zone outcome tracking, 2026-06-11)
- `scripts/zone_ledger.py` — registry of every published Trading Zone → `zone_ledger` table in `data/database/index.db` (`add` MANDATORY per zone at /weekly publish; `validate` writes the daily verdict/R2/limit back per zone at /validate for the frontend; `list` to inspect)
- `scripts/live_r.py` — recomputes live unrealized R + SL/TP-touch + MFE/MAE for OPEN trades from the latest OHLC (`live_metrics()` reusable by the frontend export). R read off the actual bar that hit SL — fixes the 2026-06-15 stale-R bug. `--tf` / `--include-pending` / `--id`
- `scripts/zone_outcomes.py` — replays 1H/4H/D1 OHLC vs ledger: fill at zone midpoint from publish time, constitution SL, TP1 2.5R / BE 1.5R / SL −1R → `zone_outcome` table + confluence-bucket calibration summary (run for prior week at each /weekly)
- `scripts/calibration.py` — aggregates the `zone_outcome` table → `wiki/system/core/calibration.md` (sliceable edge report: instrument/direction/R1/conviction/session, INSUFFICIENT below `--min-n`, default 10); `--json` side-output; run after `zone_outcomes.py` at /weekly

## Scripts — Validation
- `scripts/check_v1b.py` — V1b intraday H4 invalidation checker (CLI zone args; reads H4 from the `ohlc` table)
- `scripts/check_cb_calendar.py` — central-bank decision-date gate (MANDATORY at /weekly + /validate; reads static JSON; exit 1 = calendar unverified for window)
- `scripts/check_econ_calendar.py` — scheduled data-release gate (#1/#2, MANDATORY; reads the `econ_calendar` table; HIGH-impact releases for the pair's legs; `--retro <week>` = actual-vs-est surprise for Step 2b; exit 1 = no rows/stale)
- `scripts/check_intervention_watch.py` — JPY MoF intervention/jawboning gate (#4, MANDATORY for JPY; spot vs `config/intervention_watch.json` level → HARD_BLOCK/CAUTION; exit 1 = watch stale)
- `scripts/check_news.py` — pair-filtered headline readout from the `news` table (free RSS feeds; context for Section 2 + Step 2b; NOT a gate; D025)
- `scripts/check_structured_news_event.py` — T4-X structured news event check
- `scripts/structure.py` — shared fractal pivots, MTF structure helpers + `structure_events` (BOS/CHoCH labeling) + `time_at_price` (USD-base VP substitute) (D025)

## Scripts — Config & Lib
- `scripts/config/cb_calendar_2026.json` — static central-bank decision dates 2026 (8 banks, hard-block/caution map; RBNZ H2 + SNB Sep/Dec need verification; rebuild every December)
- `scripts/config/intervention_watch.json` — JPY MoF intervention levels + jawboning log (#4; Claude updates jawboning[] from web search each /weekly JPY run; push verified_through forward)
- `scripts/config/_fx_base.py` — shared FX-major defaults (rate_diff macro, COT on, ETF off, TICK 100000)
- `scripts/config/xauusd/config.py` — XAUUSD instrument config (real_yield macro)
- `scripts/config/eurusd/config.py` — EURUSD config (DGS2 + DFF−ECBDFR, COT 6E, VP 6E=F)
- `scripts/config/gbpusd/config.py` — GBPUSD config (DGS2 + DFF−SONIA, COT 6B, VP 6B=F)
- `scripts/config/eurgbp/config.py` — EURGBP CROSS config (EG1; no USD leg, macro PLACEHOLDER pending EG2, COT off)
- `scripts/config/audusd/config.py` — AUDUSD config (D024 pair #1; no daily RBA series → carry leg off, COT 6A, VP 6A=F; COMMODITY iron-ore+copper #3)
- `scripts/config/nzdusd/config.py` — NZDUSD config (D024 pair #2; no daily RBNZ series → carry leg off, COT 6N, VP 6N=F; COMMODITY dairy+copper #3)
- `scripts/config/_fx_usd_base.py` — shared USD-BASE defaults (USD_BETA_SIGN=+1, COT_INVERTED, VP off)
- `scripts/config/usdcad/config.py` — USDCAD config (D024 pair #3; USD-base, OIL_SERIES=DCOILWTICO, COT 6C inverted)
- `scripts/config/usdchf/config.py` — USDCHF config (D024 pair #4; USD-base, no oil leg, COT 6S inverted, SNB carry off)
- `scripts/config/usdjpy/config.py` — USDJPY config (D024 pair #5; USD-base + FIRST JPY: PIP_SIZE 0.01, PRICE_DP 3, TICK 650 static, COT 6J inverted, BoJ carry off)
- `scripts/config/eurjpy/config.py` — EURJPY config (D024 pair #6; FIRST cross-JPY: USD_BETA_SIGN 0, JPY pip plumbing, one-leg macro RATE_GBP=None, COT EUR/JPY XRATE direct)
- `scripts/config/gbpjpy/config.py` — GBPJPY config (D024 pair #7 LAST; cross-JPY #2: one-leg macro live leg = SONIA via RATE_EUR slot + LIVE_LEG_LABEL/BASELINE_LABEL, V1b 0.05, COT disabled — no CFTC cross contract)
- `scripts/lib/ohlc_store.py` — shared OHLC loading/caching utilities + bad-tick guard (auto wick-clamp/bar-drop on upsert, >10% D1 / >5% intraday dev vs rolling-median close; log → `data/{source}/{symbol}/_quarantine.csv`). `upsert` also slice-syncs the merged bars into the `ohlc` table of `data/database/index.db` (fail-soft; CSV stays reader-facing mirror)
- `scripts/db.py` — shared SQLite access for `data/database/index.db`: `read_table`/`write_table` (state registries, DB-canonical + CSV mirror) + `replace_ohlc_slice` (OHLC live sync). All-string round-trip, auto-indexes

## Data
- `data/database/index.db` — **CANONICAL store** (gitignored, written live by `db.py` + `ohlc_store` + `weekly_pull.py`). All
  tabular data now lives here — the source CSVs were migrated + deleted. Tables:
  - `zone_ledger` — published-zone shadow registry (`zone_ledger.py`)
  - `zone_outcome` — R1/zone-quality would-be R per zone, midpoint fill (`zone_outcomes.py`)
  - `trade_outcome` — system P&L: entry-mechanics replay (E0+offset+EC) + gate-accuracy audit
    (`trade_outcome.py` + `entry_confluence.py`/`config/ec_spec.py`). Replaces the retired hand-logged
    `trade` table + `/log` skill (D031 — real book was n≈2, never calibratable)
  - `ohlc` — all OHLC bars, cols source/symbol/tf/datetime/o/h/l/c/v (15min master + resampled
    1h/4h/1day, 11 instruments); written live by `ohlc_store.upsert`; read via `db.read_ohlc`
  - `macro_series` — FRED series (series_id/date/value: DFII10, VIXCLS, DGS2/10, ECBDFR, etc.)
  - `market_series` — yahoo DXY + commodities (source/symbol/date/value)
  - `news` — free-RSS headlines (`check_news.py`); `econ_calendar` — Forex Factory releases
    (`check_econ_calendar.py`); `gld_holdings` — daily GLD tonnage
- `data/database/backups/` — `backup_db.py` gzipped SQL dumps of index.db (gitignored; off-machine copy = DR)
- (removed: `_manifest.json` → last_dt from DB; `_quarantine.csv` bad-tick log + `calibration/summary.json` → derived, regenerate on demand)
- `data/calibration/summary.json` — optional JSON edge summary (`calibration.py --json`)
- `data/weekly_pull/{inst}/` — IMMUTABLE weekly pull text files
- `data/cftc/deahistfo{year}.zip` — COT yearly archives (24h refresh)
- `data/news_events/` — T4-X structured event JSONs
- `forecasts/{weekly,daily}/{all 11 instruments}/` — forecast/validation output markdown

## Frontend (Phase 0 done — 2026-06-16; plan: `wiki/system/core/frontend_plan.md`)
- `api/main.py` — read-only FastAPI over index.db; reuses `scripts/db.py` + `scripts/live_r.live_metrics`; endpoints `/health`, `/positions`, `/gates`, `/zones`, `/forecast`. Run `bash api/run.sh` (127.0.0.1:8000).
- `api/gates.py` — `/gates` gate computation (Phase 1, 2026-06-16); reuses the 3 gate scripts read-only (CB/econ/intervention) → per-instrument blocks + summary + warnings; does NOT modify scripts/.
- `api/zones.py` — `/zones` (zone_ledger⋈zone_outcome → per-instrument zones + derived board_status) + `/forecast` (raw forecast markdown, path-validated under forecasts/) (Phase 2, 2026-06-16).
- `api/charts.py` — `/chart/{inst}?tf=D1|H4|1H|15M` (ohlc candles + overlays: zone bands, trade lines, BOS/CHoCH markers via structure.py, structure state) (Phase 3, 2026-06-16).
- `api/edge.py` — `/edge?min_n=&week=` (reuses calibration.build → sliceable shadow-edge stats + confluence→R scatter + shadow-vs-real divergence) (Phase 4, 2026-06-16).
- `api/macro.py` — `/macro` (9 FRED series latest+Δ1+Δ5 from macro_series) + `/news/{inst}` (pair-filtered headlines reusing check_news keywords) (Phase 5, 2026-06-16).
- `api/requirements.txt` — fastapi+uvicorn (installed into `.venv`, NOT pipeline requirements.txt / sandbox `.pydeps`)
- `frontend/` — Next.js 16 (app router, TS, Tailwind v4, dark-only) cockpit polling /positions+/gates+/zones 60s. `cd frontend && npm run dev` → :3000. `app/page.tsx` (cockpit+gate banner+instrument grid), `components/ZoneBoard.tsx` (zone board + forecast-markdown modal, react-markdown+remark-gfm), `components/PriceChart.tsx` (lightweight-charts v5 candles+zone/trade overlays+BOS/CHoCH markers), `components/EdgePanel.tsx` (calibration stat tables + SVG confluence→R scatter + shadow-vs-real), `components/MacroPanel.tsx` (macro snapshot table + pair-filtered news), `lib/{api,instruments,usePoll}.ts`. **All 5 frontend phases done 2026-06-16.** ⚠ read `frontend/node_modules/next/dist/docs/` before edits (breaking changes vs training data).
