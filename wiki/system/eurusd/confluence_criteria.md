---
type: system
updated: 2026-05-28
confidence: medium-low
tags: [eurusd, confluence, scoring, gates, swing]
related: [macro_drivers.md, profile.md, constitution_addendum.md]
---

# EURUSD Confluence Criteria

> Same ARCHITECTURE as XAUUSD (`wiki/system/xauusd/confluence_criteria.md`): weekly forecast → daily
> validation → outward-offset limit entry. EUR differs only in signal definitions, weights, and
> pip-scaled thresholds. Universal rules (risk, stop formula, R, offset) live in [[constitution]]
> + [[constitution_addendum]]. All price thresholds in PIPS (1 pip = 0.0001).

## EUR is MEAN-REVERTING — confluence is counter-extreme (research-derived, not copied from gold)

Phase-2e (`scripts/research_eurusd_indicators.py`, 6.4yr) measured which indicators have forward
edge ON EUR. Result: EUR fades extremes; it does NOT trend or break out. So EUR setups are
**fades at structural range extremes**, and the signals/weights below reflect measured EUR edge —
deliberately different from gold's trend/macro 7-signal set.

Measured edge (forward 5d vs 48.9% baseline): RSI>70 short +6.6pp / RSI<30 long +4.4pp (strongest);
20d swing extreme +1.3–2.3pp; Bollinger 2σ +1.6pp; Donchian breakout NEGATIVE (−4.4pp → never a
continuation signal); EMA trend weak (~+1pp).

## Weekly Confluence (max 10.0) — minimum 5.5 to qualify as PENDING

Weights track MEASURED EUR edge (Phase-2e): RSI extreme is the strongest signal → top scored
weight. Structural extreme stays MANDATORY by ROLE (you need a level to fade) but is not the
highest weight. Fundamental is a **0-point veto** (null/regime-unstable → never awards points;
can only block — see S5).

| # | Signal | Weight | EUR definition (all mean-reversion / counter-extreme) |
|---|---|---|---|
| 1 | **Structural Extreme** [MANDATORY, role-anchor] | 2.5 | Price at prior weekly/daily swing H/L or 20d high/low or round number (1.10/1.15) — the level to FADE. Zones, not lines. Mandatory: no level = no fade. |
| 2 | **RSI Extreme / Divergence (Daily)** | 3.0 | RSI>70 (fade short) / <30 (fade long), OR divergence. Strongest measured EUR edge (+6.6/+4.4pp) → highest weight. |
| 3 | **Bollinger 2σ over-extension** | 2.0 | D1 close beyond 20,2 band in fade direction (+1.6pp, independent of RSI). |
| 4 | **Volume Profile (CME 6E)** | 2.0 | Weekly POC/VAH/VAL within ~10 pips of the extreme (real liquidity, independent confirm of exhaustion level). Tolerance = ½×median H4 ATR (calibrated E5). |
| 5 | **Fundamental context** [VETO, 0 pts] | 0.0 | Awards NO points. Acts ONLY as a veto: if US-EU rate diff + Fed/ECB + DXY are STRONGLY driving INTO the extreme (i.e. fundamentals actively pushing price further past the level you want to fade) → block the fade. Macro is null/regime-flipping as a standalone directional signal (macro_drivers) → it cannot ADD conviction, only remove it. |
| 6 | **Pivot / round number** | 0.5 | Weekly/monthly pivot or big figure within ~10 pips of extreme (calibrated E5). |

Total scored = 2.5 + 3.0 + 2.0 + 2.0 + 0 + 0.5 = **10.0**. S1 mandatory.
NO breakout / trend-continuation / EMA-trend signal — they have negative or no edge on EUR.
Setups are inherently counter-extreme; there is no separate "Setup C" (the whole EUR book is mean-reversion).

## Daily Validation (max 10.0) — min 6.0 to place order

Mean-reversion gates: confirm the fade at the extreme is RIPE (exhaustion), not a trend running.

Weights mirror the weekly set: RSI-extreme (strongest measured edge) is the top-weighted anchor;
structural-exhaustion is the confirm; fundamental is a 0-point veto.

| # | Condition | Weight | EUR pass-when |
|---|---|---|---|
| G1 | RSI extreme present (Daily/H4) | 3.0 | RSI>70 for shorts / <30 for longs (or fresh divergence) — strongest EUR edge → top weight |
| G2 | At structural extreme + H4/H1 exhaustion | 2.5 | Price in the weekly zone AND H4/H1 showing stall/reversal (NOT a clean trend continuing through it) — `scripts/structure.py` state ≠ strong continuation |
| G3 | Over-extension (Bollinger 2σ) | 2.0 | Price beyond 20,2 band in fade direction (independent confirm) |
| G4 | Fundamental not against the fade | VETO, 0 pts | Awards NO points. Hard veto: if rate-diff + DXY STRONGLY driving further INTO the extreme → NO TRADE. Macro null standalone → cannot add score, only block. |
| G5 | Risk/VIX regime OK | 1.5 | VIX regime table. VIX>35 → fades into a panic move blocked |
| G6 | London/pre-NY window + compression | 0.5 | entry in 07:00–13:00 UTC liquidity window AND that window's range < **35 pips** (calibrated p33 of 6.4yr; median is 41p) — compressed pre-move (EUR-active; replaces gold's Asia gate) |
| G7 | D1 ATR not expanding | 0.5 | D1 ATR14 ≤ 20d median (a blow-off expansion = don't fade yet) |

Total scored = 3.0 + 2.5 + 2.0 + 0 + 1.5 + 0.5 + 0.5 = **10.0**.
Floor logic: G1+G2 (5.5) = RSI-exhaustion + structure-extreme is the core; ≥6.0 needs one more confirm.
At least one of G1/G2 is effectively required (without both, max = 4.5 < 6.0). G4 is a pure veto (0 pts, can only block). Min 6.0 → ORDER LIMIT (if H1 trigger) / WATCH / else NO TRADE.

## H1 Trigger (entry confirmation)
Pin bar / engulfing / break-and-retest on H1 inside zone. Determines ORDER LIMIT vs WATCH only.

## Outward-Offset Limit (THE live edge — same as XAUUSD, pip-scaled)
```
entry_offset = (10 − weekly_confluence_score) × 0.25 × stop_distance   [price units]
Short: limit = zone_top    + entry_offset    (above zone, outward)
Long:  limit = zone_bottom − entry_offset    (below zone, outward)
```
Forces price to commit THROUGH the zone extreme before filling. This is the live-execution edge —
kept regardless of backtest (backtests understate its real-fill quality). See constitution_addendum.

## Stop + Sizing (pip-scaled, see constitution_addendum)
`stop_distance = avg(0.5×D1_ATR14, H4_ATR14_trading, structural_dist)`; H4 trading filter = bar range ≥ 5 pips.
`lots = floor($2000 / (stop_distance × 100000))`.

## Calibrated thresholds (E5, 2026-05-28 — `scripts/calibrate_eurusd.py`, 6.4yr)
- **G6 compressed cutoff = 35 pips** (07–13 UTC window; p33 of distribution, median 41p).
- **VP / pivot proximity = ~10 pips** (½ × median H4 ATR ≈ 13p, rounded down).
- H4 trading-day flatline filter = 5 pips confirmed (drops only 0.5% of bars = genuine flatline).
- Reference ATRs (measured): D1 ATR14 ≈ 69 pips, H4 ATR14 ≈ 27 pips.
- Still open: VP 6E liquidity quality vs gold's GC (verify 6E volume depth at /weekly).
