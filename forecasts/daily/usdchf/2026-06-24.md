---
type: daily_validation
instrument: usdchf
date: 2026-06-24
week: 2026-W26
generated: 2026-06-24T04:14Z
spot: 0.81088
h4_atr: 0.00143
d1_atr: 0.00542
sl: 0.00207
vix: 17.3
macro_dgs2: 4.24
macro_slope20d: 0.11
dxy_jump: 0.448
adx_d1: 30.8
zones:
  - label: PRIMARY
    direction: LONG
    zone: [0.7980, 0.8010]
    verdict: NO_TRADE
    entry_confluence: 1.5
    hard_block: false
  - label: COUNTER
    direction: SHORT
    zone: [0.8090, 0.8130]
    verdict: NO_TRADE
    entry_confluence: 1.0
    hard_block: true
---

# USDCHF Daily Validation — 2026-06-24

**Run:** 2026-06-24 03:18 UTC · Spot: 0.81088 · H4_ATR: 0.00143 · ADX: 30.8 (TRENDING)

## Gates
- ✅ CB calendar: no SNB decision in window (next quarterly Jun — confirmed already passed 2026-06-19 ← verify: SNB was Mar/Jun/Sep/Dec; Jun decision was 06-19 per prior session data)
- ⚠️ Econ: US Core PCE + GDP 2026-06-25 12:30 UTC (D028 forward-carry if any fill)
- No VIX veto/score for usdchf (washout)

## PRIMARY — LONG 0.7980–0.8010 · ZC 5.0 · MEDIUM

**Q1–Q3:** V1 intact (D1 close 0.81088 > zone top 0.8010; note: zone never dipped — price rallied away). V1b: no H4 closes below 0.7976. ✅ No re-forecast triggers. ✅

**Q4:** Zone unreached — spot 0.81088, zone top 0.8010 (99 pips above the zone). Price rallied through and away from the buy-the-dip zone. No E0. EC ~1.5.

❌ **NO TRADE — zone unreached (price 99 pips above zone top)**

---

## COUNTER — SHORT 0.8090–0.8130 · ZC 5.0 · MEDIUM-LOW

**Q1:** V1 intact (D1 close 0.81088 < zone top 0.8130). V1b: threshold = 0.8130 + 0.0004 = 0.8134; last 2 H4 closes 0.80972 / 0.81088 both below 0.8134. ✅

**Q2 (Bias flip?):** DXY 20d slope rising → bullish USDCHF. DXY slope flip AGAINST short zone → re-check bias. Slope was always rising; macro is against the short. No new flip but macro misaligned throughout. ✅ (no new trigger; zone was already flagged MEDIUM-LOW / DXY against)

**Q3:** No re-forecast. ✅

**Q4 (Entry Confluence):**
- ADX 30.8 > 30, D1 trend UP (BOS UP @ 0.80152) → HARD VETO: trending against SHORT fade

> [!warning] HARD BLOCK — D1 ADX 30.8 > 30, trend direction UP (BOS UP 0.80152 confirmed). Short fade is against a trending bull move. Hard veto clears any prior lock.

❌ **NO TRADE — HARD BLOCK (ADX 30.8 trending UP against SHORT fade)**

Full EC moot: E0 ❌, E1 ❌ (H1 RSI 60 < 65; Stoch 81 but W%R/RSI primary gates unmet), E2 ❌ (DXY slope against), E3 ❌ (no squeeze), E4 ❌ (ADX 30.8 > 25) → EC ~1.0/10 independent of veto.
