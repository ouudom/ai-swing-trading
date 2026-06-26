---
type: weekly_forecast
instrument: eurgbp
week: 2026-W26
generated: 2026-06-21
macro_bias: NEUTRAL
macro_confidence: LOW
mtf_alignment: MIXED
best_zone: PRIMARY
conviction: MEDIUM
baseline_rate_diff: -1.48
baseline_dxy: 100.814
weekend_gap_pct: N/A
cot_net: 0
cot_net_chg: 0
adx_val: 12.9
---

# EURGBP Weekly Forecast — W26 (Mon 2026-06-22)

## 0. Prior-Week Retrospective (W25)
_Last forecast: W25 — NEUTRAL range; PRIMARY LONG 0.8608–0.8625, SECONDARY SHORT 0.866–0.8682. Calibration: eurgbp mixed._
| Prior zone | Dir | Thesis | Outcome | Verdict |
|---|---|---|---|---|
| PRIMARY 0.8608–0.8625 | LONG | Range-floor dip-buy | PENDING/NO_TOUCH | UNTESTED — price stayed up, never dipped |
| SECONDARY 0.866–0.8682 | SHORT | Range-top fade | **LOSS_SL (−1.0R)** | **BROKE** — D1 CHoCH UP @0.86567 (06-18), range shifted up through the short |

**Carry-forward:** The W25 short broke when the range **shifted UP** (D1 CHoCH UP, BoE-hold + ECB-2.25% favoring EUR; political-transition upside risk to EURGBP per ING). The floor-long never filled. **Lesson:** re-anchor both zones to the new, higher range — short the new highs (0.8682+), buy the new floor (~0.8635), not the old 0.860 level.

## 1. Fundamental / Macro — NEUTRAL / LOW (cross, macro non-scoring)
| Driver | Value | Δ | Signal |
|---|---|---|---|
| ECB Deposit (ECBDFR) | 2.25% | hold | hawkish ECB cycle — EUR-supportive (context) |
| GBP SONIA | 3.73% | hold | BoE held 06-18, cautious — GBP soft |
| Rate diff (EUR−GBP) | −1.48% | +0.25 (20d) | WIDENING → mild EURGBP-bullish **tilt only (Z4, t<1.7)** |
| VIX | 18.44 | — | neutral (EG4: risk-off favors EURGBP UP — inverted, no veto) |

**Read:** Cross macro is dead/thin — bias set by structure, not rates. The non-scoring tilt (rate-diff widening + UK political risk) leans mildly EURGBP-UP, which is the headwind for the primary short. **Risk:** a TTM-squeeze upside break extends the new uptrend.

## 2. News / Calendar (no-trade windows, UTC)
| Date/Time | Event | Impact | Action |
|---|---|---|---|
| — | No high-impact EU/UK tier-1 release flagged in window | — | EU flash PMIs mid-week = context |

CB-calendar gate (06-21 +12d): **no ECB/BoE decisions in window** (ECB 07-23, BoE 07-30). FOMC caution-only for the cross (06-17 past). Clean calendar.

## 3. Technical — D1 CHoCH UP / ADX 12.9 (RANGING)
| | Value | Note |
|---|---|---|
| Price | 0.86724 | above EMA50 0.86591 / EMA200 0.86639 |
| RSI(14) D1 | 59.4 | rising — momentum up, not yet >65 |
| D1 ATR(14) | 0.00233 | **COMPRESSED** vs median 0.00283 → Z6 ✅; TTM squeeze ON (5 bars) = break pending |
| Oscillators | **D1 OVERBOUGHT** (W%R −3.9 / CCI 110.4 / above BB upper %B 1.1) · H4 W%R −19.8 OB | strong mean-reversion SHORT signal at range top |
| Market structure | D1 **CHoCH UP @0.86567** (06-18) · H4 MIXED (BOS↑ @0.86645) | range shifted up — bullish near-term tell |

