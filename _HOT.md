# _HOT — Session State
*Always current. Updated at end of every session.*

## System Status — v2 ACTIVE (2026-06-02)
Project restarted as **structured + AI-analysis high-quality entry signal generation** (XAUUSD only).
- Markdown-only: Claude writes forecasts/validations directly (no DB).
- Unit: **Trading Zone** (max 3/week, ≤1 counter), Zone Confluence (max 10, floor 5).
- Entry Confluence (max 10, floor 5; E0 confirmation 3pt). New SL/TP/offset (see constitution).
- **R1 (Zone Confluence) + R2 (Entry Confluence) APPROVED + ACTIVE** in `confluence_criteria.md`.
  Pin tail ratio = ≥2.5×body. Ready for first v2 `/weekly`.

## Multi-Instrument Expansion (2026-06-09) — IN PROGRESS
Adding **EURUSD + GBPUSD** alongside XAUUSD. Pipeline is now multi-instrument.
- **P1 DONE** — shared FX base config `scripts/config/_fx_base.py`; `config/eurusd/config.py` + `config/gbpusd/config.py`; registered in `REGISTERED_INSTRUMENTS`. Backfilled 2022→now (1day/4h/1h). `fetch.py`/`compute.py --instrument eurusd|gbpusd` produce clean snapshots.
- **P2 DONE** — pluggable macro block (`MACRO_MODE`): gold=`real_yield` unchanged; FX=`rate_diff` = US 2Y (DGS2) slope direction + policy diff (DFF − ECBDFR/SONIA) carry gate. COT parametrized (EUR=6E, GBP=6B). ETF disabled for FX. Lot sizing TICK_MULTIPLIER=100000 verified.
- **P3 DONE (analysis)** — built `scripts/backtest_signals.py` (multi-instrument, extended catalogue: Connors RSI2, z-score, Keltner, TTM squeeze, Aroon, Supertrend, PSAR, ROC, ATR-pctile, big-figure, engulf/pin, 2s10s, carry-diff slope). Validated vs gold. Ran both pairs 2022→now D1/H4/H1. Backfilled FRED DGS2/ECBDFR/IUDSOIA/DGS10 full history (were stub-length). Results: `wiki/research/{eurusd,gbpusd}/signal-results.md` + `signal-scan-raw.txt`.
  - **🔑 EURUSD + GBPUSD are MEAN-REVERTING — inverse of gold.** Fade oscillator/band/structure extremes; trend-following (EMA/ADX/Supertrend/PSAR/Aroon) is measured ANTI-edge (many t<−2.6). EUR richest on H4 (RSI>70 short +10pp t=4.66); GBP on D1 reversal (near-20d-low long +13.8pp t=4.61) + H1 oscillators.
  - **DEEP-BACKFILL DONE** — D1 now 2010→now (16yr, 4279 bars); H4/H1 to 2020 (TD free intraday cap); DXY to 2009. Re-ran all scans (`--since 2010-01-01`).
  - **🔑 Macro REVIVED on 16yr (was null on 2022-only = regime artifact):** **DXY 1d jump>0.5 → SHORT the pair is the strongest signal found (EUR +23pp t=9.29, GBP +18pp t=7.27).** US2Y(DGS2) 20d slope now significant (t≈2.1–2.4). VIX 1d spike>3 → pair DOWN (risk-off USD bid; GBP −22pp t=−5.60) = SHORT gate. **Carry-diff + 2s10s stay DEAD (t<0.3).**
  - **Confluence APPROVED + ACTIVE (D021, 2026-06-09)** with scored macro/intermarket gate (DXY-jump, US2Y slope, VIX-spike). `wiki/system/{eurusd,gbpusd}/confluence_criteria.md`.
