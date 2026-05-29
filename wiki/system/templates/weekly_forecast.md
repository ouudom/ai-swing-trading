---
type: system
updated: 2026-05-24
confidence: high
tags: [template, forecast, weekly]
related: [constitution, confluence_criteria]
---

# Weekly Forecast Template

> **Structured schema:** `schemas/weekly.py` (`WeeklyForecast`, `Setup`, `MacroDriver`).
> Markdown is a rendered view from the SQLite DB (`data/trading.db`).
> Use `render/weekly_md.py` to regenerate from DB, or `db/crud.py` to query programmatically.

File: `forecasts/weekly/YYYY-WNN.md` — immutable after Monday open.

---

## Frontmatter

```yaml
---
type: weekly_forecast
week: YYYY-WNN
generated: YYYY-MM-DD
macro_bias: BULLISH | BEARISH | NEUTRAL
macro_confidence: HIGH | MEDIUM-HIGH | MEDIUM | MEDIUM-LOW | LOW
mtf_alignment: ALIGNED | MIXED | OPPOSING
best_setup: A | B | NONE
conviction: HIGH | MEDIUM-HIGH | MEDIUM | MEDIUM-LOW | LOW
baseline_dfii10: x.xx
baseline_dxy: xxx.xxx
weekend_gap_pct: x.xxx
cot_mm_net: ±xxxxx
cot_mm_net_chg: ±xxxxx
etf_gld_tonnes: xxxx.xx
etf_gld_wk_chg: ±xx.xx
---
```

---

## Body Skeleton

```markdown
# XAUUSD Weekly Forecast — WNN (Mon YYYY-MM-DD)

## Macro — <BIAS> / <CONFIDENCE>

| Driver | Value | Δ1W | Signal |
|---|---|---|---|
| DFII10 real yield | x.xx% | ±x.xx | ↑ bearish / ↓ bullish |
| DGS10 nominal | x.xx% | ±x.xx | context |
| 5Y breakeven | x.xx% | ±x.xx | inflation read |
| Fed Funds | x.xx% | — | posture |
| DXY (FRED) | xxx.x | ±x.x | ↑ bearish / ↓ bullish |

**Read:** <2 sentences — yield direction + DXY posture + net gold implication>
**Risk to bias:** <one line — what flips this to opposite>

## Technical — <D1 trend> / ADX <value> (<TRENDING|TRANSITIONAL|RANGING>)

| | Value | Note |
|---|---|---|
| Price | $xxxx | vs EMA50 $xxxx / EMA200 $xxxx |
| RSI(14) D1 | xx.x | divergence? |
| H4 structure | HH+HL / LH+LL / ranging | last swing ref |
| H1 structure | same | |
| D1 ATR(14) | $xx.xx | compressed? vs 20d median $xx.xx |
| H4 ATR(14) trading-only | $xx.xx | range>=$1 filter (excl weekend/holiday) |
| 0.5 × D1_ATR14 | $xx.xx | volatility floor for stop |

**Key resistance:** $xxxx–$xxxx (<confluence>), $xxxx–$xxxx, $xxxx–$xxxx
**Key support:** $xxxx–$xxxx (<confluence>), $xxxx–$xxxx, $xxxx–$xxxx
**Volume Profile (CME GC):** VAH $xxxx / POC $xxxx / VAL $xxxx — <one line>

## Positioning

| | Value | Read |
|---|---|---|
| COT MM net | ±xxxxx (Δ ±xxxxx) | crowded / neutral |
| GLD tonnes | xxxx.xx | 1w: ±xx / 4w: ±xx |
| Weekend gap | ±x.xxx% | noise / note / warning / re-forecast |

<One line: flows confirm or contradict macro bias?>

## Pre-Screen Gates (run before scoring any setup)

| Gate | Status | Note |
|---|---|---|
| G1 H4+H1 structure aligned | ✅/❌ | direction |
| G3 DFII10 slope supports | ✅/❌ | slope value |
| G5 VIX regime | ✅/❌ | VIX xx.xx — calm/mixed/risk-off |
| G2 D1 ATR compressed | ✅/❌ | $xx.xx vs median $xx.xx |
_G6 (Asia range) is daily-only — not assessed at /weekly time._

## Setup A — <Label> [n.n/10] <CONVICTION>

> IF price reaches $xxxx.xx THEN buy/sell limit → target $xxxx.xx

| | |
|---|---|
| Direction | LONG / SHORT |
| Zone | $xxxx – $xxxx |
| Signals | ✅ S1 Structural / ✅ S6 Fundamental / ✅ S7 Vol Profile / ❌ S3 RSI div / ✅ S2 Fib / ❌ S4 EMA / ❌ S5 Pivot |
| Score | n.n / 10.0 |
| Stop calc | structural_dist $xx.xx, H4_ATR $xx.xx, 0.5×D1_ATR $xx.xx → stop_distance = avg() = $xx.xx |
| Offset | (10 − n.n) × 0.25 × $xx.xx = $xx.xx (OUTWARD) |
| Limit | $xxxx.xx (zone_top + offset for short / zone_bottom − offset for long) |
| Stop | $xxxx.xx (limit ± stop_distance) |
| TP | $xxxx.xx @ <structural anchor> (= x.xR) |
| Lots | $2000 / ($xx.xx × 100) = x.xx → **x.xx lots** |
| Invalidation | D1 close <above/below> $xxxx |

## Setup B — <Label> [n.n/10] | NONE — <reason>

<same compact table or "NONE — [reason]">

## Setup C — Counter [n.n/10] | NONE — <reason>

<same or "NONE — [macro HIGH / no RSI div / score <7.5]">
_If counter: S6 unavailable (macro works against). S3 mandatory. Cap 40% zone width._

## Bias Statement

<3 lines max. Bias + preferred setup + what switches to B + key threshold to watch.>

## No-Trade Events

| Date/Time UTC | Event | Action |
|---|---|---|
| Mon DD HH:MM | … | 2h block / hard block |

## Contradiction / Conflict

<One line. If macro vs technical conflict: add `> [!warning]` callout + note conviction downgrade.>
```

---

## Rules
- Setup below 5.5/10 → NONE, never force
- Counter below 7.5/10 or macro HIGH → NONE
- Lots always show formula then rounded-DOWN value
- TP names structural anchor + actual R-multiple
- Zones as ranges `$x–$y`, never single lines
- File immutable after Monday open
