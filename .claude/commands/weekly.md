Run the full weekly forecast → produce Trading Zones.

Argument: `[instrument]` ∈ {xauusd, eurusd, gbpusd, eurgbp, audusd} (default xauusd). One instrument per invocation.
(eurgbp = CROSS: macro-light mean-reversion, no VIX-veto, European event blocks. audusd: no VIX-veto +
no DXY block — VIX level INVERTED tilt, DXY-jump dead; RBA/AU-CPI/China events.)

Goal: a weekly forecast that publishes up to **3 Trading Zones** (at most 1 counter-trend), each
scored by **Zone Confluence** (max 10, floor 5.0 — `wiki/system/{instrument}/confluence_criteria.md` R1).

## Step 0 — Instrument parametrization
| Param | xauusd | eurusd | gbpusd | eurgbp (cross) | audusd |
|---|---|---|---|---|---|
| Character | momentum (pro-trend) | mean-reversion (fade) | mean-reversion (fade) | mean-reversion (fade), macro-light | mean-reversion (fade), H4-centric |
| Macro baseline field | `baseline_dfii10` | `baseline_dgs2` | `baseline_dgs2` | `baseline_rate_diff` (ECBDFR−SONIA, weak) | `baseline_dgs2` |
| Profile | xauusd_profile.md | eurusd_profile.md | gbpusd_profile.md | eurgbp_profile.md | audusd_profile.md |
| Confluence R1 | xauusd | eurusd | gbpusd | eurgbp | audusd |

## Prerequisites — Read First
1. `wiki/system/core/macro/yield_environment.md` — prior macro baseline
2. `wiki/system/core/constitution.md` — risk rules, SL/TP/offset, zone rules, multi-instrument table
3. `wiki/system/{instrument}/confluence_criteria.md` — Zone Confluence (R1) signal set + weights
4. `wiki/system/{instrument}/{instrument}_profile.md` — drivers, sessions, ATR, events

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

### Web Search (supplementary)
- Central-bank speaker comments this week (Fed; + ECB for eurusd / BoE for gbpusd)
- Macro / geopolitical news affecting the instrument
- Scheduled high-impact events next week (FOMC/NFP/CPI/Retail; + ECB/BoE decisions for FX) — UTC

## Step 2 — Read Data
Read the full `weekly_pull_{YEAR}_W{WW}.txt` before analysis.

## Step 3 — 5-Section Analysis

**1. Fundamental / Macro** —
- xauusd: DFII10 (level + 20d slope vs `baseline_dfii10`), DXY, Fed posture. Falling real yield = bullish.
- FX majors (eurusd/gbpusd): US2Y (DGS2) 20d slope vs `baseline_dgs2`, DXY 1d jumps, VIX, policy-diff CONTEXT (not scored).
  Falling US2Y = pair-bullish. **DXY 1d jump>0.5 → pair-bearish (strongest signal). VIX spike → pair-bearish.**
- eurgbp (CROSS — no USD leg): macro is **thin/DEAD (EG2)** → price/structure only. No DXY, no US rates.
  Direction tilt (low weight): EUR−GBP rate diff (ECBDFR−SONIA) widening → bullish; **VIX spike → EURGBP UP** (risk-off
  favors EUR over GBP — INVERTED vs majors). Bias is set by structure/oscillator extremes, not macro.
- audusd: US2Y (DGS2) slope vs `baseline_dgs2` + **VIX LEVEL regime (INVERTED: VIX>20 → long tilt
  t=6.14, VIX<15 → short tilt t=5.29)**. **DXY-jump DEAD for AUD (t=−0.85) — context only, never score
  or block.** No daily RBA series (carry leg off). China/commodity beta = narrative context.
Bias: BULLISH/BEARISH/NEUTRAL + confidence. Flag regime shift vs baseline.

**2. News Analysis** — scheduled high-impact calendar next week (UTC, mark hard blocks),
central-bank commentary, geopolitical drivers. No-trade windows.

**3. Technical Analysis** — key S/R zones as boxes (swing points + Volume Profile), EMA 20/50/200,
RSI state, D1 ATR regime, weekly pivots, ADX regime.
- xauusd: gold is momentum — RSI>70 is NOT a short signal; structure = breakout locator.
- FX: **mean-reversion — RSI>65/70 IS a short signal, RSI<35 a long; structure = FADE point.**
  Trend-following (EMA regime/ADX-trend/Supertrend) is anti-edge — do NOT use as pro-trend confluence.