- **P4 DONE** — `{eurusd,gbpusd}_profile.md` written (TICK_MULTIPLIER 100000, pip econ, ATR regimes from 16yr, V1b 5/6 pips, sessions, events, FX VIX-veto-LONGS). Constitution generalized: multi-instrument table, lots=$2000/(SL×TICK_MULTIPLIER), MIN_BAR_RANGE/V1b/baseline/veto parametrized. D001 superseded by D021.
- **P5 DONE** — `/weekly` + `/validate` command docs parametrized by `[instrument]` (Step-0 param table, branched macro + per-pair R1/R2 + FX VIX-veto-longs + DXY-jump block). `check_v1b.py` FX display fixed (5dp) + `--buffer` per pair. Per-instrument forecast dirs created (`forecasts/{weekly,daily}/{eurusd,gbpusd}/`). Smoke-tested check_v1b + validate macro branch on eurusd. **Legacy `.venv/bin/python` in weekly.md replaced with `pyrun.sh`.**
- **READY + LIVE:** first `/weekly eurusd` + `/weekly gbpusd` published (W24). Templates now carry `instrument` field.

## FX Active Forecasts — 2026-W24 (PENDING, mean-reversion)
Both generated Tue 2026-06-09 (mid-week instantiation; re-anchor next Sunday). Bearish bias both
(USD strength: US2Y rising, DXY +0.75% wk, VIX spiked +6 to 21.5 → short bias + LONG veto). Strategy =
**sell the bounce into resistance** (limits rest ABOVE spot; do not chase the low). **CPI Wed 06-10 = hard block.**
- **EURUSD** [W24](forecasts/weekly/eurusd/2026-W24.md): PRIMARY SHORT **1.1618–1.1640** (ZC 7.5), SECONDARY SHORT **1.1574–1.1593** (ZC 6.5). Counter NONE (VIX veto). Spot 1.1539, RSI 35.9.
- **GBPUSD** [W24](forecasts/weekly/gbpusd/2026-W24.md): PRIMARY SHORT **1.3400–1.3447** (ZC 8.0), SECONDARY SHORT **1.3370–1.3390** (ZC 6.5). Counter NONE (VIX veto). Spot 1.3350, RSI 40.1, ADX 16.1.
- **EURGBP** [W24](forecasts/weekly/eurgbp/2026-W24.md): **NEUTRAL/range** (ADX 13.8, 0.8614–0.8682). PRIMARY LONG **0.8608–0.8624** (ZC 8.0), SECONDARY SHORT **0.8664–0.8682** (ZC 7.5). Counter NONE. Spot 0.86352 mid-range, RSI 43.7. First eurgbp forecast (D023). Fade both edges; macro non-scoring; **NO VIX-veto**; sizing USD; route via netting ledger.
- To place orders: `/validate eurusd` / `/validate gbpusd` / `/validate eurgbp` each morning (need price at a zone + oscillator-extreme reversal confirm). No FX orders placed yet.
- **06-09 13:47 UTC `/validate all` (scheduled NY-session) — ALL FX ZONES = ❌ NO TRADE (PENDING held).** EUR EC 2.0/10 (H4 RSI 37.2 not OB, ADX 39.3 trending, price below short zones); **GBP EC 4.5/10 — NOW 0.5 SHORT: price rallied INTO primary short zone $1.3400–1.3447 (H1 high 1.34080), H1 RSI 87.3 extreme OB, ADX 24.9, compression — only missing E0 (no confirmed bearish H1 reversal close yet). WATCH for a close-confirmed 1H pin/engulf at ~1.340 → E0 +3.0 → 7.5 ORDER LIMIT**; EURGBP first validate — both zones NO TRADE (LONG 4.5 / SHORT 3.0, spot 0.86329 mid-range, at neither zone). Hard blocks all pass (V1/V1b intact, V3 clear=CPI Wed, VIX 18.92 fresh→no veto, DGS2/rate-diff flat, DXY 1d −0.321). Files: [eurusd](forecasts/daily/eurusd/2026-06-09.md) / [gbpusd](forecasts/daily/gbpusd/2026-06-09.md) / [eurgbp](forecasts/daily/eurgbp/2026-06-09.md).
- **06-09 05:36 UTC `/validate all` — BOTH PAIRS, ALL 4 ZONES = ❌ NO TRADE (PENDING held).** EUR EC 2.0/10 (RSI oversold not OB, ADX 39.3 trending); GBP EC 3.0/10 (D1 RSI 41.6, H1 RSI 64.0 shy of >65). Price below all short zones — no fade setup. Hard blocks all pass (V1/V1b intact, V3 clear=CPI is Wed, VIX stale→veto suspended, DGS2 0 drift, DXY 1d −0.119). Files: [eurusd](forecasts/daily/eurusd/2026-06-09.md) / [gbpusd](forecasts/daily/gbpusd/2026-06-09.md).
- Known: backfill forward-catch-up throws non-fatal `No data available` at the future/weekend edge — data lands fine.
- EURUSD DXY near-circular (EUR=58% of DXY) — context only, weight in P3. GBP cleaner (~12%).

