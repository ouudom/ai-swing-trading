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
- To place orders: `/validate eurusd` / `/validate gbpusd` each morning (need a bounce into a zone + bearish reversal confirm). No FX orders placed yet (price below all short zones).
- Known: backfill forward-catch-up throws non-fatal `No data available` at the future/weekend edge — data lands fine.
- EURUSD DXY near-circular (EUR=58% of DXY) — context only, weight in P3. GBP cleaner (~12%).

## Open Position
None

## Active Forecast
[2026-W23](forecasts/weekly/xauusd/2026-W23.md) — **BEARISH / MEDIUM-HIGH, conviction HIGH.** Sell bounces into resistance; price $4330 in strong downtrend.

### LIVE ORDER LIMITS (refreshed 2026-06-09 01:46 UTC pre-London `/validate`, expire 21:00 UTC — re-validate each morning)
- **PRIMARY SHORT** [9.5/10] — box **$4367–$4390**. **SELL LIMIT $4415.67 | 0.43 lots | SL $4462.13** | TP1 2.5R $4299.52 (manual) / TP2 3.0R $4276.29 (limit) / BE@1.5R $4345.98. Entry Confluence 6.0 (no E0, midpoint anchor). Invalidate: D1 close > $4390.
- **SECONDARY SHORT** [9.5/10] — box **$4450–$4485**. **SELL LIMIT $4504.67 | 0.43 lots | SL $4551.13** | TP1 2.5R $4388.52 (manual) / TP2 3.0R $4365.29 (limit) / BE@1.5R $4434.98. Entry Confluence 6.0 (no E0, midpoint anchor). Invalidate: D1 close > $4485.
- COUNTER — NONE (macro MEDIUM-HIGH + no RSI divergence).
- ⚠️ Both resting limits well above spot ($4336, shallow bounce) — fill only on a strong bounce. H4 ATR eased to $42.50 so SL tightened $49.14→$46.46, lots 0.40→0.43. **CPI Wed 06-10 = cancel any unfilled limit within 2h of London/NY open.**

## Week Status
- Week: 2026-W23
- Trades taken: 0 (2 limits placed, unfilled)
- Risk allocated: $3,996 (2 × $1,997.78 unfilled limits)
- weekly_reforecast_count: 0

## Pending Actions
- **`/validate` daily 07:30 UTC** — re-validate/refresh both live limits each morning (expire 21:00 UTC, never carry forward).
- **CPI Wed 2026-06-10 = HARD BLOCK (V3)** — cancel any live limit within 2h of London/NY open. PPI Thu, UMich Fri = caution.
- Watch CPI cool-print squeeze risk (%B below lower band = bounce risk) — sell the bounce, don't chase.
- **Watch T5 macro drift:** DFII10 now 2.19 vs baseline 2.11 = +0.08% (WITH bias). Another ~+0.07% (>0.15% total) forces a re-forecast even though bias-supporting.

## Last Session
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
- NOTE for user: `weekly_pull.py` names today's file `weekly_pull_2026_W24.txt` (ISO week 24) while
  the active forecast is labelled `2026-W23`. Pre-existing week-numbering mismatch — cosmetic for
  /validate (reads CSVs), but check before next `/weekly` so it doesn't write a W24 file.
2026-06-07 — First v2 `/weekly` (W23). Published 2 SHORT zones (Primary $4367–$4390, Secondary
$4450–$4485, both 9.5/10), no counter. BEARISH MEDIUM-HIGH / conviction HIGH after NFP-shock −5.08%
week. Rewrote yield_environment (W23), updated _INDEX. CPI Wed 06-10 hard block flagged.
