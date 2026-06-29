---
description: Full weekly forecast → Trading Zones. One or all instruments.
argument-hint: [instrument]
model: claude-opus-4-8
---
Run the full weekly forecast → produce Trading Zones.

> **Model routing:** the ANALYSIS runs on Opus 4.8 (Step 2b judgment, Step 3 five-section, Step 4
> zone scoring + veto judgment, contradiction protocol — keep these here). The MECHANICAL legs —
> Step 0b DB guard, Step 1/1b/1c/1d pull + CB/econ/intervention gates, the Step 2b script runs
> (`zone_outcomes.py`, `check_econ_calendar.py --retro`), and the Post-Forecast script runs
> (`zone_ledger.py add`, `zone_outcomes.py`, `trade_outcome.py`, `calibration.py`) — should be
> delegated to the **`swing-fetch` subagent (Haiku)** to keep Opus tokens for the thinking. Spawn it
> with the instrument list + week/date, await its structured gate brief + file paths, then do the
> analysis here. For a single-instrument run the delegation is optional; for the all-11 default it
> saves the most. The subagent never analyses or scores — it runs scripts and reports.

Argument: `[instrument]` ∈ {xauusd, eurusd, gbpusd, eurgbp, audusd, nzdusd, usdcad, usdchf, usdjpy, eurjpy, gbpjpy}.
**Default (no arg) = ALL 11 instruments** — run the full procedure below once per instrument, in the order listed. Pass a single instrument to forecast just that one.
Batch run: do Step 0b (DB guard) ONCE up front; space the per-instrument `weekly_pull.py` calls ~8s apart (Twelve Data free tier = 8 req/min); run the Post-Forecast calibration refresh (`calibration.py`) ONCE at the end after every instrument, not per pair.
> Per-pair character / macro-direction / VIX-veto / re-forecast-series / confluence-philosophy are
> defined ONCE in `constitution.md` multi-instrument table + each pair's `confluence_criteria.md`.
> Step 0 table below + the §1 macro / Step-4 veto blocks carry only the command-specific deltas
> (operative gates + edge thresholds). Don't re-derive a pair's character here.

Goal: a weekly forecast that publishes up to **3 Trading Zones** (at most 1 counter-trend), each
scored by **Zone Confluence** (max 10, floor 5.0 — `wiki/system/{instrument}/confluence_criteria.md` R1).

## Step 0 — Instrument parametrization
| Param | xauusd | eurusd | gbpusd | eurgbp (cross) | audusd | nzdusd | usdcad (USD-base) | usdchf (USD-base) | usdjpy (USD-base, JPY) | eurjpy (cross, JPY) | gbpjpy (cross, JPY) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Character | momentum (pro-trend) | mean-reversion (fade) | mean-reversion (fade) | mean-reversion (fade), macro-light | mean-reversion (fade), H4-centric | mean-reversion (fade), macro-light/squeeze-led | mean-reversion (fade), USD-base | mean-reversion (fade), H1-centric, DXY proxy | **asymmetric carry-drift**: LONG drift-continuation / SHORT D1-H4-extreme fade | **symmetric mean-reversion + calm-drift** on long-drift floor; macro NONE | **extension-fade, SHORT-dominant**, strongest long-drift floor; NO calm row; macro NONE |
| Macro baseline field | `baseline_dfii10` | `baseline_dgs2` | `baseline_dgs2` | `baseline_rate_diff` (ECBDFR−SONIA, weak) | `baseline_dgs2` | `baseline_dgs2` (context only) | `baseline_dgs2` (FLIPPED polarity) | `baseline_dgs2` (FLIPPED, weak tilt) | `baseline_dgs2` (DEAD — drift in baseline) | `baseline_ecb_rate` (context only — macro dead) | `baseline_sonia_rate` (context only — macro dead) |
| Profile | xauusd_profile.md | eurusd_profile.md | gbpusd_profile.md | eurgbp_profile.md | audusd_profile.md | nzdusd_profile.md | usdcad_profile.md | usdchf_profile.md | usdjpy_profile.md | eurjpy_profile.md | gbpjpy_profile.md |
| Confluence R1 | xauusd | eurusd | gbpusd | eurgbp | audusd | nzdusd | usdcad | usdchf | usdjpy (direction-aware) | eurjpy | gbpjpy |