## FX Currency-Leg Netting — ACTIVE (2026-06-09, D022, Architecture A)
EURUSD/GBPUSD/EURGBP = triangle (`EURGBP=EURUSD/GBPUSD`). Two majors share USD leg → simultaneous
orders concentrate on ONE factor. **FX risk unit = $2000 per currency-factor, not per instrument.**
Gate at `/validate`: other major already live today → **keep best, drop weaker** by Entry
Confluence (loser = ❌ SKIP, stays PENDING; emit `> [!warning] Concentration:` callout). Same dir →
doubled-USD bet; opposite → EURGBP-cross bet. EURGBP reference-only (never traded). Gold NOT netted.
Full framework + Architecture B roadmap: `wiki/system/core/currency_exposure.md`.
- ⚠️ **Latent now:** both W24 FX forecasts are SHORT → SHORT+SHORT = **2× long USD** if both fill.
  Today both = NO TRADE so not yet exposed; gate engages the moment both reach ORDER LIMIT.

## EURGBP Onboarding (2026-06-09) — EG0 + EG1 + EG3 DONE; EG3 = GO
Adding EURGBP as tradable (plan in `wiki/system/core/currency_exposure.md` "Architecture B / onboarding").
- **EG0 DONE** — `scripts/fx_exposure.py` FX netting ledger (Architecture B core). USD + EURGBP-cross
  risk axes, $2000/axis cap, keep-best-drop-weaker gate. Selftest PASS. **Prereq for trading EURGBP**
  (EURGBP = the cross factor → would stack on an implied cross without the ledger).
- **EG1 DONE (D1)** — `config/eurgbp/config.py` (cross; no USD leg; macro PLACEHOLDER; COT off);
  registered in `weekly_pull` + `backtest_signals`. D1 data 2010→now (4287 bars). ⏳ H4/H1 pull
  stalled (backfill edge-loop bug — D1 fine).
- **EG3 DONE = GO (D1)** — `wiki/research/eurgbp/signal-results.md`. Strongly mean-reverting (same as
  majors): near-20d-low long +9.3pp t=4.61, Keltner-low +11.9 t=4.51, RSI<30 +16.7 t=3.32; trend-follow
  = anti-edge. Edge clears cost: D1 ATR 25–41 pips, spread 1–1.5 pip = 6–10% of edge (~10×). Macro
  rows dead (placeholder, wrong for cross) → confirms EG2 rebuild needed.
- **EG2 DONE = macro THIN/DEAD** — built cross model `MACRO_MODE="cross_rate_diff"` (ECBDFR−SONIA,
  X-series in `backtest_signals`); DXY gated off for cross. Backtest D1: all 20d rate slopes noise;
  only X3 diff-widen (t=1.50) + E16 VIX-spike (t=1.68) hint, sub-significant. Data limit (no free
  daily German/UK market yields). ⇒ **EURGBP confluence = price/structure mean-reversion; macro =
  LOW-weight tilt, NOT a gate.** 🔑 **VIX polarity INVERTED vs majors** (risk-off → EURGBP UP) →
  FX VIX-veto-LONGS does NOT apply to EURGBP (key EG4 input). EG2b optional: wire Bund–Gilt daily.
