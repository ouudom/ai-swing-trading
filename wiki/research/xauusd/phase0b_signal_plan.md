---
type: research
updated: 2026-05-29
confidence: high
tags: [xauusd, research, signals, phase0b, independent-testing]
related: [_INDEX.md, concepts/macro-regime.md, concepts/atr-compression.md]
---

# XAUUSD Phase 0b — Independent Signal Research Plan

## Why This Exists

XAUUSD confluence signals (early version) were weighted by theory and literature, NOT by
measured forward-return edge.

This plan corrects that. Every signal is tested IN ISOLATION vs the 54% baseline. No combined
scoring. Signals that fail get cut or demoted. Signals that pass (with sufficient N) get
weight proportional to measured edge.

**Script:** Phase 0b signal research runner (removed in repo cleanup)

---

## Data Inventory

| Source | TF | Range | Rows | Path |
|---|---|---|---|---|
| Twelve Data (UTC) | D1 | 2020-01-24 → now | ~1,645 | `data/twelvedata/xauusd/1day.csv` |
| Twelve Data (UTC) | H4 | 2020-01-24 → now | ~9,748 | `data/twelvedata/xauusd/4h.csv` |
| Twelve Data (UTC) | H1 | 2020-01-24 → now | ~37,600 | `data/twelvedata/xauusd/1h.csv` |
| yfinance GC=F | D1 | 2004→now (~22yr) | ~5,500 | `data/yahoo/XAUUSD_long.csv` (auto-fetched) |
| FRED DFII10 | daily | 2003→now | ~5,850 | `data/fred/DFII10.csv` |
| FRED T5YIE | daily | 2003→now | ~5,850 | `data/fred/T5YIE.csv` |
| FRED VIXCLS | daily | 1990→now | ~9,190 | `data/fred/VIXCLS.csv` |
| FRED DFF | daily | 1954→now | ~26,200 | `data/fred/DFF.csv` |
| FRED DCOILWTICO | daily | 1986→now | ~10,160 | `data/fred/DCOILWTICO.csv` |
| ICE DXY | daily | ~2005→now | ~5,000 | `data/yahoo/DXY.csv` |
| CFTC COT (gold) | weekly | 2019→now | ~350wk | `data/cftc/deahistfo{year}.zip` |

**Note:** D1 macro tests use TD 6.3yr (2020–2026). Seasonality tests use 22yr yfinance
to get sufficient N for monthly/day-of-week signals.

---

## Methodology

```
For each signal:
  1. Compute condition: True/False for every bar
  2. For True bars: forward close return at horizon H
  3. Compute win% in expected direction (up for long signal, down for short)
  4. edge = win% − baseline%
  5. t_stat = (win% − baseline) / sqrt(baseline*(1−baseline)/N)
  6. Report: N | win% | edge (pp) | avg_ret% | t_stat
```

**Forward windows (primary):**
- D1: `fwd=5` (1 trading week — matches weekly bias horizon)
- H4: `fwd=6` (24h — one trading day)
- H1: `fwd=4` (4h — one session)

**Statistical threshold:**
- |t| > 2.0 → possible edge (p < 0.05), tentative
- |t| > 2.6 → credible edge (p < 0.01), act on it
- N < 25 → report but mark INSUFFICIENT
- N < 50 → treat as weak even if t > 2

**Baseline:**
- D1: 54.0% up (gold 2020–2026 secular drift; 22yr ~54%)
- H4/H1: computed from sample (non-trading bars filtered)

**Key discipline:** test LONG and SHORT direction for every signal. A signal showing edge
long but anti-edge short has asymmetric use (long-only filter). Both must be measured.

---

## Signal Catalogue

### Category A — Oscillator Extremes (Mean-Reversion)

These measure overbought/oversold. Theory: gold mean-reverts at extremes.

| # | Signal | Direction | Hypothesis |
|---|---|---|---|
| A1 | RSI(14) > 70 | SHORT | Overbought fade |
| A2 | RSI(14) < 30 | LONG | Oversold bounce |
| A3 | RSI(14) > 65 (softer) | SHORT | Earlier OB |
| A4 | RSI(14) < 35 (softer) | LONG | Earlier OS |
| A5 | RSI(14) cross below 70 (fresh exit OB) | SHORT | Confirmed OB reversal |
| A6 | RSI(14) cross above 30 (fresh exit OS) | LONG | Confirmed OS reversal |
| A7 | Stochastic(14,3) K > 80 | SHORT | Stoch overbought |
| A8 | Stochastic(14,3) K < 20 | LONG | Stoch oversold |
| A9 | Williams %R > −20 | SHORT | WR overbought |
| A10 | Williams %R < −80 | LONG | WR oversold |
| A11 | CCI(20) > +100 | SHORT | CCI overbought |
| A12 | CCI(20) < −100 | LONG | CCI oversold |

