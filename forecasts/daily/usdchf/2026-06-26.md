---
type: daily_validation
instrument: usdchf
date: 2026-06-26
week: 2026-W26
generated_utc: "2026-06-26T10:22:00Z"
updated_utc: "2026-06-26T14:12:00Z"
run_type: automated_hourly
zones:
  - id: usdchf-2026-W26-PRIMARY
    direction: LONG
    zone: [0.798, 0.801]
    entry_confluence: 5.0
    verdict: ORDER_LIMIT
    e0: false
    limit_price: 0.79727
    sl: 0.00223
    sl_price: 0.79504
    tp1: 0.80285
    tp2: 0.80396
  - id: usdchf-2026-W26-COUNTER
    direction: SHORT
    verdict: NO_TRADE
    entry_confluence: 1.0
    reason: "EC 1.0 < 5.0 floor (INVALIDATED earlier)"
---

# USDCHF Daily Validation — 2026-06-26 (W26 Friday)

**Run:** 2026-06-26 10:22 UTC | **Spot:** 0.80843 | H4_ATR: 0.00198 | D1_ATR: 0.00497 | D1_med: 0.00524

**Gates:** ✅ CB clear (no SNB decision — next quarterly Sep) | ✅ Econ clear | ✅ T4-X FALSE | VIX 18.63 | DXY slope20 +2.296 (LONG aligned) | D1 ADX 34.4 (TRENDING UP — with LONG, no veto)

**Note:** E0 lock expired at 09:51 UTC (set 05:51). Re-deriving midpoint anchor.

---

## Zone 1 — PRIMARY LONG 0.798–0.801 (ZC 5.0)

**Q1/Q2 blocks:**
- V1: D1 close below zone bottom (0.798)? Spot 0.80843 >> 0.798. ✅ Intact.
- V1b: `check_v1b.py` → threshold 0.79760 | H4 closes 0.80859/0.80843 >> 0.79760. ✅ Intact.
- V3 (CB/event): No SNB today. ✅ Clear.
- D1 ADX>30 veto: ADX 34.4 > 30 BUT D1 state UP (trending WITH the LONG zone = no veto). ✅
- SNB block: No decision today. ✅

**Q3 re-forecast:** DGS2 drift = 4.11 − 4.20 = −0.09 (< 0.15 threshold, polarity FLIPPED for USDCHF so falling DGS2 is WITH short CHF). DXY slope20 +2.296 still supports LONG USDCHF. No re-forecast.

**FX Exposure:** `fx_exposure.py` → INDEPENDENT (no other live FX order limits).

**Q4 Entry Confluence:**

| # | Signal | Wt | Pass | Note |
|---|--------|----|------|------|
| E0 | 1H RSI-reclaim (35) or pin/engulf | 3.0 | ❌ 0 | LONG-confirm: none. H1 09:00 RSI 35, Stoch 16 — at threshold but no reclaim confirmed. Price above zone (0.80843 > 0.801). |
| E1 | H1/H4 oscillator still extreme LONG (W%R<−80, Stoch<20) | 2.5 | ✅ 2.5 | H4 W%R −91.1 OVERSOLD, H4 Stoch 19.3 OVERSOLD. H1 Stoch 16, RSI 35. Strong oversold cluster on H4. |
| E2 | DXY 20d slope rising (LONG USDCHF) | 1.5 | ✅ 1.5 | +2.296. DXY uptrend = USD bull = LONG USDCHF. |
| E3 | Squeeze/calm context | 1.0 | ❌ 0 | H4 TTM squeeze OFF. H1 squeeze OFF. |
| E4 | D1 ADX < 25 | 1.0 | ❌ 0 | ADX 34.4 > 25. Trending (but with, not against). |
| E5 | Zone structure intact | 1.0 | ✅ 1.0 | D1 close above 0.798. Zone intact. |
| **TOTAL** | | **10** | **5.0** | |

**✅ ORDER LIMIT — anchor: 50% midpoint 0.79950 (no E0, lock expired)**

SL: 0.5×0.00497=0.002485 > H4_ATR 0.00198 → SL = avg(0.002485, 0.00198) = **0.00223**
offset: max(0.000743, 5×0.2×0.00223) = max(0.000743, 0.00223) = **0.00223**

```
USDCHF ORDER LIMIT: BUY 0.79727 | SL 0.79504 | TP1 2.5R 0.80285 (manual) | TP2 3.0R 0.80396 (limit) | BE @1.5R 0.80062 | expires 2026-06-26 21:00 UTC
Entry Confluence: 5.0/10 (E0:❌ E1:✅ E2:✅ E3:❌ E4:❌ E5:✅)
Anchor: 50% midpoint 0.79950 | SL 0.00223 | offset 0.00223
```

