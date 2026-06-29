---
type: weekly_forecast
instrument: eurgbp
week: 2026-W24
generated: 2026-06-09
macro_bias: NEUTRAL
macro_confidence: LOW
mtf_alignment: MIXED
best_zone: PRIMARY
conviction: MEDIUM
baseline_rate_diff: -1.73     # ECBDFR 2.00 − SONIA 3.73 (EUR−GBP; weak/context, EG2 dead)
baseline_dxy: 99.728          # context only — DXY irrelevant to the cross
weekend_gap_pct: 0.045
adx_val: 13.8
spot: 0.86352
---

# EURGBP — Weekly Forecast 2026-W24 (CROSS, first forecast)

> First `/weekly eurgbp` since onboarding (D023). Mean-reverting, macro-light cross. Sizing in USD
> (no GBP convert). All orders route through the FX netting ledger ([[currency_exposure]]) — EURGBP
> IS the cross risk-axis vs any held EURUSD/GBPUSD.

## Bias — NEUTRAL (range-bound), conviction MEDIUM
EURGBP is **ranging** (ADX 13.8) inside ~0.8614–0.8682. Spot 0.86352 sits mid-lower range, below
EMA50 (0.86637) + EMA200 (0.86653), RSI(14) D1 43.7 and falling, ATR compressed (0.00262 < 0.00329
20d median), %B 0.27. No trend to follow — the edge is **fading the range extremes** (EG3/EG4).
Near-term drift is mildly soft (RSI falling, MACD bearish but ADX 13.8 = weak) → the support-fade
LONG is the more immediate setup; the resistance-fade SHORT needs a bounce first.

## 1. Fundamental / Macro (NON-SCORING tilt — EG2 dead)
Cross macro is thin/dead on free daily data. EUR−GBP rate diff (ECBDFR 2.00 − SONIA 3.73) = **−1.73,
flat 20d** → no directional pull (GBP carries higher rate, long-standing, already priced). VIX 21.51
(spiked) → weak EURGBP-**up** tilt (risk-off favors EUR over GBP — inverted vs majors); minor support
for the LONG, scored only as Z4 0.5. **No DXY, no US-rate input** (no USD leg). Bias set by structure,
not macro.
> Note: the weekly-pull MACRO block prints the gold template (DFII10/breakeven) — not cross-aware yet
> (cosmetic; macro is non-scoring for eurgbp anyway). Rate-diff read taken from FRED directly.

## 2. News (UTC) — cross hard-blocks = ECB/BoE/UK/EZ; US = caution only
- **US CPI Wed 2026-06-10** — CAUTION only for the cross (no USD leg); not a hard block. PPI Thu, UMich Fri.
- ⚠️ **Verify at /validate:** UK labour-market (likely ~06-09/06-16) and UK monthly GDP/IP (likely
  ~06-11/06-12) — if scheduled this week these ARE EURGBP hard blocks (V3). Web calendar didn't
  confirm exact dates; `/validate` Query A re-checks daily. BoE decision is W25 (~06-18), not this week.

## 3. Technical — range map (fade points)
| Level | Price | Role |
|---|---|---|
| Swing highs (prior) | 0.8731 / 0.8723 / 0.8721 | upper range ceiling (TP-ext) |
| 20d / recent high | 0.86816 (05-29) | range top |
| Weekly R2 | 0.86756 | resistance |
| EMA50 / EMA200 D1 | 0.86637 / 0.86653 | overhead cluster (fade) |
| Weekly R1 | 0.8657 | resistance / TP |
| BB mid / Weekly PP | 0.8657 / 0.86422 | range mid (TP) |
| **Spot** | **0.86352** | mid-lower range |
| Fib 78.6% | 0.86284 | minor |
| Weekly S1 | 0.86236 | support |
| 20d low / swing-low cluster | 0.86139 / 0.86084–0.8613 | range floor (fade) |
| Weekly S2 | 0.86088 | support |
RSI 43.7 (mid, falling) · MACD bearish (weak, ADX 13.8) · BB lower 0.86099 / upper 0.87042.

## 4. Positioning & Flows
COT disabled for the cross (no single CFTC EURGBP contract; derived 6E/6B not built). Weekend gap
+0.045% = NOISE. No flow signal.

## 5. Top-Down (D→H4→1H) — MIXED (ranging)
D1 ranging below EMAs (mild down-drift). H4 chopping 0.8627–0.8655. H1 oscillators are the validated
entry trigger (t up to 7.45). Alignment MIXED — informs the FADE, not a trend.

---

## Trading Zones

### PRIMARY — LONG (support fade) · box 0.8608–0.8624 · Zone Confluence 8.0/10
Range-floor fade: 20d low 0.86139 + swing-low cluster 0.8608–0.8614 + weekly S1/S2 (0.86236/0.86088)
+ Fib 78.6% 0.86284 just above.
- **IF** EURGBP dips into **0.8608–0.8624** AND an H1/H4 oversold bullish reversal prints at the zone
  (RSI<35 / Stoch<20 / %R<−80 + reversal candle on close), **THEN** buy the fade back toward range
  mid 0.8657.
- Z1 structural 3.0 (MAND ✅) · Z2 D1 oscillator 2.0 (RSI falling→oversold at zone) · Z3 H1 oscillator
  1.0 · Z4 sentiment tilt 0.5 (VIX-up favors EURGBP) · Z5 ADX<25 1.0 (13.8 ✅) · Z6 compression/lower-BB
  0.5 · Z7 Williams/Stoch 0.5 → **8.0**.
- **TP anchor:** weekly PP 0.86422 (TP1 area) → R1 0.8657 (TP2/structural). Indicative ~2.5–3R on an
  H4-ATR stop below 0.8605. SL/offset computed at `/validate`.

### SECONDARY — SHORT (resistance fade) · box 0.8664–0.8682 · Zone Confluence 7.5/10
Range-ceiling fade: EMA50/200 cluster 0.86637/0.86653 + weekly R2 0.86756 + 20d/swing high 0.86816 +
upper BB 0.87042.
- **IF** EURGBP bounces into **0.8664–0.8682** AND an H1/H4 overbought bearish reversal prints at the
  zone (RSI>65 / Stoch>80 + reversal candle on close), **THEN** sell the fade back toward range mid
  0.8657 → PP 0.86422.
- Z1 structural 3.0 (MAND ✅) · Z2 D1 oscillator 1.5 (needs bounce to overbought) · Z3 H1 oscillator
  1.0 · Z4 tilt 0 (VIX-up works against a short) · Z5 ADX<25 1.0 ✅ · Z6 compression/upper-BB 0.5 ·
  Z7 Williams/Stoch 0.5 → **7.5**.
- **TP anchor:** range mid 0.8657 (TP1) → weekly PP 0.86422 (TP2/structural) → S1 0.86236 stretch.

### COUNTER — NONE
Bias is NEUTRAL/range — both zones are range fades, neither is counter-trend. No third zone.

---

## Bias statement
EURGBP ranging (ADX 13.8) 0.8614–0.8682; fade both edges. **Buy 0.8608–0.8624 support**, **sell
0.8664–0.8682 resistance** — wait for an oscillator-extreme reversal at the zone (validated H1 trigger).
Macro non-directional; conviction MEDIUM (clean range, but a UK data hard-block this week could
interrupt — verify at `/validate`).

## No-trade calendar (verify daily at /validate)
- US CPI Wed 06-10 = caution (cross barely reacts). UK labour / UK GDP this week = HARD BLOCK if
  scheduled (confirm dates). BoE W25 (~06-18). No EURGBP entries 2h before any ECB/BoE/UK/EZ tier-1.
