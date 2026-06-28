---
type: daily_validation
instrument: eurgbp
date: 2026-06-26
week: 2026-W26
generated_utc: "2026-06-26T10:23:00Z"
zones:
  - id: eurgbp-2026-W26-PRIMARY
    direction: SHORT
    verdict: NO_TRADE
    entry_confluence: 3.0
---

# EURGBP Daily Validation — 2026-06-26

**Spot:** 0.86298 | H4_ATR: 0.00116 | D1_ATR: 0.00264 | D1 ADX: 23.4 (TRANSITIONAL → floor 6.5)

**Gates:** ✅ CB clear (ECB/BoE no decision today) | ✅ Econ clear | ✅ T4-X FALSE

## Zone 1 — PRIMARY SHORT 0.8682–0.8715 (ZC 8.0)

Spot 0.86298 is **52 pips BELOW zone bottom** (0.8682). Zone not approached.

**Q1/Q2 blocks:** V1/V1b ✅ intact. V3 ✅ clear.

**Q4 EC (floor 6.5 for TRANSITIONAL ADX):**

E0 ❌ (no SHORT confirm; LONG-confirm none) | E1 ❌ (D1 Stoch 19.7 OVERSOLD = OPPOSITE of SHORT overbought requirement) | E2 ❌ (H1 RSI 66 overbought but at current price not at 0.8682 zone) | E3 ✅ 1.0 (ADX 23.4 < 25) | E4 ✅ 1.0 (zone intact) | E5 ✅ 1.0 (TTM squeeze ON 4 bars D1, 5 bars H4 — compression holding)

**EC: 3.0/10 < 5.0 (and << 6.5 TRANSITIONAL floor) → ❌ NO TRADE**

D1 is OVERSOLD — the opposite regime of a SHORT fade zone. Zone at 0.8682 remains far with no upward momentum.

| Zone | Verdict | EC |
|------|---------|----|
| PRIMARY SHORT 0.8682–0.8715 | ❌ NO TRADE | 3.0 |

(SECONDARY LONG previously INVALIDATED.)

## 15:09 UTC Re-run (automated hourly)

Spot 0.86345. Zone PRIMARY SHORT 0.8682–0.8715 — 33.5 pips below zone bottom. Zone not reached.
D1 OVERSOLD (Stoch 19.7, W%R −81.4, squeeze ON 4b) — opposite of SHORT requirement. H4 mid.
No E0 SHORT-confirm. EC 3.0/10 (unchanged). **PRIMARY SHORT ❌ NO TRADE unchanged.** Ledger: ACCEPT.

## 16:09 UTC Re-run (automated hourly)

Spot 0.86238 | H4_ATR 0.00127 | D1_ATR 0.00264 | D1_ADX 16.9 (ranging) | DXY N/A (cross)

**PRIMARY SHORT 0.8682–0.8715:** ❌ NO TRADE — zone unreached (spot 0.86238, 44 pips below zone bottom 0.8682). D1 oscillators now OVERSOLD (Stoch 19.7, W%R −81.4) — opposite of the OVERBOUGHT needed for E1. D1 TTM squeeze ON (4 bars). No E0 short-confirm. EC ≈ 2.0/10 (E5 ADX<25 ✅ 1.0 · E6 ATR-compressed 0.5 · E7 0 · rest ❌). SECONDARY LONG previously INVALIDATED.

V1/V1b: all clear. No macro flip gate for EURGBP (cross — rate-diff context only). No re-forecast.

Note: D1 has rotated from OVERBOUGHT (at weekly forecast) to OVERSOLD — price pulled back ~80 pips from the zone. PRIMARY SHORT zone would require a recovery bounce back to 0.8682+; even then E1 (D1 overbought) would need to reset. Zone quality degraded; will expire at week end.
