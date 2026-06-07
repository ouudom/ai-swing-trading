Run the full weekly forecast (XAUUSD) → produce Trading Zones.

Goal: a weekly forecast report that publishes up to **3 Trading Zones** (at most 1 counter-trend),
each scored by **Zone Confluence** (max 10, floor 5.0 — see `wiki/system/xauusd/confluence_criteria.md` R1).

## Prerequisites — Read First
1. `wiki/system/core/macro/yield_environment.md` — prior macro baseline (DFII10, DXY, bias, posture)
2. `wiki/system/core/constitution.md` — risk rules, SL/TP/offset, zone rules
3. `wiki/system/xauusd/confluence_criteria.md` — Zone Confluence (R1) signal set + weights

## Step 1 — Fetch Data
```bash
.venv/bin/python scripts/weekly_pull.py --instrument xauusd   # orchestrator: cache gate → fetch → compute
# granular: scripts/fetch.py (network only) | scripts/compute.py (indicators only, no TD/FRED net)
.venv/bin/python scripts/weekly_pull.py --instrument xauusd --force   # force full refetch
```
Reads keys from `.env` (`TWELVE_DATA_KEY`, `FRED_KEY`). 1 Twelve Data call (15M bars). Fail → stop.
Cache: skips refetch if snapshot <15min old OR market closed (Fri 22:00 → Sun 22:00 UTC) AND file exists.

Pull file: `data/weekly_pull/xauusd/weekly_pull_{YEAR}_W{WW}.txt` — contains:
H4/D1/W1 OHLC (30 bars), H4/D1 ATR14 + D1 20d median + compression flag, swing H/L (5 each H4/D1),
Fib levels, weekly pivots, Volume Profile (CME GC VAH/POC/VAL), FRED (DFII10, DGS10, T5YIE, FEDFUNDS,
DXY proxy), DFII10 20d slope + drift, COT MM net + 1w chg, GLD tonnes + 1w/4w chg, weekend gap %,
VIX, ADX(14) D1.

### Web Search (supplementary)
- Central-bank speaker comments this week affecting gold
- Macro / geopolitical news affecting gold
- Scheduled high-impact events next week (FOMC, NFP, CPI, US Retail Sales) — exact dates/times UTC

## Step 2 — Read Data
Read the full `weekly_pull_{YEAR}_W{WW}.txt` before analysis.

## Step 3 — 5-Section Analysis

**1. Fundamental Analysis** — DFII10 (level + 20d slope vs prior `baseline_dfii10`), DXY (level +
20d slope), Fed posture, 10Y nominal / breakeven. Bias: BULLISH/BEARISH/NEUTRAL + confidence
HIGH/MEDIUM/LOW. Falling real yield = bullish gold; rising = bearish. Flag regime shift vs baseline.

**2. News Analysis** — web-search results: scheduled high-impact calendar next week (dates/times
UTC, mark hard-block events), central-bank commentary, geopolitical drivers. Note any no-trade windows.

**3. Technical Analysis** — key S/R zones as boxes (swing points + Volume Profile), EMA 20/50/200
position, RSI state (divergence? — note: gold is momentum, RSI>70 is NOT a short signal), D1 ATR
regime (compressed vs 20d median), weekly pivots in play, ADX regime.

**4. Positioning & Flows** — COT MM net + 1w change (note: crowded long is NOT a contrarian short
on gold — momentum asset), GLD ETF tonnes + 1w/4w change, weekend gap %. Flag contradictions vs bias.

**5. Top-Down Analysis (D→H4→1H)** — assess structure on Daily, then H4, then H1. State alignment
toward each candidate direction: D1 trend → H4 trend → H1 trend. This feeds Zone Confluence Z4.
`mtf_alignment`: ALIGNED / MIXED / OPPOSING.

## Step 4 — Build Trading Zones (Zone Confluence, R1)
For each candidate zone, score Z1–Z7 (`confluence_criteria.md`), never double-count:
```
Z1 Structural Zone 2.0 (MANDATORY) | Z2 DFII10 slope 2.5 | Z3 DXY slope 1.5
Z4 Top-down MTF 2.0 | Z5 EMA regime 1.0 | Z6 ATR compression 0.5 | Z7 VP node 0.5
```
- Publish a zone if score ≥ 5.0 (Z1 mandatory). Max 3 zones, at most 1 counter.
- Counter zone: macro (Z2+Z3) scores 0; RSI divergence MANDATORY; macro conf must be LOW/MEDIUM.
- Apply vetoes: VIX>35 blocks shorts; never score RSI>70 / COT>200k as short.
- For each zone write the IF/THEN in one sentence + name the zone (Primary / Secondary / Counter),
  direction, zone box (range), score, signals hit.
- SL / offset / TP are NOT frozen here — computed at `/validate`. But name the TP structural anchor
  and compute indicative R for the report.

## Step 5 — Write the Forecast Report
Use template `wiki/system/templates/weekly_forecast.md`. Frontmatter:
```yaml
type: weekly_forecast
week: YYYY-WNN
generated: YYYY-MM-DD
macro_bias: BULLISH | BEARISH | NEUTRAL
macro_confidence: HIGH | MEDIUM-HIGH | MEDIUM | MEDIUM-LOW | LOW
mtf_alignment: ALIGNED | MIXED | OPPOSING
best_zone: PRIMARY | SECONDARY | NONE
conviction: HIGH | MEDIUM-HIGH | MEDIUM | MEDIUM-LOW | LOW
baseline_dfii10: x.xx
baseline_dxy: xxx.xxx
weekend_gap_pct: x.xxx
cot_mm_net: ±xxxxx
cot_mm_net_chg: ±xxxxx
etf_gld_tonnes: xxxx.xx
etf_gld_wk_chg: ±xx.xx
adx_val: xx.x
```
Body: Fundamental / News / Technical / Positioning & Flows / Top-Down sections, then each Trading
Zone with box + Zone Confluence score + signals + IF/THEN + TP anchor + indicative R. Weekly bias
statement (≤3 lines). No-trade events calendar. `> [!warning]` contradiction callout if
macro vs technical vs positioning conflict (and lower conviction to MEDIUM per Contradiction Protocol).

Save to `forecasts/weekly/xauusd/YYYY-WNN.md` (Claude writes markdown directly — no DB).

## Post-Forecast Updates
1. Rewrite `wiki/system/core/macro/yield_environment.md` with this week's macro snapshot.
2. Update `_HOT.md`: Active Forecast link + one-line bias; all new zones PENDING with box + direction;
   week number; reset risk used + `weekly_reforecast_count` to 0 if new week; refresh Pending Actions.
3. Update `_INDEX.md`: add the new forecast file under Forecasts.
