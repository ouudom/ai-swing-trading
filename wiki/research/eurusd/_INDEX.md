---
type: research
updated: 2026-05-28
tags: [index, eurusd]
---

# EURUSD Research Index

Edge-first build. NO live rules until a signal is measured to have edge here (not assumed
from XAUUSD). Thresholds in **pips**, not dollars. See [[constitution]] for universal rules.

## Macro Driver Decision (2026-05-28)

Anchor = **US–EU short-rate differential: DGS2 − ESTR** (daily, independent of EUR price).
- German Bund is monthly-only on FRED → no daily 10y/2y differential feasible free.
- DXY rejected as primary: ~−0.95 corr with EURUSD → price-derived, not independent macro.
- DGS2 carries daily movement (US rate expectations = dominant EURUSD driver); ESTR
  (`ECBESTRVOLWGTTRMDMNRT`, daily) supplies the EU side.
- **Must be confirmed in Phase 2** (differential-slope vs forward EUR return) before weight is locked.
- Sign convention (to verify): rising differential → USD strength → EUR bearish. EUR long wants
  slope < 0; EUR short wants slope > 0 (mirrors XAUUSD G3).

## Planned Concepts (Phase 2 — fill with measured results)

| File | Hypothesis to test |
|---|---|
| `concepts/mtf-market-structure.md` | Does fractal HH/HL gate (scripts/structure.py) predict EUR direction? Win-rate vs random. |
| `concepts/macro-rate-differential.md` | DGS2−ESTR slope vs forward EUR return. Confirm/reject as G3-equivalent. Compare vs DXY slope + US-side-only (DFII10/DGS2). |
| `concepts/atr-compression.md` | EUR ATR compression → expansion probability. Pip thresholds. |
| `concepts/session-timing.md` | London/NY-overlap effect on EUR (NOT Asia — gold's G6 won't transfer). |
| `concepts/stop-loss.md` | Structural vs ATR stop on EUR; pip-scaled stop formula. |
| `concepts/dxy-correlation.md` | EUR–DXY rolling corr (feeds correlation guard USD_BETA_SIGN=-1). |

## Data Sources

| Source | TF | Notes |
|---|---|---|
| Twelve Data EUR/USD (UTC) | M15 | `data/twelvedata/eurusd/15min.csv` (backfill 2020→now) |
| → resampled | H1/H4/D1 | via `scripts/resample_twelvedata.py --symbol EUR/USD` |
| FRED DGS2 | daily | US 2y |
| FRED ECBESTRVOLWGTTRMDMNRT | daily | ESTR euro short-term rate |
| FRED DFII10, DGS10 | daily | US real/nominal 10y (context) |
| FRED DFF, VIXCLS | daily | policy + risk regime |

## Research Standards (inherit from xauusd)