- **EG4 DONE (DRAFT)** — `wiki/system/eurgbp/eurgbp_profile.md` + `confluence_criteria.md`. Low-vol
  ATR regimes (16yr D1: normal 47–76 pips, ~half a major). 🔑 **GBP-quoted sizing fix**: `lots =
  $2000/(SL×100000×GBPUSD_spot)` — uncorrected is ~35% oversized; config `SIZING_FX_CONVERT=True`,
  EG5 implements. Constants: MIN_BAR_RANGE 2pip, V1b 4pip. R1/R2 = mean-reversion fade (Z1 structure
  3.0 + Z2 D1 osc 2.5 mandatory), macro demoted to 0.5 tilt, **NO VIX-veto**, **European event
  blocks** (ECB/BoE/UK/EZ; US = caution only). H1 rows (Z3/E2) PROVISIONAL — need H4/H1 pull.
  Constitution multi-instrument table + EURGBP column added.
- **EG5 DONE** — wired EURGBP into both command docs. `weekly.md`: instrument {…,eurgbp}, Step-0 row,
  cross macro note, Z-table (Z1 3.0/Z2 2.5/macro 0.5 tilt), no-veto, frontmatter (`baseline_rate_diff`,
  `gbpusd_spot`). `validate.md`: Step-0 row (TICK×GBPUSD convert, 2pip/4pip, veto NONE), macro python
  branch (ECBDFR−SONIA diff + loads gbpusd_spot), DXY skipped, **GBP→USD lot-sizing conversion**
  `lots=2000//(SL×100000×gbpusd_spot)`, European event blocks (US=caution), eurgbp R2 row, **FX netting
  gate** (run `fx_exposure.py` before any FX order). `forecasts/{weekly,daily}/eurgbp/` created.
  Smoke-tested: macro diff −1.731 (flat, dead-confirmed), gbpusd_spot 1.33631, sizing 5→4 lots
  (uncorrected $2339 → corrected $1871), check_v1b accepts eurgbp.
- **Sizing = USD, NO GBP convert (operator decision 2026-06-09).** Reverted the GBP→USD pip
  conversion across config/validate/profile/confluence/constitution. EURGBP sizes like the majors:
  `lots = $2000/(SL×100000)`. Caveat noted: assumes broker settles EURGBP pips in USD (if GBP, ~33%
  over — revisit). `SIZING_FX_CONVERT=False`.
- **Backfill bug FIXED (2026-06-09)** — `backfill_twelvedata.py`: (1) backward progress-guard (stop
  when `first_dt` stops decreasing → no more 2010-edge infinite loop), (2) forward-only now catches
  the "No data available" edge error gracefully (was a traceback). Verified backward guard stops.
- **H4/H1 PULLED + VALIDATED** (H4 9785, H1 39217 bars, 2020→now). Intraday confirms mean-reversion
  both directions: H1 RSI<30 long +7.7 t=6.47, %R<−80 long t=7.42, RSI>65/Stoch>80 short t≈3.4; H4
  RSI<30 long t=3.36, Stoch>80 short t=3.54. Z3/E2 H1 rows VALIDATED (short side, thin on D1, is
  significant on intraday). **Confluence flipped DRAFT→ACTIVE.**
- ✅ **EURGBP ONBOARDING COMPLETE (EG0–EG5 + data).** Confluence ACTIVE, all docs/code wired, netting
  ledger enforced, sizing USD (no convert). **Ready for first `/weekly eurgbp`** — no zones published
  yet. Optional later: derived 6E/6B COT, EG2b Bund–Gilt macro gate.

## Open Position
None

## Active Forecast
[2026-W24](forecasts/weekly/xauusd/2026-W24.md) — **BEARISH / MEDIUM-HIGH, conviction HIGH.** Sell bounces into resistance; price ~$4185 in strong downtrend (ADX 48), now ~$180 below primary short zone — zones far OTM, re-anchor likely Sunday.

