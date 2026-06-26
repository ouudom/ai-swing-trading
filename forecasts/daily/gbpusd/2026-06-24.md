---
type: daily_validation
instrument: gbpusd
date: 2026-06-24
week: 2026-W26
generated: 2026-06-24T04:14Z
spot: 1.31895
h4_atr: 0.00253
d1_atr: 0.00864
sl: 0.00342
vix: 17.3
macro_dgs2: 4.24
macro_slope20d: 0.11
dxy_jump: 0.448
adx_d1: 24.0
zones:
  - label: PRIMARY
    direction: SHORT
    zone: [1.3380, 1.3415]
    verdict: NO_TRADE
    entry_confluence: 1.0
    hard_block: false
  - label: COUNTER
    direction: LONG
    zone: [1.3140, 1.3200]
    verdict: NO_TRADE
    entry_confluence: 4.5
    hard_block: false
---

# GBPUSD Daily Validation — 2026-06-24

**Run:** 2026-06-24 03:16 UTC · Spot: 1.31895 · H4_ATR: 0.00253 · SL: 0.00342 · ADX: 24.0 (TRANSITIONAL → floor 6.5)

## Gates
- ✅ CB calendar: no decisions in window
- ⚠️ Econ: US Core PCE + GDP 2026-06-25 12:30 UTC (D028 forward-carry applies to any fills)
- ✅ DXY jump 0.448 < 0.5 — no hard block on COUNTER LONG
- ✅ VIX 17.3 / spike 0.5 — no LONG veto

## PRIMARY — SHORT 1.3380–1.3415 · ZC 5.0 · MEDIUM-LOW

**Q1–Q3:** V1/V1b intact. No re-forecast triggers. ✅

**Q4:** Zone unreached — spot 1.31895, zone bottom 1.3380 (148 pips above). No E0. EC ~1.0.

❌ **NO TRADE — zone unreached**

---

## COUNTER — LONG 1.3140–1.3200 · ZC 7.0 · MEDIUM

**Q1:** V1 intact (D1 close 1.31895 > invalidation 1.3161). V1b: last 2 H4 closes 1.31998 / 1.31895 both above threshold 1.3134. ✅

**Q2 (Bias flip?):** DGS2 4.24 (baseline 4.20, drift +0.04 < 0.15%). DXY jump 0.448 < 0.5 hard-block level. ✅

**Q3 (Re-forecast?):** No trigger. ✅

**Q4 (Entry Confluence):**
- E0 reversal confirm: ❌ (no bullish pin/engulf/RSI-reclaim on 1H; H1 RSI 38, Stoch 39 — neither below threshold)
- E1 D1 oscillator still extreme (long side): ✅ D1 RSI 33.5, Stoch 19.6, W%R -88.7, CCI -161.9 — deeply oversold (2.5)
- E2 H1 oscillator extreme today: ❌ H1 RSI 38 > 30, Stoch 39 > 20 (thresholds not met)
- E3 ADX<25: ✅ ADX 24.0 (1.0)
- E4 Structure/band intact: ✅ spot at D1 BB lower 1.31971, near 20d low (1.0)
- E5 Compression: ❌ ATR expanding (0.00864 > median 0.00754)
- **EC = 4.5/10**

> [!note] ADX 24.0 = TRANSITIONAL — EC floor raised to 6.5 for gbpusd. Score 4.5 < 6.5.

❌ **NO TRADE — EC 4.5 below transitional floor 6.5 (no E0, H1 not oversold yet)**

**Watch:** DXY jump approaching hard-block level (0.448 vs 0.5 trigger). D1 is deeply oversold — if H1 RSI dips below 30 and prints a bullish pin on approach/retest of zone, re-evaluate at next hourly run.