### Category B — Bollinger / Volatility Bands

| # | Signal | Direction | Hypothesis |
|---|---|---|---|
| B1 | Close > BB(20,2) upper | SHORT | Over-extension fade |
| B2 | Close < BB(20,2) lower | LONG | Under-extension bounce |
| B3 | Close > BB(20,1.5) upper (softer) | SHORT | Earlier signal |
| B4 | Close < BB(20,1.5) lower (softer) | LONG | Earlier signal |
| B5 | BB width at 20-bar low (squeeze) | NEUTRAL | Expansion imminent |
| B6 | BB width expanding (> 20-bar median) | NEUTRAL | Trend continuation |

### Category C — Trend / Structure / Momentum

| # | Signal | Direction | Hypothesis |
|---|---|---|---|
| C1 | Close > EMA(20) | LONG | Short-term bullish |
| C2 | Close < EMA(20) | SHORT | Short-term bearish |
| C3 | Close > EMA(50) | LONG | Medium-term bullish |
| C4 | Close < EMA(50) | SHORT | Medium-term bearish |
| C5 | Close > EMA(200) | LONG | Long-term uptrend |
| C6 | Close < EMA(200) | SHORT | Long-term downtrend |
| C7 | EMA(20) > EMA(50) | LONG | Golden-cross regime |
| C8 | EMA(20) < EMA(50) | SHORT | Death-cross regime |
| C9 | Donchian(20) breakout UP (close > 20d high) | LONG | Breakout momentum |
| C10 | Donchian(20) breakdown (close < 20d low) | SHORT | Breakdown momentum |
| C11 | At 20d swing HIGH (within 0.3%) | SHORT | Structural resistance |
| C12 | At 20d swing LOW (within 0.3%) | LONG | Structural support |
| C13 | MACD line crosses above signal | LONG | Momentum turn |
| C14 | MACD line crosses below signal | SHORT | Momentum turn |
| C15 | ADX(14) < 20 | NEUTRAL | Ranging — fade extremes |
| C16 | ADX(14) 20–25 (transitional) | NEUTRAL | Regime gate |
| C17 | ADX(14) > 25 | NEUTRAL | Trending — follow trend |

### Category D — Volatility Regime

| # | Signal | Direction | Hypothesis |
|---|---|---|---|
| D1 | D1 ATR(14) < 20-bar median | NEUTRAL | Compressed → expansion |
| D2 | D1 ATR(14) > 1.5× 20-bar median | NEUTRAL | Expanding → fade or chase? |
| D3 | D1 ATR(14) < 20-bar median + RSI>70 | SHORT | Compressed + OB = strong fade |
| D4 | NR7 (narrowest range in 7 bars) | NEUTRAL | Compression signal |
| D5 | Inside bar (range < prior bar) | NEUTRAL | Pause / indecision |

### Category E — Macro (D1 only, FRED data)

| # | Signal | Direction | Hypothesis |
|---|---|---|---|
| E1 | DFII10 20d slope < 0 | LONG | Real yields falling → gold bullish |
| E2 | DFII10 20d slope > 0 | SHORT | Real yields rising → gold bearish |
| E3 | DFII10 level < 0 | LONG | Negative real rates → hold gold |
| E4 | DFII10 level > 2.0 | SHORT | High real rates → headwind |
| E5 | DFII10 level 0–1 | NEUTRAL | Moderate real rates |
| E6 | DFII10 5d jump > +0.15 | SHORT | Hawkish shock |
| E7 | DFII10 5d drop > 0.15 | LONG | Dovish shock |
| E8 | DXY(ICE) 20d slope < 0 | LONG | Weak dollar → gold up |
| E9 | DXY(ICE) 20d slope > 0 | SHORT | Strong dollar → gold down |
| E10 | DXY 1d jump > 0.75 pts | SHORT | Dollar spike |
| E11 | T5YIE 20d slope > 0 | LONG | Inflation expectations rising |
| E12 | T5YIE 20d slope < 0 | SHORT | Inflation expectations falling |
| E13 | VIX level > 20 | LONG | Elevated fear → safe-haven |
| E14 | VIX level > 30 | LONG | Panic — gold flight? |
| E15 | VIX level < 15 | SHORT | Complacency → risk-on, gold weak? |
| E16 | VIX 1d spike > 3 pts | LONG | Fear spike → safe-haven |
| E17 | DFF > 4% (high rate regime) | SHORT | Rate headwind |
| E18 | DFF < 1% (ZIRP regime) | LONG | Rate tailwind |
| E19 | Oil(WTI) 20d slope > 0 | LONG | Inflation signal |
| E20 | Oil(WTI) 20d slope < 0 | SHORT | Deflation signal |

