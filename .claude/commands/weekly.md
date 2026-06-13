Run the full weekly forecast → produce Trading Zones.

Argument: `[instrument]` ∈ {xauusd, eurusd, gbpusd, eurgbp, audusd, nzdusd, usdcad, usdchf, usdjpy, eurjpy, gbpjpy} (default xauusd).
One instrument per invocation.
(eurgbp = CROSS: macro-light mean-reversion, no VIX-veto, European event blocks. audusd: no VIX-veto +
no DXY block — VIX level INVERTED tilt, DXY-jump dead; RBA/AU-CPI/China events. nzdusd: macro-light,
weakest edges — squeeze-led; no VIX/DXY/US2Y gates; RBNZ/NZ-CPI events; fewer zones expected.
usdcad = **USD-BASE**: long pair = LONG USD — US2Y flipped, VIX>20 → SHORT bias, COT 6C inverted,
🛢 oil tilt; BoC/CAD-CPI/jobs events. usdchf = **USD-BASE**: DXY 20d SLOPE is the live macro (only
pair beyond EUR/GBP), VIX WASHOUT (no gate/score), COT 6S inverted; SNB quarterly + regime note.
usdjpy = **USD-BASE + JPY-quoted + ASYMMETRIC**: NOT the fade template — LONG = drift continuation
(squeeze/calm/dip), SHORT = D1/H4 oscillator extremes only, H1-only shorts PROHIBITED; DXY 20d slope
live, VIX washout, COT 6J inverted; pip 0.01, 3dp; BoJ/MoF intervention regime ≥158.
eurjpy = **CROSS-JPY, macro NONE**: symmetric mean-reversion on long-drift floor — buy washouts,
fade extension, never chase; NO VIX/DXY/rate gates (all dead); pip 0.01, 3dp; COT EUR/JPY XRATE
direct but THIN; BoJ/MoF + ECB hard blocks — interventions slam crosses.
gbpjpy = **CROSS-JPY #2, macro NONE**: extension-fade, SHORT-side dominant, on strongest long-drift
floor (D1 LNG 56.7%); NO calm/squeeze row (dead — only JPY pair without it); NO VIX/rate gates;
pip 0.01, 3dp; **COT DISABLED** (no CFTC cross contract); BoJ/MoF + BoE hard blocks; highest ATR.)

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
   was the zone simply never reached?
4. Carry it forward: if the same thesis is about to be re-issued, state explicitly why it is still
   valid given last week's result (or why the read changes). A bias that BROKE two weeks running on
   the same structural reason → cap conviction MEDIUM and flag it.
5. If the break exposes a **repeatable** lesson (not noise), add one line to
   `wiki/system/{instrument}/{instrument}_profile.md` (or `setup_library.md` for a cross-pair
   pattern) — this is how the profile learns. One-off / event-driven misses do NOT get recorded.
Write the result into Section 0 of the report (template). NO prior forecast (first week) → state
"first forecast — no retrospective" and skip.

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
- nzdusd: **macro nearly all DEAD** — US2Y slope dead (t=−0.7), DXY dead, VIX spike dead. Only weak
  inverted VIX LEVEL tilt (VIX>20→long t=2.18, VIX<15→short t=2.38). Bias = structure/oscillator/
  squeeze, not macro. No daily RBNZ series. Dairy/China = narrative context.
- usdcad (**USD-BASE — every USD intuition flips**): US2Y slope vs `baseline_dgs2` with FLIPPED
  polarity (rising US2Y = bullish USDCAD, t≈2.0); **VIX LEVEL = fade-the-USD regime: VIX>20 →
  SHORT bias (+5.5pp t≈3.9), VIX<15 → LONG bias**; 🛢 WTI 5d>+5% → SHORT tilt (t=1.67, ~1wk FRED
  lag); DXY-jump DEAD. COT 6C INVERTED (spec long CAD = bearish USDCAD — snapshot prints both).
- usdchf (**USD-BASE, DXY proxy**): **DXY 20d SLOPE = the live macro** (rising → bullish USDCHF
  t=2.32, falling → bearish t=2.34 — only pair beyond EUR/GBP where DXY scores). **VIX = WASHOUT
  (haven-vs-haven): no gate, no score.** US2Y slope flipped weak tilt (t≈1.4). DXY 1d jump = anti
  (fade, never block). COT 6S INVERTED. ⚠ SNB regime: shorts near 0.78–0.80 fight the SNB.