**4. Positioning & Flows** — COT net + 1w change (xauusd: crowded long NOT a contrarian short;
FX: positioning context only), (xauusd) GLD tonnes, weekend gap %. Flag contradictions vs bias.

**5. Top-Down (D→H4→1H)** — structure on Daily→H4→H1, alignment per candidate direction.
`mtf_alignment`: ALIGNED / MIXED / OPPOSING. (Note: for FX this informs the FADE, not a trend follow.)

## Step 4 — Build Trading Zones (Zone Confluence, R1)
Score each candidate zone per the instrument's `confluence_criteria.md` R1 — **the Z1–Z7 table
differs by instrument**:
- **xauusd:** Z1 Structural 2.0 (MAND) | Z2 DFII10 slope 2.5 | Z3 DXY slope 1.5 | Z4 MTF 2.0 | Z5 EMA regime 1.0 | Z6 ATR compression 0.5 | Z7 VP node 0.5.
- **eurusd:** Z1 Structural 2.0 (MAND) | Z2 H4 oscillator extreme 2.0 | Z3 band over-extension 1.5 | Z4 big-figure 1.0 | Z5 macro/intermarket (DXY-jump/US2Y-slope/VIX-spike) 1.5 | Z6 non-trend ADX<25 1.0 | Z7 compression 1.0.
- **gbpusd:** Z1 Structural D1-extreme 2.5 (MAND) | Z2 D1 oscillator extreme 2.0 | Z3 H1 oscillator 1.5 | Z4 macro/intermarket 1.5 | Z5 non-trend ADX<25 1.0 | Z6 band/compression 0.5 | Z7 seasonal/Williams 1.0.
- **eurgbp (cross):** Z1 Structural D1-extreme 3.0 (MAND) | Z2 D1 oscillator extreme 2.5 | Z3 H1 oscillator 1.5 (validated) | Z4 macro/sentiment TILT 0.5 | Z5 non-trend ADX<25 1.0 | Z6 band/compression 0.5 | Z7 Williams/Stoch 1.0. (Macro NOT a gate — EG2 dead.)
- **audusd:** Z1 Structural 2.0 (MAND) | Z2 H4 oscillator extreme 2.0 | Z3 H4 band over-extension 1.5 | Z4 big-figure LONG 0.5 | Z5 macro regime tilt (VIX level INVERTED + US2Y slope) 1.5 | Z6 non-trend ADX<25 1.5 | Z7 compression/squeeze 1.0. (NO DXY row — dead for AUD.)

Rules: publish if score ≥ 5.0 (Z1 mandatory). Max 3 zones, ≤1 counter.
- Counter zone (xauusd): macro Z2+Z3 score 0; RSI divergence MANDATORY; macro conf LOW/MEDIUM.
- Vetoes: xauusd VIX>35 blocks shorts + never score RSI>70/COT>200k short. **FX majors: VIX>35 or VIX
  spike>3 blocks LONGs; DXY 1d jump against a zone blocks it; never score trend-follow.**
  **eurgbp (cross): NO VIX veto, NO DXY block** (risk-off → EURGBP up, inverted; DXY irrelevant). Only
  veto = D1 ADX>30 trending against the fade. Never score trend-follow.
  **audusd: NO VIX veto, NO DXY block** (VIX level scores inverted in Z5; DXY-jump dead). Only veto =
  D1 ADX>30 trending against the fade. Never score trend-follow.
- Write IF/THEN in one sentence + name zone (Primary/Secondary/Counter), direction, box, score, signals.
- SL/offset/TP computed at `/validate`, not here — but name the TP structural anchor + indicative R.

## Step 5 — Write the Forecast Report
Template `wiki/system/templates/weekly_forecast.md`. Frontmatter (instrument-aware baseline):
```yaml
type: weekly_forecast
instrument: xauusd | eurusd | gbpusd | eurgbp | audusd
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
1. Rewrite `wiki/system/core/macro/yield_environment.md` with this week's macro snapshot (note which instrument).
2. Update `_HOT.md`: Active Forecast link + bias; new zones PENDING (box + direction) tagged by instrument;
   week number; reset risk used + `weekly_reforecast_count` to 0 if new week; refresh Pending Actions.
3. Update `_INDEX.md`: add the new forecast file under Forecasts.
