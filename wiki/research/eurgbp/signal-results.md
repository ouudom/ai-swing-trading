---
type: system
updated: 2026-06-09
confidence: high
tags: [research, eurgbp, signals, backtest, mean-reversion, go-no-go]
related: [currency_exposure, decisions, signal-results]
---

# EURGBP Signal Edge Scan — EG3 Go/No-Go (D1, 2010→now)

**VERDICT: GO (D1).** EURGBP is strongly mean-reverting — same edge DNA as EURUSD/GBPUSD
(inverse of gold) — and the edge clears transaction cost comfortably despite the cross's low
volatility. Cleared to proceed with full onboarding (EG2 macro rebuild → EG4 profile/confluence →
EG5 wiring), gated on the Architecture B exposure ledger (EG0, built). See `decisions.md` D022.

## Run
`bash scripts/pyrun.sh scripts/backtest_signals.py --instrument eurgbp --since 2010-01-01 --tf D1`
Bars = 4287 (D1, 2010-01→2026-06). Baseline LNG 49.0% / SHT 50.7%, fwd window 5 D1 bars.
H4/H1 NOT yet scanned (backfill edge-loop bug stalled intraday pull — see Known Issues).

## Edge structure — mean-reversion confirmed (matches D021 FX family)
Fade oscillator / band / structure extremes. Trend-following is a measured ANTI-edge.

| Signal | Dir | N | win% | edge pp | t | |
|---|---|---|---|---|---|---|
| Near 20d LOW | LNG | 607 | 58.3 | +9.3 | 4.61 | ** |
| Close < Keltner low | LNG | 358 | 60.9 | +11.9 | 4.51 | ** |
| CCI < −100 | LNG | 483 | 58.8 | +9.8 | 4.32 | ** |
| Stoch K < 20 | LNG | 994 | 55.0 | +6.1 | 3.82 | ** |
| Williams %R < −80 | LNG | 1069 | 54.3 | +5.4 | 3.52 | ** |
| RSI < 30 | LNG | 99 | 65.7 | +16.7 | 3.32 | ** |
| RSI < 35 | LNG | 378 | 57.1 | +8.2 | 3.18 | ** |
| RSI2 < 10 (Connors) | LNG | 1228 | 52.9 | +3.9 | 2.72 | ** |
| CCI > +100 | SHT | 528 | 56.4 | +5.7 | 2.64 | ** |
| Close < BB lower / z<−2 | LNG | 194 | 57.7 | +8.8 | 2.44 | * |
| Williams %R > −20 | SHT | 798 | 54.6 | +3.9 | 2.22 | * |

**Anti-edges (trend-follow = lose):** Near-20d-LOW REV −9.2 (t=−4.53), Donchian20 breakdown −13.7
(t=−4.24), PSAR bull −2.9 (t=−2.61), ROC10>0 long −2.8, Close>EMA50 long −2.9, Supertrend/EMA
regime all negative. Identical polarity to EURUSD/GBPUSD — never trend-follow this cross.

**Long (oversold-fade) is the richer side** (more, stronger signals) — consistent with a
range-bound cross that snaps back from lows. Short-fade works but thinner (CCI>100, %R>−20, z>+2).

## Cost clearance — the real go/no-go for a low-vol cross
| Metric | Value |
|---|---|
| Spot | 0.86303 |
| D1 ATR14 now | 25.2 pips (compressed regime) |
| D1 ATR14 1y median | 35.8 pips |
| D1 ATR14 5y median | 41.1 pips |
| Best-signal avg drift (5d) | +0.15% to +0.20% = **13–17 pips** |
| Retail spread (typ) | 1.0–1.5 pip = **6–10% of a 0.18% edge** |
| Lots @ $2000 risk, ~18-pip SL | ~11 std lots |

