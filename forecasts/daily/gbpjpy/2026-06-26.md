---
type: daily_validation
instrument: gbpjpy
date: 2026-06-26
week: 2026-W26
generated_utc: "2026-06-26T10:23:00Z"
zones:
  - id: gbpjpy-2026-W26-PRIMARY
    direction: LONG
    verdict: NO_TRADE
    entry_confluence: 2.0
---

# GBPJPY Daily Validation — 2026-06-26

**Spot:** 213.565 | H4_ATR: 0.415 | D1_ATR: 1.129 | D1 ADX: 15.5 (RANGING)

**Gates:** ✅ CB clear (BoJ/BoE no decision) | ✅ Econ clear | ✅ T4-X FALSE

**MoF intervention watch:** Spot 213.565 in caution band 210–214. ⚠ CAUTION — LONG conviction capped MEDIUM. Jawboning active (Katayama 06-19). Not hard-block (spot < 214).

## Zone 1 — PRIMARY LONG 212.0–212.9 (ZC 6.0)

Spot 213.565 is **66 pips ABOVE zone top** (212.9). Zone not approached from above.

**Q1/Q2 blocks:** V1 ✅ (no D1 close below 211.9 invalidation) | V1b ✅ (H4 closes 213.451/213.565 >> 211.95 threshold) | V3 ✅ | MoF CAUTION (not hard-block at 213.565).

**Q4 EC:**

E0 ❌ (RSI-reclaim primary for GBPJPY LONG: H1 RSI 62 not a reclaim from below 35. Pin fired but de-prioritized D027 + price above zone) | E1 ❌ (LONG needs washout: D1 Stoch 23.7 mid, W%R −71.1 mid, H4 Stoch 70.1 mid-overbought — no washout) | E2 ❌ (session 12–16 UTC = 1.5; currently 10:10 UTC, outside window) | E3 ❌ (no H1 inside-bar break at zone, price above zone) | E4 ✅ 1.0 (zone intact) | E5 ✅ 1.0 (ADX 15.5 < 25 — ranging)

**EC: 2.0/10 < 5.0 → ❌ NO TRADE**

Price above zone, no washout oscillators, outside session window. MoF caution adds further risk to LONG.

| Zone | Verdict | EC |
|------|---------|----|
| PRIMARY LONG 212.0–212.9 | ❌ NO TRADE | 2.0 |

Note: Replay shows GBPJPY PRIMARY LONG RUNNING +1.55R (filled 06-24 via prior fill in replay). Zone still OPEN in ledger; live re-check finds EC below floor today.

## 15:09 UTC Re-run (automated hourly)

Spot 213.454 (above zone 212.00–212.90). H4_ATR: 0.422 D1_ATR: 1.129. D1 ADX 15.3 (calm).
H4 Stoch 70.0, W%R −30.0 (mid — no washout). No E0. MoF CAUTION (spot in band, cap MEDIUM).
EC 3.5/10 (E2 1.5 session + E4 1.0 + E5 1.0 — unchanged). **PRIMARY LONG ❌ NO TRADE unchanged.** Ledger: ACCEPT.

## 16:09 UTC Re-run (automated hourly)

Spot 213.693 | H4_ATR 0.42 | D1_ATR 1.129 | D1_ADX 15.3 (ranging) | MoF CAUTION active (jawboning 06-19)

**PRIMARY LONG 212.00–212.90:** ❌ NO TRADE — zone not reached; spot 213.693 is 80 pips ABOVE zone top (212.90). Price has moved up and away from the zone all week. Bull engulf fired at H1 (15:00 bar RSI 61, Stoch 79) but at 213.69 — irrelevant (not in zone). H4 BOS UP @ 213.751 (12:00 bar, 0 bars ago) = H4 structure has broken UP, confirming zone was bypassed.

EC ≈ 2.0/10 (E2 extreme engine — price now above zone, not at Keltner-low; E6 big-fig 212.00 remains valid; rest ❌). V1/V1b: intact (H4 closes at 213.7+, well above zone). MoF CAUTION remains (cap MEDIUM on any LONG — moot as zone not reached).

COUNTER SHORT 215.6–216.4: Not armed (spot 213.693 has not approached that zone either). H4 overbought (Stoch 88.0, W%R −4.2) — watch if price extends to 215.6+ on W27.

No re-forecast triggers (price-move T3 only for gbpjpy; weekly range 212.5–213.8 = <1% so no T3).