## Prerequisites — Read First
1. `wiki/system/core/macro/yield_environment.md` — prior macro baseline
2. `wiki/system/core/constitution.md` — risk rules, SL/TP/offset, zone rules, multi-instrument table
3. `wiki/system/{instrument}/confluence_criteria.md` — Zone Confluence (R1) signal set + weights
4. `wiki/system/{instrument}/{instrument}_profile.md` — drivers, sessions, ATR, events

## Step 0b — DB durability preflight (MANDATORY — never skip)
```bash
bash scripts/pyrun.sh scripts/db_guard.py all   # WAL checkpoint → integrity check → rotating backup
```
Non-zero exit = corrupt store. **STOP** and recover (`sqlite3 index.db .recover | sqlite3 fixed.db`)
before publishing zones — the DB is the source of truth.

## Step 1 — Fetch Data
```bash
bash scripts/pyrun.sh scripts/weekly_pull.py --instrument <INSTRUMENT>   # cache gate → fetch → compute
# granular: scripts/fetch.py (network only) | scripts/compute.py (indicators only, no net)
bash scripts/pyrun.sh scripts/weekly_pull.py --instrument <INSTRUMENT> --force   # full refetch
```
Keys from `.env`. 1 Twelve Data call (15M bars). Fail → stop. Cache: skip if snapshot <15min old OR
market closed (Fri 22:00 → Sun 22:00 UTC) AND file exists.

Pull file `data/weekly_pull/<INSTRUMENT>/weekly_pull_{YEAR}_W{WW}.txt` contains: H4/D1/W1 OHLC,
H4/D1 ATR14 + 20d median + compression, swing H/L, Fib, weekly pivots, Volume Profile, FRED macro
block (xauusd: DFII10/DGS10/T5YIE; FX: US2Y/DGS10/Fed-funds/foreign-policy + policy diff), DXY,
COT net + 1w chg, (xauusd only) GLD tonnes, weekend gap %, VIX, ADX(14) D1.

### Step 1b — Central-bank calendar (MANDATORY — mechanical, never skip)
```bash
bash scripts/pyrun.sh scripts/check_cb_calendar.py --days 10   # static calendar, all 8 banks
```
List in the forecast's no-trade calendar EVERY decision the checker reports for this instrument
(hard block or caution) inside the trade week + 2 days. The checker is authoritative for the 8
scheduled banks (FOMC/ECB/BoE/BoJ/SNB/RBA/RBNZ/BoC) — web search supplements, never replaces it
(W24 published EUR zones into an unflagged ECB day; this step is the fix). Exit 1 = calendar not
verified far enough — update `scripts/config/cb_calendar_{year}.json` before publishing zones.

### Step 1c — Economic data-release calendar (MANDATORY — #1/#2)
```bash
bash scripts/pyrun.sh scripts/check_econ_calendar.py --instrument <INSTRUMENT> --days 9
```
Lists HIGH-impact scheduled releases for the pair's currency legs in the trade week + 2d, with
no-trade windows (release ±30min) → feed into Section 2. Exit 1 = calendar CSV stale → it's
refetched by Step 1's `weekly_pull.py` (Forex Factory free JSON, no API key); if the feed is down, the
web search below is the fallback (never the sole source for CB *decisions* — those are Step 1b).

### Step 1d — JPY intervention watch (JPY pairs only, MANDATORY — #4)
```bash
bash scripts/pyrun.sh scripts/check_intervention_watch.py --instrument <usdjpy|eurjpy|gbpjpy> --spot <SPOT>
```
HARD_BLOCK longs in the MoF intervention zone / CAUTION in the band or on recent jawboning. Update
`scripts/config/intervention_watch.json` jawboning[] from the web search below + push
verified_through forward (same discipline as `cb_calendar`). Exit 1 = stale → refresh first.