### Category F — COT Positioning (D1, weekly signal forward-filled)

| # | Signal | Direction | Hypothesis |
|---|---|---|---|
| F1 | Spec net > 200k contracts | SHORT | Crowded long → fade |
| F2 | Spec net < 75k contracts | LONG | Washed out → buy |
| F3 | Spec net at 80th percentile of 3yr | SHORT | Relative extreme long |
| F4 | Spec net at 20th percentile of 3yr | LONG | Relative extreme short |
| F5 | W/W change < −15k (selling) | SHORT | Spec exiting longs |
| F6 | W/W change > +15k (buying) | LONG | Spec building longs |
| F7 | Commercial net > 80th pctile (hedging) | SHORT | Smart money hedging heavily |

### Category G — Seasonality (22yr yfinance for N)

| # | Signal | Direction | Hypothesis |
|---|---|---|---|
| G1 | Monday | LONG/SHORT | Monday effect |
| G2 | Tuesday | LONG/SHORT | Day bias |
| G3 | Wednesday | LONG/SHORT | Mid-week |
| G4 | Thursday | LONG/SHORT | Pre-Friday |
| G5 | Friday | LONG/SHORT | Weekend positioning |
| G6 | January | LONG | Seasonal demand |
| G7 | September | SHORT | Historically weakest month |
| G8 | November/December | LONG | Year-end + Indian wedding season |
| G9 | Turn of month (last 3 days) | LONG | Month-end rebalancing |
| G10 | Turn of month (first 3 days) | LONG | Month-start flows |
| G11 | Q1 (Jan–Mar) | LONG | Historically strong |
| G12 | Q3 (Jul–Sep) | SHORT | Historically weak |

### Category H — Session (H4/H1 only)

| # | Signal | Direction | Hypothesis |
|---|---|---|---|
| H1 | Asia session bar (22:00–06:00 UTC) | NEUTRAL | Low vol, but drift? |
| H2 | London open (07:00–09:00 UTC) | LONG | Directional burst |
| H3 | NY open (13:00–15:00 UTC) | LONG | Volatility spike |
| H4 | NY/London overlap (12:00–16:00 UTC) | LONG | Peak liquidity |
| H5 | London close (16:00–17:00 UTC) | SHORT | Fade the day's move? |
| H6 | Asia compression → London breakout dir | LONG/SHORT | Compressed Asia → directional London |

---

## Combination Signals (Phase 0c — after individual results)

Only test combinations that both passed individually. Combinations tested second, not first.

Candidates (pending A/B results):
- Macro gate (E1/E2) + RSI extreme (A1/A2) — both pass → combined stronger?
- ATR compressed (D1) + oscillator extreme (A1/A2)
- Structural extreme (C11/C12) + RSI extreme (A1/A2)
- VIX regime (E13/E14) + DFII10 slope (E1/E2)

---

## Output Format (from script)

```
XAUUSD Signal Edge Scan — D1 fwd=5 — baseline=54.0%
Signal                       Dir  N     win%   edge    avg%     t
─────────────────────────────────────────────────────────────────
[A1] RSI>70 → short          SHT  142   58.5   +8.5   -0.42%   2.02 *
[A2] RSI<30 → long           LNG   67   62.7   +8.7   +0.51%   1.70
[E1] DFII10 slope<0 → long   LNG  531   57.2   +3.2   +0.18%   2.41 *
...
* = t>2.0   ** = t>2.6   (N<30 = INSUFF)
```

---

## Action Thresholds

| Result | Action |
|---|---|
| edge > +5pp AND t > 2.0 AND N > 50 | **Keep / promote weight** |
| edge +2–5pp AND t > 2.0 | Keep at current weight, monitor |
| edge < +2pp OR t < 1.5 | **Cut or demote to 0-pt filter** |
| edge negative (anti-predictive) | **Remove from system entirely** |
| Seasonality: edge > +5pp AND N > 40/year | Add as weekly context note |

---

## After This Research

1. Re-derive XAUUSD weekly confluence weights from measured edge
2. Compare to current weights (S1–S6): which were justified, which weren't
3. Write results to `concepts/` files (one per category)
4. Update `wiki/system/xauusd/confluence_criteria.md` weights if evidence supports change
5. Log in `wiki/system/core/decisions.md` (D018 or next available)