- Report: N, win%, edge in pp, EV in R, trades/yr. Test long AND short.
- Thresholds in pips. EUR random-baseline TBD (compute; gold's 54% does not transfer).
- One TD call/pull (15M resampled locally).

## Phase 2 Findings (2026-05-28) — `scripts/research_eurusd.py`

**Macro driver FAILS.** No stable directional edge from any rate/positioning signal:
- DGS2−ESTR slope (3yr): −5.7pp edge (anti-predictive). Level: corr +0.26 at 20d BUT...
- **22yr test (yfinance EUR 2004→now):** slope edge ~0 (±1pp); level corr ~0.02–0.05.
- **Regime-unstable:** diff_sl FWD5 edge = +3.1 (2010-15), +4.0 (2020-23), **−3.2 (2023-26)**.
  The recent inverted signal is a regime artifact, OPPOSITE the textbook 2010-23 behavior.
- DXY slope ~0; DFII10 slope ~0 (full history).
- **COT EUR positioning** (2019-26, 385wk): corr(net_pct, fwd5)=+0.011, no edge. Net-short
  extreme 58% up (weak, N=67). Contract `EURO FX - CHICAGO MERCANTILE EXCHANGE` verified.
- EU CPI/PMI *surprise*: needs consensus-calendar data, not available free in this stack.

**Other signals:**
- MTF structure (fractal HH/HL): both-up 55.8% up (+6.9pp long), but **short side inverted**
  (both-down → 54.2% UP). Weak, asymmetric.
- ATR compression: NO edge (compressed 89% vs normal 87% expand).
- Session: ROBUST. EUR active **12–15 UTC** (NY/London overlap, 21-23 pips), London open 07-08
  (17 pips), **Asia dead (8-9 pips)**. Gold's G6 (Asia compression) does NOT transfer.
- Directional baseline: 48.9% up (neutral, no drift — unlike gold's 54%).

**Conclusion:** the fundamental-gate that gold relies on (DFII10 slope, weight 3.0) has NO
transferable equivalent for EUR. Only session timing is a clean, robust feature.

Data added: `data/yahoo/EURUSD_d.csv` (22yr daily), `data/yahoo/DXY_long.csv`,
`data/cftc/eur_cot_net.csv`, ECBDFR/DGS2/ESTR backfilled.

## Phase 2b Findings — session strategies (2026-05-28) `scripts/research_eurusd_session.py`

Pivoted to session edge after macro failed. Tested on 3yr intraday. **Also no robust edge:**
- London-open breakout (Asia range, 07→16): −0.28p avg, breakeven/neg.
- Overlap continuation (12→16): **−2.02p** (momentum fails after costs).
- Overlap fade (12→16): +0.42p (right sign, mean-reverting, but tiny).
- Fade by 12:00 move size: ONLY 10-20p bucket pays (+1.74p, N=185 ≈60/yr); ≥20p moves TREND
  (fade loses −2.6p); Asia-range breakout-fade loses −3.38p (breakouts continue).
- Net: session TIMING is real (when EUR moves) but no robust directional STRATEGY survives costs.

**Overall EUR conclusion:** with free data (3yr intraday / 22yr daily) + tested methods, NO
robust tradeable edge found — macro (dead), structure (weak/asymmetric), ATR (none), COT (none),
session strategies (breakeven/negative). Recommend shelve EUR or pursue better data
(paid pre-2023 intraday, tick data, economic-calendar surprise) before building.

## Phase 2c — exotic battery (2026-05-28) — also NULL

22yr daily + 3yr intraday: day-of-week (all |t|<1), turn-of-month (t=−0.04), overnight-gap
reversal (neg/insignificant; yfinance FX gaps are bar artifacts anyway). No edge.

**FINAL (3yr):** every avenue null on 3yr. BUT see update below — better data changed this.

## Phase 2d — HistData extends sample to 6.4yr (2026-05-28)

User supplied HistData.com M1 2020-2023 → merged with TD via `scripts/ingest_histdata_eur.py`
to `data/research/eurusd/{tf}.csv` (2020→now). **Timezone gotcha (user-flagged, confirmed):**
HistData "EST" actually tracks US Eastern WITH DST → convert via `America/New_York`, not fixed
offset. Validated 0.40 pip median vs TD overlap (fixed +5h was 1h off in summer).

**Re-ran session edges on 6.4yr — the 3yr fade result was NOISE and INVERTED:**
- 3yr said fade 10-20p moves (+1.74p). On 6.4yr that bucket = −0.14p (gone).
- 6.4yr: fade LARGE overlap moves pays — fade(≥20p 12:00 move, exit 16:00): 20-30p +3.0p (53% win,
  N=128), 30p+ +4.8p (54% win, N=96), monotonic. ~35 trades/yr. Per-trade sharpe ~0.1 (modest).
- Continuation still loses (−1.95p); London breakout breakeven (+0.41p).
- LESSON: 3yr was too small; candidate edge = NY-overlap large-move mean-reversion. Needs Phase-3
  backtest with stop/target/costs to confirm tradeable expectancy (sharpe is thin).

## Phase 3 — VALIDATED EDGE (2026-05-28) `scripts/backtest_eur_session.py`

**EUR NY-overlap large-move mean-reversion. Rule:** at 12:00 UTC, if the H1 bar moved
>= 20 pips, FADE it — enter opposite at 13:00 open, stop 20p, target 40p (1:2 R), time-exit
16:00 close. ~35 trades/yr, win ~46% (sub-50% by design; 1:2 R carries it).

**Out-of-sample STABLE** (the decisive test, given 3yr noise earlier):
- 2020-23 (HistData feed): PF 1.26, +2.74p/trade
- 2023-26 (TD feed):       PF 1.21, +2.09p/trade
- Both halves + two independent feeds positive → robust, not whole-sample overfit.
- (Symmetric-stop variant thr25/stop40/tgt40 REJECTED: 1st half PF1.53 but 2nd half 0.93.)

**Cost sensitivity (full 6.4yr):** 0.8p→PF1.24, 1.5p→PF1.16 (+1.71p), 2.0p→PF1.11, 2.5p→PF1.06.
Edge is REAL but THIN — needs a tight-spread broker (<1.5p) + limit execution. Per-trade
sharpe ~0.1 → high variance, expect drawdowns; size small.

→ Proceed to Phase 4 codify as a SEPARATE daily intraday-session system (NOT /weekly swing).

## Phase 2e — confluence indicators for the SWING system (2026-05-28) `scripts/research_eurusd_indicators.py`

User keeps the weekly-forecast/daily-validation/offset architecture; EUR gets its OWN signals.
Scanned candidate indicators, forward-5d edge vs 48.9% baseline (6.4yr daily):

**EUR is MEAN-REVERTING (opposite of trend/macro gold):**
- RSI>70 → short: **+6.6pp** (55.5%, N=200). RSI<30 → long: **+4.4pp** (53.3%, N=195). ← strongest
- close<BB_lower → long: +1.6pp. 20d-low → long: +2.3pp. 20d-high → short: +1.3pp (structural).
- Donchian-20 breakout: NEGATIVE (−4.4 up / −3.1 dn) → EUR breakouts FAIL, fade them.
- EMA-trend continuation: weak (~+1pp). Pullback-in-trend: negative.

→ EUR confluence = counter-trend mean-reversion at structural extremes + RSI extreme/divergence
+ Bollinger; NO breakout/trend-continuation signal. Fundamental kept as lower-weight context
(macro null as standalone). Codified in `wiki/instruments/eurusd/confluence_criteria.md`.

## Phase 5 — threshold calibration (2026-05-28) `scripts/calibrate_eurusd.py`

Replaced provisional placeholders with values derived from the 6.4yr distribution:
- G6 compressed cutoff = **35 pips** (07–13 UTC window range; p33, median 41p).
- T3 counter-move = **1.0%** (p97 of D1 |%move|; ≈1.7× the 0.6% D1-ATR%).
- Weekend-gap tiers EUR-scaled: NOTE 0.05% / WARN 0.20% / REFORECAST 0.50% (gold's were ~10× bigger).
- V1b buffer = **7 pips** (0.3× median H4 range 23.5p).
- VP/pivot proximity = **~10 pips** (½× median H4 ATR 27p).
- Reference ATRs: D1 ≈ 69 pips, H4 ≈ 27 pips (profile.md corrected from stale 49/18).
- H4 5-pip flatline filter confirmed (drops only 0.5% of bars).

Codified in confluence_criteria.md + constitution_addendum.md + profile.md.

## Pending Research (resume conditions)

- [ ] EU CPI/PMI surprise (blocked: needs consensus-calendar source)
- [ ] Better intraday history (paid TD tier pre-2023) to widen sample beyond rangey 2023-26
- [ ] A specific, theory-grounded hypothesis (not blind pattern search)