- usdjpy (**USD-BASE, JPY-quoted, ASYMMETRIC**): **DXY 20d SLOPE = the live macro** (rising →
  bullish t=2.21 / falling → bearish t=1.73). **VIX = WASHOUT** (haven-vs-haven, like CHF): no gate,
  no score. **US2Y DEAD** (t≈0.1–0.6 — carry lives in the D1 long drift, baseline LNG 58.9%). DXY
  1d jump = anti. COT 6J INVERTED. ⚠ MoF/BoJ regime: longs ≥158 at fresh highs fight the MoF
  (2022/2024 interventions = 300–500 pip slams); BoJ decision days hard block.
- eurjpy (**CROSS-JPY — macro NONE, first 100% price-driven pair**): no USD leg, no DXY/US2Y rows;
  ECB leg (ECBDFR) scans ANTI (t −1.2/−1.3) — context line only; **VIX DEAD** (E13 t=0.91) despite
  carry-barometer reputation — no gate, no score. Bias = structure/oscillator/calm-regime only.
  ⚠ MoF/BoJ regime shared with usdjpy — interventions slam crosses; spot 185+ = record territory.
- gbpjpy (**CROSS-JPY #2 — macro NONE, second 100% price-driven pair**): no USD leg, no DXY/US2Y
  rows; SONIA leg (IUDSOIA) scans dead (t 0.58/0.29) — context line only; **VIX DEAD** (E13 t=0.89,
  spike −1.81 mildly anti) — no gate, no score. Bias = structure/oscillator/session only.
  ⚠ MoF/BoJ regime shared — GBPJPY slams are the LARGEST of the crosses; spot 214+ = record territory.
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
- **nzdusd:** Z1 Structural 2.0 (MAND) | Z2 H4 oscillator extreme 2.0 | Z3 compression/squeeze 2.0 (strongest NZD signal) | Z4 H4 band over-extension 1.5 | Z5 big-figure LONG 1.0 | Z6 non-trend ADX<25 1.0 | Z7 VIX regime tilt (weak, inverted) 0.5. (NO US2Y/DXY rows — dead for NZD.)
- **usdcad (USD-base):** Z1 Structural 2.0 (MAND) | Z2 H4 oscillator extreme 2.0 | Z3 H4 band over-extension 2.0 (BB-upper short t=3.19) | Z4 compression/squeeze 1.5 | Z5 VIX regime fade-USD 1.0 | Z6 US2Y-flipped + oil tilt 1.0 | Z7 non-trend ADX<25 0.5. (NO DXY row; COT inverted = context.)
- **usdchf (USD-base):** Z1 Structural 2.0 (MAND) | Z2 H1 oscillator extreme cluster 2.0 (short t 4.0–5.5) | Z3 DXY 20d slope aligned 2.0 | Z4 compression/squeeze (H1 TTM/calm) 1.5 | Z5 D1 pattern/extreme 1.0 | Z6 H4 band/big-figure 1.0 | Z7 non-trend ADX<25 0.5. (NO VIX row — washout; H4 thin, H1-centric.)
- **usdjpy (USD-base, DIRECTION-AWARE):** Z1 Structural 2.0 (MAND) | Z2 side engine 2.5 — LONG: D1 TTM squeeze/calm ATR (t 3.3–4.5) · SHORT: ≥2 of D1 RSI>65 / H4 CCI>+100 / H4 Keltner-high (t 2.1–3.1) | Z3 DXY 20d slope aligned 2.0 | Z4 LONG dip at 20d low 1.0 | Z5 D1 pattern (PSAR/engulf) 1.0 | Z6 LONG big-figure 1.0 | Z7 not-extended ADX<25 0.5. (NO VIX row; counter = SHORT.)
- **eurjpy (cross-JPY, NO macro):** Z1 Structural 2.0 (MAND) | Z2 extreme engine 2.5 — LONG: washout (D1 Stoch<20 / H1 Keltner-low / 20d low, t 2.6–3.1) · SHORT: extension (D1/H4 Keltner-high / RSI>65–70, t 2.8–3.5) | Z3 calm/squeeze regime 1.5 (LONG full, SHORT half) | Z4 H4 oscillator stack 1.5 | Z5 D1 trigger (inside-bar/compression) 1.0 | Z6 big-figure 1.0 | Z7 not-extended ADX<25 0.5. (NO macro row at all; counter = SHORT.)
- **gbpjpy (cross-JPY, NO macro, NO calm row):** Z1 Structural 2.0 (MAND) | Z2 extreme engine 2.5 — SHORT: extension (D1/H4 Keltner-high / BB-upper / RSI>65 / CCI>+100, t 3.0–4.6) · LONG: washout (D1/H4 Keltner-low / RSI<35 / CCI<−100 / 20d low, t 2.2–2.6) | Z3 multi-TF extreme alignment ≥2 TFs 1.5 | Z4 H4 oscillator stack 1.5 | Z5 H4 reversal trigger (MACD-down/pin) 1.0 | Z6 big-figure 1.0 | Z7 not-extended ADX<25 0.5. (NO macro, NO calm/squeeze; counter = SHORT.)

Rules: publish if score ≥ 5.0 (Z1 mandatory). Max 3 zones, ≤1 counter.
- Counter zone (xauusd): macro Z2+Z3 score 0; RSI divergence MANDATORY; macro conf LOW/MEDIUM.
- Vetoes: xauusd VIX>35 blocks shorts + never score RSI>70/COT>200k short. **FX majors: VIX>35 or VIX
  spike>3 blocks LONGs; DXY 1d jump against a zone blocks it; never score trend-follow.**
  **eurgbp (cross): NO VIX veto, NO DXY block** (risk-off → EURGBP up, inverted; DXY irrelevant). Only
  veto = D1 ADX>30 trending against the fade. Never score trend-follow.
  **audusd: NO VIX veto, NO DXY block** (VIX level scores inverted in Z5; DXY-jump dead). Only veto =
  D1 ADX>30 trending against the fade. Never score trend-follow.
  **nzdusd: NO VIX veto, NO DXY block, NO US2Y gate** (all dead/weak for NZD). Only veto = D1 ADX>30
  trending against the fade. Never score trend-follow; never score big-figure as a SHORT (anti-edge −2.68).
  **usdcad (USD-base): NO VIX veto, NO DXY block** (VIX level scores directionally in Z5 — high VIX
  favors SHORTs; DXY dead). Only veto = D1 ADX>30 trending against the fade. Never score trend-follow;
  never score bearish-engulf/Donchian-breakdown continuation (anti-edge t=−3.83/−2.83).
  **usdchf (USD-base): NO VIX veto/score (washout), NO DXY-jump block** (DXY scores via 20d SLOPE in
  Z3 only). Vetoes: D1 ADX>30 trending against the fade; SNB decision/communication day (quarterly
  Mar/Jun/Sep/Dec Thu 08:30 UTC); SHORT zone inside 0.78–0.80 historic-low band → conviction cap
  MEDIUM. Never score trend-follow (H1 momentum continuation anti-edge t −2.6 to −3.4).
  **usdjpy (USD-base, ASYMMETRIC): NO VIX veto/score, NO DXY-jump block** (DXY scores via 20d slope
  Z3). Vetoes: BoJ decision day / active MoF jawboning = HARD BLOCK; LONG zone ≥158 at fresh
  multi-decade highs → conviction cap MEDIUM (MoF regime); **NO H1-only SHORT zones** (H1 fade
  anti-edge t=−3.3 — shorts need D1/H4 extreme evidence); no chasing extension (ADX>25 uptrend-
  continuation long anti-edge t −3.3/−3.4); turn-of-month LONG −0.5.
  **eurjpy (cross-JPY): NO VIX veto/score, NO DXY/US2Y anything** (cross, all dead). Vetoes: BoJ
  decision / active MoF jawboning / ECB decision = HARD BLOCK (interventions slam crosses); LONG
  zone at fresh record highs during intervention watch → conviction cap MEDIUM; zones are REVERSION
  zones only — never breakout/continuation (C26 anti −4.2, Donchian-up −2.6, momentum shorts −3.3);
  turn-of-month LONG −0.5 (t=−3.10).
  **gbpjpy (cross-JPY #2): NO VIX veto/score, NO DXY/US2Y anything** (cross, all dead). Vetoes: BoJ
  decision / active MoF jawboning / BoE decision = HARD BLOCK (interventions slam GBPJPY hardest);
  LONG zone at fresh record highs during intervention watch → conviction cap MEDIUM; REVERSION zones
  only — never breakout/continuation (C26 anti −5.0/−4.7, band-break long B1r −3.4, momentum shorts
  C8 −3.75); turn-of-month LONG −0.5 (G9 −2.99); January LONG caution (G6 −2.28); NO calm/squeeze
  scoring (dead).
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
   Then refresh the calibration report (reads the freshly-resolved outcomes):
   `bash scripts/pyrun.sh scripts/calibration.py` → rewrites `wiki/system/core/calibration.md`.
   Scan it: any instrument×direction or R1 bucket flipped to **DEAD** (n≥min-n) → flag in `_HOT.md`
   Pending Actions for a confluence-criteria review before publishing more of that edge.
2. Rewrite `wiki/system/core/macro/yield_environment.md` with this week's macro snapshot (note which instrument).
3. Update `_HOT.md`: Active Forecast link + bias; new zones PENDING (box + direction) tagged by instrument;
   week number; reset risk used + `weekly_reforecast_count` to 0 if new week; refresh Pending Actions.
4. Update `_INDEX.md`: add the new forecast file under Forecasts.