### LIVE ORDER LIMITS — NONE (2026-06-10 02:14 UTC `/validate all`, CPI day = V3 HARD BLOCK)
- **No live XAUUSD limits.** Yesterday's two SELL limits expired 06-09 21:00 UTC and were **NOT re-placed** — V3 CPI hard block (May CPI 12:30 UTC, within 2h NY open) + gold sold off to ~$4185, now ~$180 below the primary short zone.
- **PRIMARY SHORT** [9.5/10] box **$4367–$4390** — PENDING (not invalidated; far OTM). Invalidate: D1 close > $4390.
- **SECONDARY SHORT** [9.5/10] box **$4450–$4485** — PENDING. Invalidate: D1 close > $4485.
- COUNTER — NONE.
- ⚠️ Gold trending hard down (D1 close $4217.73, ADX 48, RSI D1 24.6). Zones increasingly far out-of-money → likely re-anchor at Sunday `/weekly` if no retrace. T5 DFII10 drift now +0.10% (baseline 2.11 → 2.21; another +0.05% forces a re-forecast).

## Week Status
- Week: 2026-W24
- Trades taken: 0 (no live orders — all canceled/expired on CPI day)
- Risk allocated: $0 (XAUUSD limits expired 06-09 21:00 UTC, not re-placed; 0 FX orders)
- weekly_reforecast_count: 0

## Pending Actions
- **`/validate` daily 07:30 UTC** — re-validate each morning. No limits currently live.
- **CPI TODAY 2026-06-10 12:30 UTC = ACTIVE V3 HARD BLOCK** — all US-event instruments NO TRADE through the CPI window. PPI Thu, UMich Fri = caution. Re-validate post-CPI for fresh setups.
- Watch CPI cool-print squeeze risk (oversold across TFs = bounce risk) — sell the bounce, don't chase.
- **Watch T5 macro drift:** DFII10 now **2.21** vs baseline 2.11 = **+0.10%** (WITH bias). Another ~+0.05% (>0.15% total) forces a re-forecast even though bias-supporting.
- **EURGBP WATCH:** primary LONG (0.8608–0.8624) developing — H4 RSI 15.6 oversold, price ~3 pips above support. Needs D1 oversold + price in-zone + bullish E0 to trigger.
- **FX netting gate (D022):** when EURUSD AND GBPUSD both reach ✅ ORDER LIMIT same day → apply leg netting, keep higher-EC zone at $2000, SKIP the other. Currently both SHORT = 2× USD if unnetted.

## Last Session
2026-06-10 (02:14 UTC, pre-London `/validate all` — XAUUSD + EURUSD + GBPUSD + EURGBP). Data pulled
02:14 UTC. **CPI DAY (US May CPI 12:30 UTC, confirmed via BLS) = V3 HARD BLOCK** for all three US-event
instruments. **ALL ZONES ACROSS ALL 4 INSTRUMENTS = ❌ NO TRADE; all held PENDING (none invalidated).**
- **XAUUSD** spot $4184.62 — gold sold off ~$148 overnight, now ~$180 below primary short zone; D1 close
  $4217.73, ADX 48, RSI D1 24.6 (deeply oversold, strong downtrend). EC 6.0 but V3 overrides. Yesterday's
  2 SELL limits expired 21:00 UTC, NOT re-placed (CPI). No re-forecast (T3 move is WITH bias not counter;
  T5 drift +0.10% <0.15; **precondition 3 FAILS — CPI <12h**, so re-forecast blocked regardless).
- **EURUSD** spot 1.15400 below both short zones; RSI not OB, ADX D1 39.6 trending → EC 2.0. NO TRADE + V3.
- **GBPUSD** spot 1.33766 (inside secondary zone 1.3370–1.3390) but yesterday's OB bounce FADED (H1 RSI
  87→35) → EC dropped 4.5→3.0. NO TRADE + V3.