**Key resistance (SHORT fade):** 0.86816 (05-29 high) · Donchian upper 0.8682 · weekly R3 0.86842 · Keltner-upper 0.86981 · round 0.8700 · May high 0.873.
**Key support (LONG fade):** VA low 0.86243 · Fib 61.8% 0.86424 · weekly PP 0.86345 · recent swing lows 0.86182.
**Time-at-price (H1):** HTN 0.86455 / VA 0.86243–0.86551 — acceptance core below spot.

## 4. Positioning & Flows
COT disabled (no CFTC cross contract). D1 above both EMAs after the CHoCH-up; the squeeze + bullish MACD warn the up-move may extend before reverting — the short's main risk.

## 5. Top-Down (D→H4→1H) — MIXED
| TF | Structure | Toward |
|---|---|---|
| D1 | CHoCH UP, overbought, squeeze ON | up (stretched) |
| H4 | MIXED, BOS↑ | up |
| H1 | bull engulf fired (06-19) | up |
**Alignment:** MIXED — near-term momentum is UP into an overbought extreme; the PRIMARY short fades that exhaustion, the SECONDARY long buys the floor on a pullback.

> [!warning] Contradiction / Conflict
> D1 OVERBOUGHT (fade-short signal) vs D1 CHoCH-UP + bullish MACD + TTM-squeeze-ON (breakout-up risk). Per protocol → PRIMARY short conviction capped **MEDIUM**; a squeeze break + D1 close > 0.8710 invalidates it.

## Trading Zones

### PRIMARY — SHORT 0.8682–0.8715 · Zone Confluence 8.0/10 · MEDIUM
> IF price pushes into 0.8682–0.8715 and prints a bearish 1H/H1 reversal THEN sell → target HTN 0.86455.
- Z1 Structural D1-extreme 3.0 ✅ (20d-high region / 05-29 high 0.86816 + Donchian upper 0.8682 + weekly R3 0.86842 + round 0.8700) · Z2 D1 oscillator OVERBOUGHT (CCI 110.4 / W%R −3.9 / above BB upper) 2.5 ✅ · Z3 H1 0 ❌ (recheck at validate) · Z4 macro tilt 0 ❌ (rate-diff favors UP) · Z5 ADX<25 (12.9) 1.0 ✅ · Z6 BB-touch + ATR-compressed 0.5 ✅ · Z7 Williams%R>−20 (−3.9) 1.0 ✅
- **TP anchor:** HTN 0.86455 / weekly PP 0.86345 (~3R off mid-zone, SL ~15 pips). **Invalidation:** D1 close **> 0.8710** (squeeze break up). Route through `fx_exposure.py` netting.

### SECONDARY — LONG 0.8625–0.8645 · Zone Confluence 5.0/10 · MEDIUM-LOW
> IF price pulls back into 0.8625–0.8645 (range floor / Fib) and prints a 1H pin THEN buy → target 0.8665.
- Z1 Structural D1-extreme 3.0 ✅ (VA low 0.86243 + Fib 61.8% 0.86424 + weekly PP 0.86345 + recent lows) · Z2 0 ❌ (not oversold now) · Z3 0 ❌ · Z4 rate-diff tilt LONG 0.5 ✅ · Z5 ADX<25 1.0 ✅ · Z6 ATR-compressed 0.5 ✅ · Z7 0 ❌
- **TP anchor:** EMA200 0.86639 / 0.8665 (~2R, SL ~15 pips). **Invalidation:** D1 close **< 0.8618**. Route through netting.

### COUNTER — NONE
Range cross with no trend to counter; both zones are range-edge fades.

## Bias Statement
NEUTRAL range cross with the range shifted UP (D1 CHoCH). Prefer PRIMARY SHORT fading the overbought new highs 0.8682–0.8715 (MEDIUM — squeeze-break risk); SECONDARY LONG buys a pullback to the 0.8635 floor. D1 close > 0.8710 flips to upside-breakout; < 0.8618 kills the long.

## No-Trade Calendar
No CB decisions in window. Watch the D1 TTM squeeze (5 bars on) — a release sets W26 direction.
