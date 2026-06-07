---
type: research
updated: 2026-05-29
confidence: high
tags: [xauusd, phase0b, signals, edge, independent-testing]
related: [../phase0b_signal_plan.md, macro-regime.md, atr-compression.md, mtf-market-structure.md]
---

# XAUUSD — Independent Signal Results (Phase 0b)

Script: Phase 0b signal research runner (removed in repo cleanup)  
Data: TD 6.3yr 2020-2026 (D1/H4/H1), FRED macro, COT 2019-2026  
Forward windows: D1 fwd=5, H4 fwd=6 (24h), H1 fwd=4 (4h)  
Baseline: D1 54.0% | H4 53.9% | H1 52.1%

---

## HEADLINE FINDING: GOLD IS MOMENTUM, NOT MEAN-REVERTING

This is the single most important result. Gold is MOMENTUM: RSI>70 = momentum CONTINUES
(not a fade). Gold fades from oversold but not from overbought.
**All confluence signals must be pro-trend or macro-regime gated, NOT fade/mean-reversion.**

---

## D1 Results Summary (fwd=5d, baseline 54.0%)

### Confirmed Edges (keep / promote)

| Signal | Dir | Edge | t | N | Verdict |
|---|---|---|---|---|---|
| E1  DFII10 20d slope < 0 → long | LNG | +5.3pp | 2.95** | 776 | ✅ CONFIRMED — current macro gate, justified |
| C7  EMA20 > EMA50 regime → long | LNG | +4.7pp | 3.13** | 1097 | ✅ EMA regime filter works, promote |
| D5  Inside bar → long | LNG | +4.4pp | 2.52* | 831 | ✅ D1 pause before continuation |
| D4  NR7 → long | LNG | +7.4pp | 2.24* | 228 | ✅ Compression precedes up move |
| A2  RSI(14)<30 → long | LNG | +8.6pp | 2.03* | 139 | ✅ Oversold bounce (LONG ONLY, asymmetric) |
| B6  BB expanding → long | LNG | +4.5pp | 2.51* | 762 | ✅ Expansion favors up continuation |
| E8  DXY 20d slope < 0 → long | LNG | +5.3pp | 2.19* | 418 | ✅ Weak dollar = gold up |
| E9  DXY 20d slope > 0 → short | SHT | -12.8pp | -4.97** | 376 | ✅ Strong dollar = gold down (useful gate) |
| E13+E1 VIX>20 + DFII10 fall → long | LNG | +7.6pp | 2.65** | 302 | ✅ Combo: fear + easing rates = strong long |
| E2+A1 DFII10 rise + RSI>70 → short | SHT | -17.2pp | -3.36** | 95 | ✅ Combo: rising yields + OB = strong short |

### Strong Anti-Edges (REMOVE from system or flip)

| Signal | Dir Tested | Edge | t | Meaning |
|---|---|---|---|---|
| A1  RSI(14)>70 → short | SHT | −12.2pp | −4.44** | Gold TRENDS at OB — fade FAILS. OB = continue up. |
| B1  Close > BB upper → short | SHT | −13.0pp | −3.07** | Breakout above BB = momentum, not fade. |
| C11 Near 20d HIGH → short | SHT | −10.2pp | −4.03** | Structural resistance fails on gold. Price continues. |
| E4  DFII10 level > 2.0 → short | SHT | −18.2pp | −5.93** | *Regime contamination (2023-26 bull despite high yields).* Use slope, not level. |
| E5  DFII10 level 0-1 → long | LNG | −14.6pp | −3.05** | Rising-rate transition period = bearish. Don't use level. |
| E15 VIX < 15 → short | SHT | −12.8pp | −4.33** | Complacency ≠ gold bearish. Low VIX = risk-on but gold can rally. |
| D2  ATR expanding → long | LNG | −7.8pp | −1.39 | Volatility expansion is not directional. |
| F1  Spec net > 200k → short | SHT | −12.3pp | −7.63** | Crowded long ≠ reversal. Large spec = momentum phase. Don't fade COT extremes. |

### Weak / Insufficient Signals (cut weight to 0)

