---
type: weekly_forecast
instrument: gbpusd
week: 2026-W24
generated: 2026-06-09
macro_bias: BEARISH
macro_confidence: MEDIUM-HIGH
mtf_alignment: ALIGNED
best_zone: PRIMARY
conviction: MEDIUM
baseline_dgs2: 4.17
baseline_policy_diff: -0.111
baseline_dxy: 99.959
weekend_gap_pct: -0.044
cot_net: -51483
cot_net_chg: +12289
adx_val: 16.1
---

# GBPUSD Weekly Forecast — 2026-W24

> **First GBPUSD forecast under the mean-reversion system (D021).** Fade extremes; SHORT zones are
> sell-the-bounce fades into resistance, NOT breakout-chasing. GBP edges run D1-reversal + H1
> oscillators. Generated mid-week (Tue) to instantiate the FX pipeline — re-anchor next Sunday `/weekly`.

**Bias: BEARISH GBP / MEDIUM-HIGH macro, conviction MEDIUM.** Same USD-strength shock as EUR
(06-05) broke price below the 1.33683 swing-low. Sell bounces into the 1.340–1.345 resistance
cluster. CPI Wed 06-10 = binary risk → conviction capped MEDIUM.

## 1. Fundamental / Macro — BEARISH GBP
- **US 2Y (DGS2) 4.17%**, +0.19% wk, **20d slope +0.0213/day RISING** → USD-rate momentum up = **bearish GBPUSD** (scored M1/M2). vs `baseline_dgs2` 4.17.
- **DXY 99.959, +0.74% wk** (rising). No fresh 1-day jump today (Δ −0.09); weekly trend USD-up. DXY 1d jump >0.5 intraday = strongest short trigger — watch.
- **VIX 21.51, spiked +6.1 today** → **bearish GBP** (GBP is a risk currency; spikes hit it hardest, t=−5.60 in research) AND **vetoes all LONG zones**. Not >35.
- Policy diff US−UK −0.11% (flat; US slightly below UK) — CONTEXT only, carry-diff DEAD (not scored).
- Net: all scored macro legs SHORT.

## 2. News — no-trade windows (US calendar drives the USD leg)
| Event | Date/UTC | Rule |
|---|---|---|
| US CPI | Wed 2026-06-10 ~12:30 | **HARD BLOCK** — cancel live limits within 2h of London/NY open |
| US PPI | Thu 2026-06-11 ~12:30 | caution |
| UMich sentiment | Fri 2026-06-12 ~14:00 | caution |
No BoE decision this week. Watch UK data prints (caution, GBP-leg).

## 3. Technical — mean-reversion (fade), price below value
- Price **1.33498**, below EMA50 (1.34466) and EMA200 (1.34034); MACD negative; D1 ADX **16.1 = RANGING** (strong fade regime, non-trend gate passes comfortably).
- **D1 RSI 40.1** (was 38.1) — low but not deep-oversold; **%B 0.15** (lower band 1.33195).
- Resistance cluster overhead: golden pocket **1.34222** + VP POC **1.343** + EMA200 1.34034 + EMA50 1.34466 + 50% fib 1.34389 → prime sell-the-bounce zone. Shallower role-reversal: VP VAL **1.33769** + broken swing-low **1.33683** + weekly PP 1.33852.
- Stance: do NOT short the low here (anti-edge). Rest sell-limits ABOVE; bounce into them = H4/H1 overbought fade.

## 4. Positioning & Flows
- COT 6B spec net **−51,483 (net SHORT), +12,289 w/w** (specs trimming shorts) — context only; FX COT not a contrarian trigger. Specs already lean short = aligned with bearish bias.
- Weekend gap −0.044% = NOISE.

## 5. Top-Down (D→H4→1H)
- D1: lower-high/lower-low since 05-25 high 1.35095 → down. H4: down since 06-05. H1: down.
- `mtf_alignment: ALIGNED` (down) — supports fading bounces short, not buying.

---

## Trading Zones

### PRIMARY — SHORT 1.3400–1.3447  | Zone Confluence 8.0/10
Resistance cluster: golden pocket 1.34222 + VP POC 1.343 + EMA200 1.34034 + 50% fib 1.34389 + EMA50 1.34466.
- **IF** price bounces into 1.3400–1.3447 **AND** `/validate` confirms a bearish H1/15M reversal with D1/H4 overbought, **THEN** sell-limit short (fade into the strongest resistance).
- Signals: Z1 structural D1-extreme 2.5 ✓ | Z2 D1 osc-extreme 2.0 (entry-confirmed) | Z3 H1 osc 0.75 (entry) | Z4 macro 1.5 ✓ (US2Y rising + VIX spike) | Z5 ADX<25 1.0 ✓ | Z6 compression 0.5 ✓. (Z7 seasonal/Williams 0.)
- TP structural anchor: weekly S1 **1.32866** → swing low 1.31613 (compute R at `/validate`; indicative ≥3R).
- Invalidate: D1 close > 1.3460 (above EMA50/cluster) = bounce became trend.

### SECONDARY — SHORT 1.3370–1.3390  | Zone Confluence 6.5/10
Role-reversal: VP VAL 1.33769 + broken swing-low 1.33683 + weekly PP 1.33852.
- **IF** price bounces into 1.3370–1.3390 **AND** `/validate` confirms bearish reversal, **THEN** sell-limit short (shallower fade; smaller expected overbought — lower confidence than Primary).
- Signals: Z1 2.5 ✓ | Z2 1.0 (modest bounce, partial) | Z4 macro 1.5 ✓ | Z5 1.0 ✓ | Z6 0.5 ✓.
- TP anchor: weekly S1 1.32866 (compute R at `/validate`).
- Invalidate: D1 close > 1.3405.

### COUNTER — NONE
LONG bounce is the natural mean-reversion trade but **VIX 1d spike>3 vetoes all LONG zones** (GBP
crashes on risk-off, the largest measured anti-long signal). No deep oversold support extreme nearby
(next strong support S1 1.32866 / 1.31613 is below, not a current fade level). No counter zone.

---

## Bias Statement
Bearish GBP on USD-strength (rising US 2Y, firm DXY, VIX risk-off spike). Sell the bounce into the
1.340–1.345 cluster (Primary) or 1.337–1.339 (Secondary). No longs (VIX veto). CPI Wed is the binary
risk — cancel unfilled limits within 2h of the print.

> [!warning] Price is short-term low and ADX is very low (16.1) — chop risk. Limits rest ABOVE spot
> (fade a bounce, never chase the low); conviction held at MEDIUM.

## No-Trade Calendar
CPI Wed 06-10 (hard block) · PPI Thu 06-11 (caution) · UMich Fri 06-12 (caution).