> [!note] E0 lock expired 09:51 UTC. Re-derived midpoint anchor (no E0). Limit re-derives each hour (D032). Previous locked limit was 0.79730; new derivation 0.79727 (< 0.5 pip difference — stable).

---

## Zone 2 — COUNTER SHORT 0.809–0.813

**❌ NO TRADE** — Previously INVALIDATED (LOSS_SL in replay at 09:51). EC 1.0 < 5.0 floor. Already resolved.

---

## Summary

| Zone | Verdict | EC | Limit |
|------|---------|----|-------|
| PRIMARY LONG 0.798–0.801 | ✅ ORDER LIMIT | 5.0 | BUY 0.79727 |
| COUNTER SHORT 0.809–0.813 | ❌ NO TRADE | 1.0 | INVALIDATED |

Limit is 0.00843 (843 pips equiv) below current spot. Zone needs a pullback from 0.808 to 0.797.

---

## 14:12 UTC Re-run (automated hourly)

Spot 0.80732 (pulled back from 0.80843). H4_ATR: 0.00198 D1_ATR: 0.00497 DXY slope20: +2.189.
EC re-derived: E0 ❌ (no E0, price still 330+ pips above zone) | E1 ✅ 2.5 (H4 W%R −93.0, H4 Stoch K 7.0 — deep oversold) | E2 ✅ 1.5 (DXY slope20 +2.189 still positive) | E3 ❌ | E4 ❌ (D1 ADX ~52) | E5 ✅ 1.0 → EC **5.0/10** (unchanged).
Ledger: ACCEPT (no-E0, re-derives) — limit 0.79727 confirmed.

## 15:09 UTC Re-run (automated hourly)

Spot 0.80920 (above zone 0.7980–0.8010). H4_ATR: 0.00198 D1_ATR: 0.00497 DXY slope20: +2.392.
**EC DOWNGRADE: 5.0 → 2.5 → ❌ NO TRADE (soft).**
H1 RSI-reclaim fired (32→48 on 14:00 bar) → H1 no longer oversold (RSI 48.8, W%R −45.5, Stoch 54.5).
E0 ❌ (RSI-reclaim fired above zone, not at zone support) | E1 ❌ (H1 not extreme) | E2 ✅ 1.5 (DXY slope20 +2.392) | E3 ❌ (squeeze OFF) | E4 ❌ (D1 ADX 35.0 > 25) | E5 ✅ 1.0 (zone intact) → EC 2.5/10.
Note: prior run (14:12) scored E1 on H4 oversold in error (spec requires H1). H4 is oversold (Stoch 12.6, W%R −82.3) but USDCHF E1 is H1-specific. Zone re-arms when H1 dips back to extreme. Ledger: ACCEPT (no-E0, re-derives).

## 16:09 UTC Re-run (automated hourly)

Spot 0.80865 | H4_ATR 0.00203 | D1_ATR 0.00497 | D1_ADX 35.0 (trending UP) | DXY slope20 +2.313 | DGS2 4.11 (drift −0.09)

**PRIMARY LONG 0.7980–0.8010:** ❌ NO TRADE — zone not approached; spot 0.80865 is now 55 pips ABOVE zone top (0.8010). Price rallied away from the zone this week. No E0 LONG-confirm in zone. EC 2.5/10 (E2 DXY slope20 ✅ 1.5 · E6 big-figure 0.80 ✅ 1.0 · rest ❌). V1b: all clear.

**COUNTER SHORT 0.8090–0.8130:** Status RESOLVED (previous run). D1 ADX 35.0 > 30 trending UP AGAINST short = hard veto confirmed. Spot 0.80865 approaching zone bottom (25 pips), but no E0 short-confirm, H1 RSI 43 mid (not overbought), DXY slope WITH usdchf long (against short). EC well below 5.0. Not re-validating (RESOLVED).

D1 now OVERBOUGHT (Stoch 92.6, W%R −13.5, CCI +105.2, ABOVE Keltner upper) — this is the short-zone territory but ADX veto + DXY alignment + no E0 block any entry. H4 CHoCH DOWN @ 0.80899 (06-26 04:00) = intraday pullback.

No re-forecast triggers (DGS2 drift −0.09 < 0.15; DXY slope still UP; usdchf has no price-move T3 gate).