### Web Search (supplementary)
- Central-bank speaker comments this week (Fed; + ECB for eurusd / BoE for gbpusd)
- Macro / geopolitical news affecting the instrument
- Scheduled high-impact DATA events next week (NFP/CPI/Retail/GDP; AU/NZ/CA/UK/EZ/JP tier-1) — UTC.
  Decision DATES come from Step 1b; search adds data releases + unscheduled risk.

## Step 2 — Read Data
Read the full `weekly_pull_{YEAR}_W{WW}.txt` before analysis.

## Step 2b — Prior-Week Retrospective (MANDATORY — feeds the new bias)
Before any new analysis, close the loop on the last forecast for THIS instrument. Without this the
forecast is blind to its own track record and can repeat a wrong thesis indefinitely.
1. Resolve last week's zones for this instrument and read the outcome:
   ```bash
   bash scripts/pyrun.sh scripts/zone_outcomes.py --week <prev YYYY-WNN> --instrument <INSTRUMENT>
   ```
   (`prev` = the ISO week immediately before the trade week being forecast.)
2. Read the prior forecast `forecasts/weekly/<INSTRUMENT>/<prev YYYY-WNN>.md` — its `macro_bias`,
   conviction, and each zone's thesis. Also glance at `wiki/system/core/calibration.md` for this
   instrument's standing edge verdict.
3. Judge, per zone and for the week's bias: **HELD / BROKE / UNTESTED** (no touch). For each, one
   line on WHY — was the macro read right, did structure invalidate, did an unscheduled event hit,
   was the zone simply never reached? Pull last week's data surprises (#2) to ground the "why":
   `bash scripts/pyrun.sh scripts/check_econ_calendar.py --retro <prev YYYY-WNN> --instrument <INSTRUMENT>`
   — a BEAT/MISS vs consensus often explains a bias that BROKE.
4. Carry it forward: if the same thesis is about to be re-issued, state explicitly why it is still
   valid given last week's result (or why the read changes). A bias that BROKE two weeks running on
   the same structural reason → cap conviction MEDIUM and flag it.
5. If the break exposes a **repeatable** lesson (not noise), add one line to
   `wiki/system/{instrument}/{instrument}_profile.md` (or `setup_library.md` for a cross-pair
   pattern) — this is how the profile learns. One-off / event-driven misses do NOT get recorded.
Write the result into Section 0 of the report (template). NO prior forecast (first week) → state
"first forecast — no retrospective" and skip.

## Step 3 — 5-Section Analysis

**1. Fundamental / Macro** — score the macro leg per pair; direction = what makes the PAIR bullish
(deadness/t-stat justification → constitution macro-direction row + `confluence_criteria.md`):

| Pair | Macro scoring leg (→ pair-bullish) | VIX | Regime note |
|---|---|---|---|
| xauusd | DFII10 level + 20d slope vs `baseline_dfii10`, falling real yield = bullish; + DXY, Fed posture | — | momentum |
| eurusd / gbpusd | US2Y(DGS2) 20d slope falling = bullish; **DXY 1d jump>0.5 = pair-bearish (strongest)**; policy-diff context only | spike → pair-bearish | — |
| eurgbp | macro thin/DEAD — price/structure only; EUR−GBP rate-diff (ECBDFR−SONIA) widening = weak bullish tilt | spike → EURGBP UP (inverted, weak tilt) | no USD leg |
| audusd | US2Y slope vs baseline + VIX LEVEL inverted (VIX>20→long / <15→short); DXY-jump DEAD | level scores (inverted) | no daily RBA |
| nzdusd | macro ~all DEAD; only weak inverted VIX-level tilt; bias = structure/squeeze | level tilt (weak) | no daily RBNZ |
| usdcad | US2Y slope FLIPPED (rising = bullish USDCAD); VIX>20→SHORT / <15→LONG bias; 🛢 WTI 5d>+5% → SHORT tilt; DXY-jump DEAD; COT 6C inverted | level scores (fade-USD) | USD-base |
| usdchf | **DXY 20d SLOPE = live macro** (rising = bullish); US2Y flipped weak; DXY 1d jump anti; COT 6S inverted | washout — no gate/score | SNB: shorts 0.78–0.80 fight SNB |
| usdjpy | **DXY 20d SLOPE = live macro**; US2Y DEAD (carry = D1 drift); DXY 1d jump anti; COT 6J inverted | washout — no gate/score | MoF: longs ≥158 fresh highs; BoJ days hard block |
| eurjpy | macro NONE (no USD leg; ECB leg anti = context); bias = structure/calm | dead — no gate/score | MoF/BoJ shared; 185+ record |
| gbpjpy | macro NONE (SONIA leg dead = context); bias = structure/session | dead — no gate/score | MoF/BoJ shared (largest slams); 214+ record |