| Signal | Edge | t | Note |
|---|---|---|---|
| A8 Stoch K<20 → long | +3.9pp | +1.25 | Similar to RSI<30 but weaker |
| E3 DFII10 level < 0 → long | +3.1pp | +1.51 | Edge exists but level signal weaker than slope |
| E13 VIX > 20 → long | +1.4pp | +0.74 | Null — VIX alone not predictive |
| E14 VIX > 30 → long | +4.4pp | +1.08 | N=149, small, not significant |
| E16 VIX spike > +3 → long | −1.4pp | −0.24 | Null |
| C9  Donchian breakout UP → long | +6.7pp | +1.73 | Almost significant, N=163 |
| F2  Spec net < 75k → long | +16.0pp | +1.76 | N=30 only — intriguing but insufficient |

### Important Asymmetries

**RSI:** Long-only signal on gold. RSI<30 → +8.6pp. RSI>70 → SHORT fails (-12.2pp). Use RSI
ONLY as oversold long trigger, never as overbought short trigger.

**COT:** Extreme long NOT a contrarian short. Momentum asset: large spec = trending = follow.
COT works only when severely washed out (very low net = long signal). No contrarian short use.

**Structural levels:** 20d HIGH proximity → short FAILS (-10.2pp). Gold breaks resistance.
20d LOW proximity → long weak (+2.2pp). Use structure for zone location (where price reacts),
NOT as a standalone fade signal.

---

## H4 Results Summary (fwd=6 bars = 24h, baseline 53.9%)

H4 finding: **Almost all technical signals have near-zero edge on H4 except oscillator extremes.**
Gold's intraday moves are largely random except for oversold bounces.

| Signal | Dir | Edge | t | Verdict |
|---|---|---|---|---|
| A8  Stoch K<20 → long | LNG | +4.4pp | +3.57** | ✅ H4 oversold bounce works |
| A10 Williams %R < -80 → long | LNG | +4.4pp | +3.57** | ✅ Same signal as Stoch<20 |
| A2  RSI<30 → long | LNG | +2.7pp | +1.79 | Marginal on H4 |
| A1  RSI>70 → short | SHT | −9.0pp | −7.97** | ❌ H4 OB = momentum (same as D1) |
| C10 Donchian DN → short | SHT | −10.5pp | −4.21** | ❌ Breakdowns: price often recovers |
| All EMA signals | - | ~0pp | <0.5 | Null on H4 (too noisy) |
| All BB signals (long) | LNG | ~0pp | <0.5 | Null: BB on H4 no edge |
| Session: NY/London overlap (12-16) | LNG | +1.1pp | +0.90 | Weak, not significant |

**H4 session:** No session has meaningful DIRECTIONAL edge. Sessions differ by volatility
(documented in session-timing.md) but not direction. Don't use H4 session as directional gate.

---

## H1 Session Results (fwd=4 bars = 4h, baseline 52.1%)

H1 technical signals: nearly all null. The one finding:

| Hour UTC | Dir | Edge | t | Note |
|---|---|---|---|---|
| 18:00 | LNG | +3.5pp | 2.81** | 2PM EST — NY afternoon |
| 20:00 | LNG | +4.2pp | 3.29** | 4PM EST — post-COMEX |
| 21:00 | LNG | +4.1pp | 2.20* | 5PM EST — CME Globex transition |
| All 00-17 UTC | - | ~0pp | <2 | No directional edge |

**Interpretation:** H18-H21 UTC = post-regular-session drift. CME COMEX regular session 
closes 1:30 PM ET (17:30-18:30 UTC depending on DST). The post-close to Asian-open window
shows mild bullish drift. This is a structural feature of gold, not actionable for swing entries
(too small, too short).

**H1 summary:** No H1 technical signal worth adding to the system. Oscillators have tiny edge
(−3 to −5pp for overbought short, same momentum pattern as D1/H4). Use H1 only for TRIGGER
DETECTION (pin bar, engulfing, B&R), not as a scored gate.

---

## Implications for Current XAUUSD System

### Weekly Confluence Signal Reassessment

