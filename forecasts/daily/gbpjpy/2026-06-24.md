---
type: daily_validation
instrument: gbpjpy
date: 2026-06-24
week: 2026-W26
generated: 2026-06-24T04:14Z
spot: 213.152
h4_atr: 0.458
d1_atr: 1.193
sl: 0.527
vix: 17.3
macro_sonia: 3.729
macro_slope20d: -0.001
adx_d1: 15.2
mof_regime: ACTIVE
mof_status: CAUTION
zones:
  - label: PRIMARY
    direction: LONG
    zone: [212.00, 212.90]
    verdict: NO_TRADE
    entry_confluence: 2.0
    hard_block: false
---

# GBPJPY Daily Validation — 2026-06-24

**Run:** 2026-06-24 03:19 UTC · Spot: 213.152 · H4_ATR: 0.458 · ADX: 15.2 (RANGING)

## Gates
- ✅ CB calendar: no BoJ/BoE decisions in window
- ✅ Econ: no high-impact GB/JP events in window (US PCE = caution only for cross)
- ⚠️ Intervention watch: MoF regime ACTIVE. Spot 213.152 in CAUTION band (210–214). Cap LONG conviction MEDIUM. Jawboning: Katayama 06-19 "decisive action." No HARD_BLOCK (< 214).

## PRIMARY — LONG 212.00–212.90 · ZC 6.0 · MEDIUM-LOW

**Q1:** V1 intact (D1 close 213.152 > invalidation 211.90). V1b: zone bottom 212.00, buffer 0.05, threshold 211.95; last 2 H4 closes 213.313 / 213.152 — well above. ✅

**Q2 (Bias flip?):** SONIA 3.729 (baseline context only — macro dead for gbpjpy). No macro flip gate. H4 CHoCH DOWN @ 213.209 (2 bars ago) = near-term bearish tilt — watch for further downside approach. ✅

**Q3:** No T3 (< 1.5% counter-move)/T4 triggers. ✅

**Q4 (Entry Confluence):**
- E0 reversal confirm: ❌ (no LONG confirm; H1 RSI 38, Stoch 49; zone not reached — spot 213.152 > zone top 212.90)
- E1 extreme still live (LONG: washout present): H4 Stoch 15.8 OVERSOLD, H4 W%R -80.4 OVERSOLD ✅ (2.5)... but zone NOT reached; price above zone
- EC approximation: ~2.0 (oscillators oversold but zone unreached)
- MoF CAUTION cap: even if zone reached, cap conviction MEDIUM

❌ **NO TRADE — zone unreached (spot 213.152 above zone top 212.90). Price needs to dip 26 pips to enter zone.**

**Watch:** H4 CHoCH DOWN at 213.209 suggests bearish pressure. If price dips below 212.90, zone activates — look for RSI-reclaim on H1 for E0. MoF CAUTION cap applies throughout.
