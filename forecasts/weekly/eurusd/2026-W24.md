---
type: weekly_forecast
instrument: eurusd
week: 2026-W24
generated: 2026-06-09
macro_bias: BEARISH
macro_confidence: MEDIUM-HIGH
mtf_alignment: ALIGNED
best_zone: PRIMARY
conviction: MEDIUM
baseline_dgs2: 4.17
baseline_policy_diff: 1.62
baseline_dxy: 99.965
weekend_gap_pct: -0.016
cot_net: +15729
cot_net_chg: +19485
adx_val: 19.5
---

# EURUSD Weekly Forecast — 2026-W24

> **First EURUSD forecast under the mean-reversion system (D021).** Character = fade extremes; the
> SHORT zones below are sell-the-bounce fades into resistance, NOT breakout-chasing. Generated
> mid-week (Tue) to instantiate the FX pipeline — re-anchor on the next Sunday `/weekly`.

**Bias: BEARISH EUR / MEDIUM-HIGH macro, conviction MEDIUM.** Sell bounces into resistance; price
broke below the 1.1577 swing-low on a USD-strength shock (06-05). Short-term oversold (D1 RSI 35.9,
%B 0.05) → expect a corrective bounce to sell. CPI Wed 06-10 = binary risk → conviction capped MEDIUM.

## 1. Fundamental / Macro — BEARISH EUR
- **US 2Y (DGS2) 4.17%**, +0.19% on week, **20d slope +0.0213/day RISING** → USD-rate momentum up = **bearish EURUSD** (scored macro, M1/M2). vs `baseline_dgs2` 4.17 (this print = baseline).
- **DXY 99.965, +0.75% on week** (rising). No fresh 1-day jump today (Δ −0.09), but the weekly trend is USD-up. A DXY 1d jump >0.5 would be the strongest short trigger — watch intraday.
- **VIX 21.51, spiked +6.1 today** (was ~15.4). **VIX 1d spike>3 → bearish EUR** (risk-off USD bid) AND **vetoes all LONG zones** this week. Not >35, so no hard short-block.
- Policy diff US−EZ +1.62% (flat) — CONTEXT only, carry-diff measured DEAD (not scored).
- Net: every scored macro leg points SHORT.

## 2. News — no-trade windows (US calendar drives the USD leg)
| Event | Date/UTC | Rule |
|---|---|---|
| US CPI | Wed 2026-06-10 ~12:30 | **HARD BLOCK** — cancel any live limit within 2h of London/NY open |
| US PPI | Thu 2026-06-11 ~12:30 | caution |
| UMich sentiment | Fri 2026-06-12 ~14:00 | caution |
ECB deposit rate stable 2.00%, no decision this week. No EUR-leg central-bank event.

## 3. Technical — mean-reversion (fade), price below value
- Price **1.15394**, below EMA50 (1.16501) and EMA200 (1.16151); MACD negative; D1 ADX **19.5 = RANGING** (fades favored, non-trend gate passes).
- **D1 RSI 35.9** (was 32.9 on 06-05) — near-oversold, ticking up = bounce risk. **%B 0.05** (lower band 1.15298 ≈ spot).
- Resistance cluster overhead: golden pocket **1.16188** + VP POC **1.16332** + EMA200 1.16151 + EMA50 1.16501 → prime sell-the-bounce zone. Shallower role-reversal: broken swing-low **1.15774** + VP VAL **1.15925** + weekly PP 1.1569.
- Mean-reversion stance: do NOT short the current low (anti-edge to chase breakdown). Rest sell-limits ABOVE at resistance; a bounce into them = H4-overbought fade.

## 4. Positioning & Flows
- COT 6E spec net **+15,729, +19,485 w/w** (specs adding longs into the drop) — context only; FX COT not a contrarian trigger. Mild warning vs the bearish bias (specs leaning the other way).
- Weekend gap −0.016% = NOISE.

## 5. Top-Down (D→H4→1H)
- D1: lower-high / lower-low since 05-29 high 1.16857 → down. H4: clean down since 06-05. H1: down.
- `mtf_alignment: ALIGNED` (down) — supports fading bounces short, not buying.

---

## Trading Zones

### PRIMARY — SHORT 1.1618–1.1640  | Zone Confluence 7.5/10
Resistance cluster: golden pocket 1.16188 + VP POC 1.16332 + EMA200 1.16151 + EMA50 1.16501.
- **IF** price bounces into 1.1618–1.1640 **AND** `/validate` confirms a bearish H1/15M reversal with H4 overbought, **THEN** sell-limit short (fade the bounce into the strongest resistance).
- Signals: Z1 structural 2.0 ✓ | Z2 H4 osc-extreme 2.0 (entry-confirmed) | Z5 macro 1.5 ✓ (US2Y rising + VIX spike) | Z6 ADX<25 1.0 ✓ | Z7 compression 1.0 ✓. (Z3 band 0, Z4 big-figure 0.)
- TP structural anchor: weekly S1 **1.1473** → D1 swing low 1.14451 (compute R at `/validate`; indicative ≥3R).
- Invalidate: D1 close > 1.1655 (above EMA50 / cluster) = bounce became trend.

### SECONDARY — SHORT 1.1574–1.1593  | Zone Confluence 6.5/10
Role-reversal: broken swing-low 1.15774 + VP VAL 1.15925 (weekly PP 1.1569 just below).
- **IF** price bounces into 1.1574–1.1593 **AND** `/validate` confirms bearish reversal, **THEN** sell-limit short (shallower fade; smaller expected overbought — lower confidence than Primary).
- Signals: Z1 2.0 ✓ | Z2 1.0 (modest bounce, partial) | Z5 1.5 ✓ | Z6 1.0 ✓ | Z7 1.0 ✓.
- TP anchor: weekly S1 1.1473 (compute R at `/validate`).
- Invalidate: D1 close > 1.1605.

### COUNTER — NONE
A LONG bounce is the obvious mean-reversion trade from oversold, but **VIX 1d spike>3 vetoes all LONG
zones** this week (risk-off USD bid), and there is no deep oversold support extreme nearby (next strong
support 1.1445/1.1415 is far). No counter zone.

---

## Bias Statement
Bearish EUR on USD-strength (rising US 2Y, firm DXY, VIX risk-off spike). Sell the bounce into
resistance — Primary at the 1.162–1.164 cluster, Secondary at 1.157–1.159. No longs (VIX veto).
CPI Wed is the binary risk — cancel unfilled limits within 2h of the print.

> [!warning] Mild conflict: COT specs are adding EUR longs into the drop, and price is short-term
> oversold (bounce risk) — hence limits rest ABOVE spot and conviction is held at MEDIUM, not higher.

## No-Trade Calendar
CPI Wed 06-10 (hard block) · PPI Thu 06-11 (caution) · UMich Fri 06-12 (caution).