- **EURGBP** spot 0.86273 — **closest setup**: ~3 pips above LONG support zone with H4 RSI 15.6 deeply
  oversold, but D1 osc (mandatory) not extreme + not in-zone + no E0 → EC 4.5. NO TRADE. US CPI = caution
  only for cross (no hard block); no VIX veto; no UK/EZ event today. **WATCH** for D1 oversold + price into
  0.8608–0.8624 + bullish E0.
- All hard blocks else pass (V1/V1b intact all 4; VIX 18.92 falling/stale; DXY 1d −0.053; DGS2 −0.02 drift).
  No FX orders → netting gate not engaged. Wrote all 4 daily files. **Re-validate post-CPI / tomorrow AM.**
2026-06-09 (13:47 UTC, scheduled NY-session `/validate all` — XAUUSD + EURUSD + GBPUSD + EURGBP) — Data
pulled 06-09 13:41 UTC. **XAUUSD** spot $4332.21 (oversold bounce, RSI D1 26.3, ADX 43.1), well below both
SHORT zones. All hard blocks pass (V1/V1b intact — last D1 close $4316.93; V3 CPI is Wed; VIX 18.92 FRESH 06-08
→ veto cleanly off; DFII10 +0.08% WITH bias <0.15). No re-forecast triggers. Both zones 6.0/10 (no E0) →
**refreshed both midpoint SELL limits**: H4 ATR firmed to $42.48 so SL $46.05→$46.45, lots 0.43, PRIMARY
$4415.34→$4415.66, SECONDARY $4504.34→$4504.66 (~$3,995 risk). **FX: all zones ❌ NO TRADE** — EUR EC 2.0/10
(price below short zones, H4 not OB, ADX 39.3 trending); **GBP EC 4.5/10 = NOW NEAR-TRIGGER — price rallied into
primary short zone $1.3400–1.3447 (H1 high 1.34080), H1 RSI 87.3, ADX 24.9, only E0 missing; WATCH for a
close-confirmed bearish H1 reversal → 7.5 ORDER LIMIT**; EURGBP first validate (LONG 4.5 / SHORT 3.0, spot 0.86329
mid-range, at neither zone). No FX orders placed → netting gate not engaged. Wrote all 4 daily files.
2026-06-09 (05:36 UTC, `/validate all` — XAUUSD + EURUSD + GBPUSD) — Pulled LIVE bars to 06-09 05:36 UTC.
**XAUUSD** spot $4341.24 (oversold bounce, RSI D1 26.3, ADX 43.1), still well below both SHORT zones. All hard
blocks pass (V1/V1b intact — last D1 close $4316.93 < zone tops; V3 clear — CPI is Wed; VIX 21.51 STALE 06-05 →
veto suspended; DFII10 +0.08% WITH bias <0.15 no flip). No re-forecast triggers. Both zones 6.0/10 (no E0) →
**refreshed both midpoint SELL limits**: H4 ATR eased to $41.69 so SL $46.46→$46.05, lots 0.43, PRIMARY
$4415.67→$4415.34, SECONDARY $4504.67→$4504.34 (~$3,960 risk). **EURUSD + GBPUSD: all 4 short zones ❌ NO TRADE**
(price below resistance, no overbought fade extreme — EUR EC 2.0/10 RSI oversold+ADX 39.3 trending; GBP EC 3.0/10
D1 RSI 41.6, H1 RSI 64.0 just shy of >65); hard blocks all pass, zones held PENDING. Wrote daily files for all three.
2026-06-09 (01:46 UTC, pre-London `/validate`) — Pulled LIVE bars to 06-09 01:46 UTC. Spot $4335.90
(shallow bounce, still well below both SHORT zones). All hard blocks pass (V1/V1b intact — last D1
close $4335.90 < zone tops; V3 clear — CPI is Wed; VIX 21.51 but STALE 06-05 → veto suspended;
DFII10 drift +0.08% WITH bias, <0.15 no flip). No re-forecast triggers (T1 +0.08<0.10, T2/T3 tiny,
T4 NFP-VIX spike already absorbed, T5 0.08<0.15). Both zones score **6.0/10 (no E0)** → **refreshed
both midpoint SELL limits**: H4 ATR eased to $42.50 so SL $49.14→$46.46, lots 0.40→0.43, PRIMARY
$4417.81→$4415.67, SECONDARY $4506.81→$4504.67 (~$3,996 risk). Wrote `forecasts/daily/xauusd/2026-06-09.md`.
2026-06-08 (13:20 UTC, scheduled NY-session `/validate`) — Pulled LIVE bars to 06-08 13:20 UTC. Spot
$4324 (still well below both SHORT zones). All hard blocks pass (V1/V1b intact — last D1 close $4324 <
zone tops; V3 clear — CPI is Wed; VIX 15.4 no veto; DFII10 0 drift). No re-forecast triggers; gold moved
further in-bias. Both zones score **6.0/10 (no E0)** → **refreshed both midpoint SELL limits**: H4 ATR
eased to $48.86 so SL $51.08→$49.14, lots 0.39→0.40, PRIMARY $4419.36→$4417.81, SECONDARY
$4508.36→$4506.81 (~$3,931 risk). Rewrote `forecasts/daily/xauusd/2026-06-08.md` (superseded the 08:06 run).
2026-06-08 (08:06 UTC, scheduled London-session `/validate`) — Rebuilt `.pydeps` in fresh sandbox
(`pyrun.sh --setup`), pulled LIVE bars to 06-08 08:00 UTC. Spot $4295 (still falling away from
zones). All hard blocks pass (V1/V1b intact, V3 clear — CPI is Wed, VIX 15.4 no veto, 0 macro drift).
No re-forecast triggers; weekend gap +0.318% (note-only). Both zones score **6.0/10 (no E0)** →
**refreshed both midpoint SELL limits**: H4 ATR rose to $51.08 so SL $48.26→$51.08, lots 0.41→0.39,
PRIMARY $4417.11→$4419.36, SECONDARY $4506.11→$4508.36 (~$3,984 risk). Rewrote
`forecasts/daily/xauusd/2026-06-08.md` (superseded the 03:08 run).
2026-06-08 (earlier) — Fixed pipeline for the Linux scheduled sandbox: added `scripts/pyrun.sh` launcher
(macOS `.venv` → system python3 + persistent `.pydeps` fallback), built `.pydeps` (yfinance etc.),
patched CLAUDE.md + .gitignore. `.claude/commands/*.md` are write-protected so the launcher
convention lives in CLAUDE.md. Re-ran `/validate` on **LIVE data** (bars to 06-08 03:00 UTC):
all hard blocks pass, no re-forecast triggers, both zones score **6.0/10 (no E0)** → **placed two
midpoint SELL limits** (PRIMARY $4417.11, SECONDARY $4506.11; SL $48.26 / 0.41 lots each; ~$3,957
risk). Spot fell to $4310 (away from zones) — resting catch-the-bounce limits. Wrote
`forecasts/daily/xauusd/2026-06-08.md`.
- RESOLVED 2026-06-09: forecast files now named by **trade week**, not run week. Gold Sun-06-07 run
  forecasts Mon-06-08 = W24 → renamed `2026-W23.md`→`2026-W24.md`, matching the FX W24 files + the
  `weekly_pull_2026_W24.txt` pull. Rule codified in `.claude/commands/weekly.md` (WNN = target week).
2026-06-07 — First v2 `/weekly` (W23). Published 2 SHORT zones (Primary $4367–$4390, Secondary
$4450–$4485, both 9.5/10), no counter. BEARISH MEDIUM-HIGH / conviction HIGH after NFP-shock −5.08%
week. Rewrote yield_environment (W23), updated _INDEX. CPI Wed 06-10 hard block flagged.