Edge/cost ≈ 10× gross. Low absolute vol (≈ half a major's ATR) is offset by EURGBP's tight
spread — net clears. **Cost does NOT kill it.** (The classic low-range-cross trap is avoided here.)

## EG2 — Cross macro rebuilt (ECB−BoE) — result: THIN/DEAD on free daily data
Replaced the inherited US/DXY placeholder with a proper EUR-vs-GBP cross model
(`MACRO_MODE="cross_rate_diff"`, X-series in `backtest_signals.macro_signals`): EUR leg = ECBDFR,
GBP leg = SONIA (IUDSOIA), diff = ECBDFR − SONIA (rising → EURGBP up). DXY block gated OFF for the
cross (USD index, irrelevant). Re-ran D1 2010→now.

| Signal | Dir | N | edge pp | avg% | t | read |
|---|---|---|---|---|---|---|
| X3 EUR-GBP diff 5d widen>+0.05 | LNG | 101 | +7.5 | +0.32 | 1.50 | right sign, sub-significant |
| E16 VIX 1d spike>3 | LNG | 160 | +6.7 | +0.25 | 1.68 | risk-off → EURGBP UP |
| X7 GBP rate 5d jump | SHT | 100 | +5.3 | +0.13 | 1.06 | right sign, weak |
| X1/X2/X5/X6/X9/X10 (all 20d rate slopes) | — | ~2000 | −1 to −2 | ≈0 | ≈−1 | **NOISE / dead** |
| E13 VIX>20 / E15 VIX<15 | — | — | −0.5 | ≈0 | <0.5 | dead |

**Conclusion:** EURGBP has **no significant macro edge** on available free daily series. Slow
rate/policy slopes are dead (mirrors D021 carry-diff death on the majors). The only directional
hints — diff-widening (X3) and VIX-spike (E16) — are sub-t=2 and data-starved. Root cause is a
DATA LIMIT, not a model failure: no free daily EUR/GBP *market* yields (German/UK 2Y/10Y), so the
differential is one-sided (ECBDFR is a flat policy step; only SONIA moves).

### Consequences for confluence (EG4)
1. **EURGBP trades on PRICE/structure (mean-reversion) — macro is NOT a scored gate.** At most a
   LOW-weight tilt: X3 (diff widening → favor longs) + E16 (VIX-spike → favor longs) as minor
   confirmation only.
2. **🔑 VIX polarity is INVERTED vs the USD-majors.** Risk-off bids EUR over GBP → EURGBP UP
   (E16 long +6.7). The FX **VIX-veto-LONGS rule (USD-bid) MUST NOT transfer to EURGBP** — it would
   block the wrong side. EURGBP needs its own (or no) risk-off rule.
3. **EG2b (optional follow-on):** to get a real two-sided macro gate, wire daily German–UK
   sovereign yields (ECB SDW / paid source) for a Bund–Gilt 2Y/10Y spread. Only worth it if a
   macro gate is later wanted; the price edge stands alone without it.

## H4 + H1 validation (2020→now) — provisional rows CONFIRMED, both sides
Pulled after the backfill fix (H4 9784 bars, H1 39216 bars). Mean-reversion holds on intraday —
the Z3/E2 H1 rows (borrowed from GBP) are validated and *stronger* than assumed; the short side
(thin on D1) is significant on intraday.

**H1 (fwd=4, 39216 bars):** RSI2<10 long t=7.45 · Williams%R<−80 long t=7.42 · RSI<35 long t=6.58 ·
Stoch<20 long t=6.48 · RSI<30 long +7.7pp t=6.47 · Keltner-low long t=6.13 · **%R>−20 short t=5.06 ·
RSI>65 short t=3.42 · BB-upper short t=3.48** · CCI<−100 long t=4.20. Oscillators highly significant
**both directions** — Z3 (zone confluence) + E2 (entry) H1 confirm fully justified at weight 1.5.

**H4 (fwd=6, 9784 bars):** RSI<30 long +8.4 t=3.36 · Stoch>80 short t=3.54 · %R>−20 short t=3.18 ·
RSI>65 short t=2.88 · BB-lower long +5.8 t=2.52 · RSI>70 short t=2.12 · Keltner-high short t=2.03.
Both sides significant — EUR-family H4-centric character present on the cross too.

⇒ **Confluence flipped DRAFT → ACTIVE.** Short-side fades are tradeable (use intraday oscillator
extremes for the short trigger, since D1 short signals were thinner).

## Remaining before live (onboarding plan, see currency_exposure.md)
- **EG0** B exposure ledger — ✅ built (`scripts/fx_exposure.py`). EURGBP orders MUST route through
  it (EURGBP IS the cross factor — direct trade can stack on an implied cross).
- **EG1** config + data — ✅ D1 (4287 bars). ⏳ H4/H1 pull stalled (backfill bug) — needed for E0
  intraday entry confirmation + H4 ATR sizing.
- **EG2** macro rebuild (ECB−BoE) — TODO, blocking for the macro gate.
- **EG3** this go/no-go — ✅ GO on D1 price edge.
- **EG4** profile + confluence (low-vol ATR regimes, GBP-denominated pip econ, derived 6E/6B COT,
  cross-appropriate veto — VIX-LONG-veto is a USD-bid rule, doesn't transfer) — TODO.
- **EG5** `/weekly` + `/validate` Step-0 param row + forecast dirs — TODO.

## Known Issues
- `scripts/backfill_twelvedata.py` **edge-loop**: at the 2010 start boundary it re-requested the
  same `2010-01-01→2010-01-03` page 240+ times (+1 row each, never terminating), burning API calls
  and stalling before H4/H1. D1 data landed fine (4287 bars). Needs a terminate-on-no-progress guard.