Intermarket (#3, D025): pull carries copper + iron ore (AUD) / dairy (NZD) — rising = risk-on bid =
pair-BULLISH **context only, NOT scored**; tie-breaker in §1/§4, never a Z-row.
Bias: BULLISH/BEARISH/NEUTRAL + confidence. Flag regime shift vs baseline.

**2. News Analysis** — scheduled high-impact calendar next week (UTC, mark hard blocks),
central-bank commentary, geopolitical drivers. No-trade windows. Read the pull's **NEWS FEED
block** + `bash scripts/pyrun.sh scripts/check_news.py --instrument <INST> --days 7` (free RSS
feeds, D025) for recent pair-relevant headlines; web search supplements, never sole-source.

**3. Technical Analysis** — key S/R zones as boxes (swing points + Volume Profile / time-at-price
for USD-base), EMA 20/50/200, RSI state, D1 ATR regime, weekly pivots, ADX regime.
- **OSCILLATORS block (D025): Stoch / Williams %R / CCI / Keltner / Donchian / TTM-squeeze / PSAR /
  Supertrend are now COMPUTED on D1+H4 in the pull (read the EXTREMES line) — no longer eyeball
  them. These ARE the Z2-engine inputs the `confluence_criteria` reference; cite the printed value.**
- **MARKET STRUCTURE block (D025): BOS/CHoCH labeled per D1+H4 (fractal N=2). CHoCH against the
  prevailing state = the reversal tell the FX fade wants; BOS = continuation.**
- USD-base pairs (usdcad/usdchf/usdjpy): VP is disabled → use the **TIME-AT-PRICE** block (H1
  acceptance HTN/value-area) as the POC/VA substitute. It is acceptance, NOT traded volume.
- xauusd: gold is momentum — RSI>70 is NOT a short signal; structure = breakout locator.
- FX: **mean-reversion — RSI>65/70 IS a short signal, RSI<35 a long; structure = FADE point.**
  Trend-following (EMA regime/ADX-trend/Supertrend) is anti-edge — do NOT use as pro-trend confluence.

**4. Positioning & Flows** — COT net + 1w change (xauusd: crowded long NOT a contrarian short;
FX: positioning context only), (xauusd) GLD tonnes, weekend gap %. Flag contradictions vs bias.

**5. Top-Down (D→H4→1H)** — structure on Daily→H4→H1, alignment per candidate direction.
`mtf_alignment`: ALIGNED / MIXED / OPPOSING. (Note: for FX this informs the FADE, not a trend follow.)
Ground it in the pull's **MARKET STRUCTURE block** (computed BOS/CHoCH + state per TF), not eyeball.

## Step 4 — Build Trading Zones (Zone Confluence, R1)
Score each candidate zone per the instrument's `confluence_criteria.md` R1 — **the Z1–Z7 table
differs by instrument**:
- **xauusd:** Z1 Structural 2.0 (MAND) | Z2 DFII10 slope 2.5 | Z3 DXY slope 1.5 | Z4 MTF 2.0 | Z5 EMA regime 1.0 | Z6 ATR compression 0.5 | Z7 VP node 0.5.
- **eurusd:** Z1 Structural 2.0 (MAND) | Z2 H4 oscillator extreme 2.0 | Z3 band over-extension 1.5 | Z4 big-figure 1.0 | Z5 macro/intermarket (DXY-jump/US2Y-slope/VIX-spike) 1.5 | Z6 non-trend ADX<25 1.0 | Z7 compression 1.0.
- **gbpusd:** Z1 Structural D1-extreme 2.5 (MAND) | Z2 D1 oscillator extreme 2.0 | Z3 H1 oscillator 1.5 | Z4 macro/intermarket 1.5 | Z5 non-trend ADX<25 1.0 | Z6 band/compression 0.5 | Z7 seasonal/Williams 1.0.
- **eurgbp (cross):** Z1 Structural D1-extreme 3.0 (MAND) | Z2 D1 oscillator extreme 2.5 | Z3 H1 oscillator 1.5 (validated) | Z4 macro/sentiment TILT 0.5 | Z5 non-trend ADX<25 1.0 | Z6 band/compression 0.5 | Z7 Williams/Stoch 1.0. (Macro NOT a gate — EG2 dead.)
- **audusd:** Z1 Structural 2.0 (MAND) | Z2 H4 oscillator extreme 2.0 | Z3 H4 band over-extension 1.5 | Z4 big-figure LONG 0.5 | Z5 macro regime tilt (VIX level INVERTED + US2Y slope) 1.5 | Z6 non-trend ADX<25 1.5 | Z7 compression/squeeze 1.0. (NO DXY row — dead for AUD.)
- **nzdusd:** Z1 Structural 2.0 (MAND) | Z2 H4 oscillator extreme 2.0 | Z3 compression/squeeze 2.0 (strongest NZD signal) | Z4 H4 band over-extension 1.5 | Z5 big-figure LONG 1.0 | Z6 non-trend ADX<25 1.0 | Z7 VIX regime tilt (weak, inverted) 0.5. (NO US2Y/DXY rows — dead for NZD.)
- **usdcad (USD-base):** Z1 Structural 2.0 (MAND) | Z2 H4 oscillator extreme 2.0 | Z3 H4 band over-extension 2.0 (BB-upper short t=3.19) | Z4 compression/squeeze 1.5 | Z5 VIX regime fade-USD 1.0 | Z6 US2Y-flipped + oil tilt 1.0 | Z7 non-trend ADX<25 0.5. (NO DXY row; COT inverted = context.)
- **usdchf (USD-base):** Z1 Structural 2.0 (MAND) | Z2 H1 oscillator extreme cluster 2.0 (short t 4.0–5.5) | Z3 DXY 20d slope aligned 2.0 | Z4 compression/squeeze (H1 TTM/calm) 1.5 | Z5 D1 pattern/extreme 1.0 | Z6 H4 band/big-figure 1.0 | Z7 non-trend ADX<25 0.5. (NO VIX row — washout; H4 thin, H1-centric.)
- **usdjpy (USD-base, DIRECTION-AWARE):** Z1 Structural 2.0 (MAND) | Z2 side engine 2.5 — LONG: D1 TTM squeeze/calm ATR (t 3.3–4.5) · SHORT: ≥2 of D1 RSI>65 / H4 CCI>+100 / H4 Keltner-high (t 2.1–3.1) | Z3 DXY 20d slope aligned 2.0 | Z4 LONG dip at 20d low 1.0 | Z5 D1 pattern (PSAR/engulf) 1.0 | Z6 LONG big-figure 1.0 | Z7 not-extended ADX<25 0.5. (NO VIX row; counter = SHORT.)
- **eurjpy (cross-JPY, NO macro):** Z1 Structural 2.0 (MAND) | Z2 extreme engine 2.5 — LONG: washout (D1 Stoch<20 / H1 Keltner-low / 20d low, t 2.6–3.1) · SHORT: extension (D1/H4 Keltner-high / RSI>65–70, t 2.8–3.5) | Z3 calm/squeeze regime 1.5 (LONG full, SHORT half) | Z4 H4 oscillator stack 1.5 | Z5 D1 trigger (inside-bar/compression) 1.0 | Z6 big-figure 1.0 | Z7 not-extended ADX<25 0.5. (NO macro row at all; counter = SHORT.)
- **gbpjpy (cross-JPY, NO macro, NO calm row):** Z1 Structural 2.0 (MAND) | Z2 extreme engine 2.5 — SHORT: extension (D1/H4 Keltner-high / BB-upper / RSI>65 / CCI>+100, t 3.0–4.6) · LONG: washout (D1/H4 Keltner-low / RSI<35 / CCI<−100 / 20d low, t 2.2–2.6) | Z3 multi-TF extreme alignment ≥2 TFs 1.5 | Z4 H4 oscillator stack 1.5 | Z5 H4 reversal trigger (MACD-down/pin) 1.0 | Z6 big-figure 1.0 | Z7 not-extended ADX<25 0.5. (NO macro, NO calm/squeeze; counter = SHORT.)

Rules: publish if score ≥ 5.0 (Z1 mandatory). Max 3 zones, ≤1 counter.
- Counter zone (xauusd): macro Z2+Z3 score 0; RSI divergence MANDATORY; macro conf LOW/MEDIUM.
- Vetoes (publish gate) — t-stat justification → constitution macro-direction/VIX rows. "Never score
  trend-follow" is universal for every FX fade pair.

  | Pair | VIX veto | DXY block | Other vetoes / never-score |
  |---|---|---|---|
  | xauusd | VIX>35 blocks SHORTs | — | never score RSI>70 or COT>200k as a short |
  | eurusd / gbpusd | VIX>35 or spike>3 blocks LONGs | DXY 1d jump against a zone blocks it | never trend-follow |
  | eurgbp | NONE | NONE | D1 ADX>30 vs the fade |
  | audusd | NONE (level scores Z5) | NONE | D1 ADX>30 vs the fade |
  | nzdusd | NONE | NONE (+ NO US2Y gate) | D1 ADX>30 vs the fade; never score big-figure as a SHORT |
  | usdcad | NONE (level scores Z5) | NONE | D1 ADX>30 vs the fade; never score bearish-engulf / Donchian-breakdown continuation |
  | usdchf | NONE (washout) | NONE (DXY scores via 20d SLOPE Z3) | D1 ADX>30 vs the fade; SNB decision/communication day (quarterly Mar/Jun/Sep/Dec Thu 08:30 UTC); SHORT zone inside 0.78–0.80 band → cap MEDIUM |
  | usdjpy | NONE (washout) | NONE (DXY via 20d slope Z3) | BoJ day / active MoF jawboning = HARD BLOCK; LONG ≥158 fresh highs → cap MEDIUM; **NO H1-only SHORT zones**; no chasing extension (ADX>25 continuation long); turn-of-month LONG −0.5 |
  | eurjpy | NONE | NONE | BoJ / MoF jawboning / ECB = HARD BLOCK; record-high LONG in intervention watch → cap MEDIUM; REVERSION only (never breakout/continuation); turn-of-month LONG −0.5 |
  | gbpjpy | NONE | NONE | BoJ / MoF jawboning / BoE = HARD BLOCK; record-high LONG in intervention watch → cap MEDIUM; REVERSION only; turn-of-month LONG −0.5; January LONG caution; **NO calm/squeeze scoring** |
- Write IF/THEN in one sentence + name zone (Primary/Secondary/Counter), direction, box, score, signals.
- SL/offset/TP computed at `/validate`, not here — but name the TP structural anchor + indicative R.

## Step 5 — Write the Forecast Report
Template `wiki/system/templates/weekly_forecast.md`. Frontmatter (instrument-aware baseline):
```yaml
type: weekly_forecast
instrument: xauusd | eurusd | gbpusd | eurgbp | audusd | nzdusd | usdcad | usdchf | usdjpy | eurjpy | gbpjpy
week: YYYY-WNN
generated: YYYY-MM-DD
macro_bias: BULLISH | BEARISH | NEUTRAL
macro_confidence: HIGH | MEDIUM-HIGH | MEDIUM | MEDIUM-LOW | LOW
mtf_alignment: ALIGNED | MIXED | OPPOSING
best_zone: PRIMARY | SECONDARY | NONE
conviction: HIGH | MEDIUM-HIGH | MEDIUM | MEDIUM-LOW | LOW
baseline_dfii10: x.xx        # xauusd only
baseline_dgs2: x.xx          # FX majors only
baseline_policy_diff: x.xx   # FX majors context only
baseline_rate_diff: x.xx     # eurgbp only (ECBDFR−SONIA; weak/context)
baseline_ecb_rate: x.xx      # eurjpy only (ECBDFR level; context — macro dead)
baseline_sonia_rate: x.xx    # gbpjpy only (IUDSOIA level; context — macro dead)
baseline_dxy: xxx.xxx
weekend_gap_pct: x.xxx
cot_net: ±xxxxx
cot_net_chg: ±xxxxx
etf_gld_tonnes: xxxx.xx      # xauusd only
adx_val: xx.x
```
Body: 5 sections, then each Trading Zone with box + Zone Confluence + signals + IF/THEN + TP anchor
+ indicative R. Bias statement (≤3 lines). No-trade calendar. `> [!warning]` contradiction callout if
macro/technical/positioning conflict (lower conviction to MEDIUM per Contradiction Protocol).

Save to `forecasts/weekly/<INSTRUMENT>/YYYY-WNN.md` (Claude writes markdown directly).

> **WNN = TARGET trade week the forecast governs — NOT the run-date week.**
> Weekend run (Fri 22:00 → Sun) forecasts the **upcoming** week → use next ISO week (the Monday it opens).
> Mid-week refresh forecasts the **current** week → use the current ISO week.
> `week:` frontmatter + title + filename must all match the trade week. Compute from the Monday the
> zones go live: `WNN = isocalendar(next_monday).week`. (E.g. run Sun 06-07 → trades Mon 06-08 → W24.)

## Post-Forecast Updates
1. **Register every published zone in the shadow ledger** (one `add` per zone — feeds outcome
   tracking / confluence calibration; `zone_outcomes.py` replays OHLC against it later):
   ```
   bash scripts/pyrun.sh scripts/zone_ledger.py add \
       --instrument <inst> --week YYYY-WNN --label PRIMARY|SECONDARY|COUNTER \
       --direction LONG|SHORT --zone-bottom X --zone-top Y --score N.N \
       --conviction <conviction> [--invalidation-level Z] [--tp-anchor T]
   ```
   `--invalidation-level` = D1-close kill level if the zone states one (else resolver defaults to
   the zone's far edge). NO ZONES published → nothing to register. (Last week's zones for this
   instrument were already resolved in Step 2b; if running a full portfolio, resolve any remaining
   instruments now: `bash scripts/pyrun.sh scripts/zone_outcomes.py --week <prev YYYY-WNN>`.)
   Then replay the entry mechanics for SYSTEM P&L + gate accuracy (R2):
   `bash scripts/pyrun.sh scripts/trade_outcome.py --week <prev YYYY-WNN>` (→ `trade_outcome` table).
   Then refresh the calibration report (reads zone_outcome R1 + trade_outcome R2/gate-accuracy):
   `bash scripts/pyrun.sh scripts/calibration.py` → rewrites `wiki/system/core/calibration.md`.
   Scan it: any instrument×direction or R1 bucket flipped to **DEAD** (n≥min-n) → flag in `_HOT.md`
   Pending Actions for a confluence-criteria review before publishing more of that edge.
2. Rewrite `wiki/system/core/macro/yield_environment.md` with this week's macro snapshot (note which instrument).
3. Update `_HOT.md`: Active Forecast link + bias; new zones PENDING (box + direction) tagged by instrument;
   week number; reset risk used + `weekly_reforecast_count` to 0 if new week; refresh Pending Actions.
4. Update `_INDEX.md`: add the new forecast file under Forecasts.
5. No DB import step — `data/database/index.db` is written live during the pull
   (`weekly_pull.py` syncs ohlc/macro/market/news/econ/gld; `db.py` writes trade/zone tables).
