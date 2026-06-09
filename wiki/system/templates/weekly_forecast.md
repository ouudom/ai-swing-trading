---
type: system
updated: 2026-06-02
confidence: high
tags: [template, forecast, weekly]
related: [constitution, confluence_criteria]
---

# Weekly Forecast Template (v2 — Trading Zones)

File: `forecasts/weekly/<instrument>/YYYY-WNN.md` — immutable after Monday open. Claude writes
markdown directly (no DB). Goal: publish up to 3 Trading Zones (≤1 counter), each scored by Zone
Confluence. Instrument ∈ {xauusd, eurusd, gbpusd}; xauusd=momentum, FX=mean-reversion (D021).

---

## Frontmatter
```yaml
---
type: weekly_forecast
instrument: xauusd | eurusd | gbpusd
week: YYYY-WNN
generated: YYYY-MM-DD
macro_bias: BULLISH | BEARISH | NEUTRAL
macro_confidence: HIGH | MEDIUM-HIGH | MEDIUM | MEDIUM-LOW | LOW
mtf_alignment: ALIGNED | MIXED | OPPOSING
best_zone: PRIMARY | SECONDARY | NONE
conviction: HIGH | MEDIUM-HIGH | MEDIUM | MEDIUM-LOW | LOW
baseline_dfii10: x.xx        # xauusd only
baseline_dgs2: x.xx          # FX only (US 2Y rate-momentum leg)
baseline_policy_diff: x.xx   # FX context only (not scored)
baseline_dxy: xxx.xxx
weekend_gap_pct: x.xxx
cot_net: ±xxxxx
cot_net_chg: ±xxxxx
etf_gld_tonnes: xxxx.xx       # xauusd only
etf_gld_wk_chg: ±xx.xx        # xauusd only
adx_val: xx.x
---
```

---

## Body Skeleton
```markdown
# XAUUSD Weekly Forecast — WNN (Mon YYYY-MM-DD)

## 1. Fundamental Analysis — <BIAS> / <CONFIDENCE>
| Driver | Value | Δ1W | Signal |
|---|---|---|---|
| DFII10 real yield | x.xx% | ±x.xx | ↑ bearish / ↓ bullish |
| DFII10 20d slope | x.xxx | trend |
| DGS10 nominal | x.xx% | ±x.xx | context |
| 5Y breakeven | x.xx% | ±x.xx | inflation read |
| Fed Funds | x.xx% | — | posture |
| DXY | xxx.x | ±x.x | ↑ bearish / ↓ bullish (20d slope x.xxx) |

**Read:** <2 sentences — yield direction + DXY posture + net gold implication>
**Risk to bias:** <one line — what flips this>

## 2. News Analysis
| Date/Time UTC | Event | Impact | Action |
|---|---|---|---|
| … | NFP/FOMC/CPI/Retail | high | 2h block / hard block |
<central-bank commentary + geopolitical drivers, 2–3 lines>

## 3. Technical Analysis — <D1 trend> / ADX <value> (<TRENDING|TRANSITIONAL|RANGING>)
| | Value | Note |
|---|---|---|
| Price | $xxxx | vs EMA20 $xxxx / EMA50 $xxxx / EMA200 $xxxx |
| RSI(14) D1 | xx.x | divergence? (note: RSI>70 NOT a short signal on gold) |
| D1 ATR(14) | $xx.xx | compressed? vs 20d median $xx.xx |
| H4 ATR(14) trading-only | $xx.xx | range>=$1 filter |

**Key resistance:** $xxxx–$xxxx (<confluence>), …
**Key support:** $xxxx–$xxxx (<confluence>), …
**Volume Profile (CME GC):** VAH $xxxx / POC $xxxx / VAL $xxxx — <one line>

## 4. Positioning & Flows
| | Value | Read |
|---|---|---|
| COT MM net | ±xxxxx (Δ ±xxxxx) | (crowded long is NOT a short signal — momentum) |
| GLD tonnes | xxxx.xx | 1w ±xx / 4w ±xx |
| Weekend gap | ±x.xxx% | noise / note / warning / re-forecast |
<One line: flows confirm or contradict bias?>

## 5. Top-Down Analysis (D→H4→1H)
| TF | Structure | Toward |
|---|---|---|
| D1 | HH+HL / LH+LL / ranging | bull/bear/none |
| H4 | … | … |
| H1 | … | … |
**Alignment:** ALIGNED / MIXED / OPPOSING — <one line>

## Trading Zone — PRIMARY [n.n/10] <CONVICTION>
> IF price reaches <zone> THEN buy/sell limit → target $xxxx (TPx)

| | |
|---|---|
| Direction | LONG / SHORT |
| Zone (box) | $xxxx – $xxxx |
| Zone Confluence | ✅ Z1 Structural / ✅ Z2 DFII10 slope / ✅ Z3 DXY slope / ✅ Z4 Top-down MTF / ❌ Z5 EMA / ✅ Z6 ATR / ❌ Z7 VP |
| Score | n.n / 10.0 |
| TP anchor | $xxxx @ <structural anchor> — indicative TP1 2.5R / TP2 3.0R |
| Invalidation | D1 close <above/below> $xxxx |

_SL, offset, limit, lots computed at /validate (not frozen here)._

## Trading Zone — SECONDARY [n.n/10] | NONE — <reason>
<same compact table or "NONE — [reason]">

## Trading Zone — COUNTER [n.n/10] | NONE — <reason>
<same table or "NONE — [macro HIGH / no RSI divergence / score <5.0]">
_If counter: Z2+Z3 score 0; RSI divergence MANDATORY; macro conf LOW/MEDIUM only._

## Bias Statement
<3 lines max. Bias + preferred zone + what switches to secondary + key threshold.>

## Contradiction / Conflict
<One line. Macro vs technical vs positioning conflict → `> [!warning]` callout + conviction downgrade to MEDIUM.>
```

---

## Rules
- Zone below 5.0/10 → NONE, never force. Counter needs RSI divergence + macro LOW/MEDIUM.
- Max 3 zones, ≤1 counter. Zones as boxes `$x–$y`, never single lines.
- Z1 Structural always mandatory. Never score RSI>70 / COT>200k as a short signal.
- TP names structural anchor; SL/offset/lots are a /validate concern.
- File immutable after Monday open.