| Signal | Current Weight | Measured D1 Edge | New Assessment |
|---|---|---|---|
| S1 Structural Extreme | 2.5 (mandatory) | Near 20d low +2.2pp (weak) | Keep as ZONE LOCATOR (mandatory by role). Weight justified as anchor, not by standalone edge. |
| S2 Fundamental (DFII10 slope) | 2.5 | +5.3pp, t=2.95** | ✅ CONFIRMED. Justified. Consider 3.0. |
| S3 RSI Divergence | 1.5 | RSI level <30: +8.6pp. RSI >70: FAILS (momentum). | Keep DIVERGENCE (not level). Divergence ≠ level extreme. Weight 1.5 plausible. |
| S4 Volume Profile (VP) | 1.5 | Not testable (no intraday volume in TD) | Keep — VP is institutional-flow proxy. Cannot confirm/deny with free data. |
| S5 Fib levels | 0.75 | Not tested | Retain at 0.75 (convention, low weight) |
| S6 EMA trend filter | 0.75 | EMA20>EMA50: +4.7pp, t=3.13** | ✅ PROMOTED to 1.0. Edge is real. |

**DXY:** Measured +5.3pp long (slope<0), t=2.19*. Currently not a scored weekly signal —
only a re-forecast trigger (T2). Consider adding as context/gate alongside DFII10.

**VIX:** Null as standalone directional signal. VIX gate correctly demoted to 0-pt veto (D017).

**RSI overbought (gold breakout from 20d high):** Anti-edge. The system must NEVER use
RSI>70 as a short confluence signal for gold. Breakouts from 20d high (C11) also anti-edge.
This means: setup short zones at structural levels are valid, but RSI overbought at the
top of a range = continuation not reversal.

### Recommended Weight Adjustments (pending approval)

| Change | From | To | Rationale |
|---|---|---|---|
| S2 Fundamental | 2.5 | 3.0 | DFII10 slope = strongest measured signal |
| S6 EMA | 0.75 | 1.0 | EMA20>EMA50 confirmed +4.7pp |
| S3 RSI Divergence | 1.5 | 1.5 | Keep — divergence ≠ level, plausible at 1.5 |
| S1 Structural | 2.5 | 2.5 | Keep — zone anchor, mandatory by role |
| S4 VP | 1.5 | 1.5 | Keep — can't refute with free data |
| S5 Fib | 0.75 | 0.5 | Reduce — no evidence, lowest confidence |
| Total | 9.5 | 9.5 (max 10 if S5 also adds 0.5) | Rebalance within 10-pt max |

**New signal candidate — DXY slope:** Measured +5.3pp, t=2.19*. Add as S7 or fold into
S2 as "Macro Bundle (DFII10 slope + DXY slope, same direction)". Needs discussion.

### Entry / Filter Signals (not confluence, but entry quality)

- **D1 Inside bar before entry:** +4.4pp edge. If the D1 bar on entry day is an inside bar
  → compression before move → HIGHER quality entry. Add to daily validation as bonus note.
- **NR7 on D1:** +7.4pp edge (N=228). If current D1 is NR7 → strong compression signal.
  Worth noting in /validate output.
- **H4 Stoch/WR < -20/-80:** +4.4pp on H4. Confirms H4 oversold = long setup ripe.
  Already captured by the ATR-compression and structure gates. No scoring change needed.

---

## What NOT to Use

These had anti-edge and should NOT appear as positive signals in the system:

1. RSI > 70 as a SHORT signal for gold (momentum, not fade)
2. Price above Bollinger upper as a SHORT signal (breakout, not reversal)
3. Near 20d HIGH as a SHORT signal (resistance fails on gold)
4. Crowded COT long (spec net > 200k) as a SHORT signal (momentum phase)
5. VIX < 15 as a SHORT signal (no edge)
6. ATR expansion as a DIRECTIONAL signal either way (null)
7. DFII10 LEVEL as a gate (regime contamination; slope only)

---

## Open Questions

- [ ] RSI DIVERGENCE (higher price + lower RSI) tested independently? Not done here — we
      tested RSI level only. Divergence is structurally different. Could have edge where level does not.
- [ ] Volume Profile (CME 6E depth) — requires TradingView data, can't backtest free.
- [ ] Fibonacci levels — require dynamic swing detection, not tested.
- [ ] COT extreme LOW (spec net < 50k): N=30, intriguing +16pp. Get more history (pre-2019).
- [ ] DXY as scored confluence signal: measured edge, pending system decision.
- [ ] Seasonality: run with --long flag once yfinance fetch works.
