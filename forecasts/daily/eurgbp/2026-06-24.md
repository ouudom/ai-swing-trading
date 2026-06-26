---
type: daily_validation
instrument: eurgbp
date: 2026-06-24
week: 2026-W26
generated: 2026-06-24T04:14Z
spot: 0.86129
h4_atr: 0.00134
d1_atr: 0.00262
sl: 0.00134
vix: 17.3
macro_rate_diff: -1.479
macro_slope20d: 0.251
adx_d1: 14.1
zones:
  - label: PRIMARY
    direction: SHORT
    zone: [0.8682, 0.8715]
    verdict: NO_TRADE
    entry_confluence: 1.0
    hard_block: false
  - label: SECONDARY
    direction: LONG
    zone: [0.8625, 0.8645]
    verdict: INVALIDATED
    entry_confluence: null
    hard_block: true
    invalidation: V1b
---

# EURGBP Daily Validation — 2026-06-24

**Run:** 2026-06-24 04:14 UTC · Spot: 0.86129 · H4_ATR: 0.00134 · ADX: 14.1 (RANGING)

## Gates
- ✅ CB calendar: no ECB/BoE decisions in window
- ✅ Econ: no high-impact EU/GB events in window (US PCE not a hard block for cross)
- No VIX veto for eurgbp (cross — inverted)

## PRIMARY — SHORT 0.8682–0.8715 · ZC 8.0 · MEDIUM

**Q1–Q3:** V1 intact (D1 close 0.86147 well below zone bottom 0.8682). V1b: H4 closes 0.86307/0.86215/0.86147 — none near zone top. ✅ No re-forecast triggers. ✅

**Q4:** Zone unreached — spot 0.86147, zone bottom 0.8682 (53 pips above). No E0. EC ~1.0.

❌ **NO TRADE — zone unreached**

---

## SECONDARY — LONG 0.8625–0.8645 · ZC 5.0 · MEDIUM-LOW

**Q1 — V1b INVALIDATED (04:14 UTC run)**

V1b threshold = 0.8625 − 0.0004 = 0.8621. Confirmed 2 consecutive H4 closes below threshold:
- 00:00 UTC close: 0.86124 (< 0.8621 — 1st breach, confirmed on final close)
- 04:00 UTC close: 0.86129 (< 0.8621 — 2nd breach)

> [!caution] V1b INVALIDATED — two consecutive H4 closes below 0.8621 threshold (0.86124 / 0.86129). Zone cancelled. ~~03:17 UTC run had 1/2 breaches (00:00 bar was still open, reading 0.86147); 00:00 bar final close confirmed at 0.86124 + new 04:00 bar sealed second breach.~~

❌ **INVALIDATED — V1b breach confirmed (2 consecutive H4 closes below 0.8621)**
