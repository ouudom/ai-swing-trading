---
type: daily_validation
instrument: xauusd
date: 2026-06-26
week: 2026-W26
generated_utc: "2026-06-26T10:22:00Z"
run_type: automated_hourly
zones:
  - id: xauusd-2026-W26-PRIMARY
    direction: SHORT
    zone: [4200, 4235]
    entry_confluence: 3.5
    verdict: NO_TRADE
    e0: false
    reason: H4_CHoCH_UP_E1_dropped
  - id: xauusd-2026-W26-SECONDARY
    direction: SHORT
    zone: [4300, 4340]
    entry_confluence: 3.5
    verdict: NO_TRADE
    e0: false
    reason: H4_CHoCH_UP_E1_dropped
---

# XAUUSD Daily Validation — 2026-06-26 (W26 Friday)

**Run:** 2026-06-26 10:22 UTC (automated hourly) | **Spot:** 4049.36 | H4_ATR: 45.88 | D1_ATR: 122.76

**Gates:** ✅ CB clear | ✅ Econ clear (no high-impact today) | ✅ T4-X FALSE | VIX 18.63 (−0.86) | DXY 101.21 (slope20 +2.30)

**Macro:** DFII10 2.23 slope20 +0.14 (supports SHORT) | DGS2 4.11 drift −0.09 (< 0.15 threshold, no re-forecast) | DXY jump1d −0.224 (no gate)

---

## Zone 1 — PRIMARY SHORT 4200–4235 (ZC 8.5)

**Q1/Q2 blocks:** V1 ✅ intact | V1b ✅ intact (H4 closes 4030.57/4049.36 << 4240 threshold) | V3 ✅ clear | VIX ✅ no SHORT veto | D1 ADX 48.4 trending DOWN = WITH short zone (no veto)

**Q3 re-forecast:** No triggers (T1 DFII10 +0.14 < 0.15, T2 DXY −0.224 < 0.5, T3 no counter-move). Continue.

**Q4 Entry Confluence:**

| # | Signal | Wt | Pass | Note |
|---|--------|----|------|------|
| E0 | 1H confirm toward SHORT | 3.0 | ❌ 0 | SHORT-confirm: none. H1 09:00 RSI 61 Stoch 83 — neutral. |
| E1 | H4 structure LH+LL | 2.5 | ✅ 2.5 | D1 DOWN (BOS 4023 Jun-24). H4 last BOS DOWN 4092 → bounce to 4049 = LH forming. |
| E2 | DFII10 slope20 > 0 | 2.0 | ✅ 2.0 | +0.14 rising real yields = gold bearish. |
| E3 | Macro drift < 0.10 against dir | 1.0 | ✅ 1.0 | Drift WITH short (yields rising). |
| E4 | ATR compression | 1.0 | ❌ 0 | D1 ATR 122.76 > med 114.06. |
| E5 | DXY slope20 > 0 | 0.5 | ✅ 0.5 | +2.296. |
| **TOTAL** | | **10** | **6.0** | |

**✅ ORDER LIMIT — anchor: 50% midpoint 4217.50 (no E0)**

SL: avg(0.5×122.76=61.38, 45.88) = **53.63** | offset: max(17.88, 42.90) = **42.90**

```
XAUUSD ORDER LIMIT: SELL 4260.40 | SL 4314.03 | TP1 2.5R 4126.32 (manual) | TP2 3.0R 4099.51 (limit) | BE @1.5R 4179.95 | expires 2026-06-26 21:00 UTC
Entry Confluence: 6.0/10 (E0:❌ E1:✅ E2:✅ E3:✅ E4:❌ E5:✅)
Anchor: 50% midpoint 4217.50 | SL 53.63 | offset 42.90
```

> [!note] No E0 — midpoint anchor, re-derives hourly (D032 no lock).

---

## Zone 2 — SECONDARY SHORT 4300–4340 (ZC 7.5)

**Q1/Q2 blocks:** All identical to PRIMARY. ✅

**Q4 Entry Confluence: 6.0/10** — same conditions, same scores.

**✅ ORDER LIMIT — anchor: 50% midpoint 4320.00 (no E0)**

offset: 42.90 (same SL/EC)

```
XAUUSD ORDER LIMIT: SELL 4362.90 | SL 4416.53 | TP1 2.5R 4228.82 (manual) | TP2 3.0R 4202.01 (limit) | BE @1.5R 4282.45 | expires 2026-06-26 21:00 UTC
Entry Confluence: 6.0/10 (E0:❌ E1:✅ E2:✅ E3:✅ E4:❌ E5:✅)
Anchor: 50% midpoint 4320.00 | SL 53.63 | offset 42.90
```

> [!note] No E0 — midpoint anchor, re-derives hourly. Replay note: W26 PRIMARY zone already WIN_TP1 +2.5R (filled Mon 4210, TP1 hit Wed — see trade_outcome). Re-derived limit 4260.40 is a fresh placement. SECONDARY at 4362.90 untouched (spot 4049).

---

## Summary

| Zone | Verdict | EC | Limit |
|------|---------|----|-------|
| PRIMARY SHORT 4200–4235 | ✅ ORDER LIMIT | 6.0 | SELL 4260.40 |
| SECONDARY SHORT 4300–4340 | ✅ ORDER LIMIT | 6.0 | SELL 4362.90 |

Both limits are resting sell limits ~210–310 pts above current spot. Last day of W26.

---

## 12:12 UTC Update (automated hourly re-run)

**Spot:** 4047.02 | H4_ATR: 43.58 | D1_ATR: 122.76

**Structural change:** H4 08:00 bar closed at 12:00 UTC — **H4 CHoCH UP @ 4044.57** confirmed. H4 state shifted from DOWN → MIXED (CHoCH UP, not a full BOS). This drops E1 from ✅ 2.5 to ❌ 0 for both zones.

**Updated EC (both zones):** E0(0) + E1(0) + E2(2.0) + E3(1.0) + E4(0) + E5(0.5) = **3.5** — below 5.0 floor.

> [!note] Soft NO_TRADE (EC < floor, not a hard block). Zones remain OPEN; if H4 re-establishes LH+LL structure before 21:00 expiry and price rallies to zone, EC can recover. Cancel any resting xauusd sell limits placed from earlier today.

| Zone | Previous | Updated | Reason |
|------|----------|---------|--------|
| PRIMARY SHORT 4200–4235 | ✅ ORDER LIMIT EC 6.0 | ❌ NO TRADE EC 3.5 | H4 CHoCH UP → E1 = 0 |
| SECONDARY SHORT 4300–4340 | ✅ ORDER LIMIT EC 6.0 | ❌ NO TRADE EC 3.5 | H4 CHoCH UP → E1 = 0 |

## 15:09 UTC Re-run (automated hourly)

Spot 4081.34 (bounced from 4013 low; +68 pts today). H4_ATR: 43.58 D1_ATR: 122.76.
H4 structure: CHoCH UP @ 4044.57 (06-26 08:00) — H4 now MIXED-to-bullish. H4 Stoch 45.0/W%R −37.8/CCI −4.0 (mid).
D1 OVERSOLD (Stoch 12.3, W%R −87.7). GLD flows INFLOW +18.63t today (watch for bias).
Both SHORT zones (4200–4235, 4300–4340) remain 119–219 pts above spot. No E0 SHORT-confirm.
EC < 5.0 — **both zones ❌ NO TRADE unchanged**. No re-forecast (DGS2 drift −0.09 < 0.15). Ledger: ACCEPT.

## 16:09 UTC Re-run (automated hourly)

Spot 4090.27 | H4_ATR 44.87 | D1_ATR 122.76 | D1_ADX 48.6 (trending) | DFII10 2.230 (flat vs baseline 2.23) | DXY slope20 +2.313

**PRIMARY SHORT 4200–4235:** ❌ NO TRADE — zone unreached (spot 4090, 110 pips below zone bottom 4200). Bounce from weekly low ~3964 continuing; H4 W%R −4.0 OVERBOUGHT = bounce overextended on H4 but price hasn't approached zone. No E0 short-confirm. EC 3.5/10 (E2 DFII10 slope ✅ 2.0 · E3 macro drift ✅ 1.0 · E5 DXY slope ✅ 0.5; E0/E1/E4 ❌).

**SECONDARY SHORT 4300–4340:** ❌ NO TRADE — zone unreached (spot 4090, 210 pips below).

⚠️ **Contra-signal watch:** GLD ETF now +16.12t INFLOW (was −18.82t at forecast), COT longs +8,481 w/w INCREASING — both contra to BEARISH bias. DFII10 drift = 0.000 (flat). No T-series trigger yet; flag only. If GLD inflows persist into W27 or DFII10 dips 0.05+, re-assess bias.

V1/V1b: all clear. D1 market structure: DOWN with new BOS DOWN @4023 on 06-24. No re-forecast (T1 DGS2 drift −0.09 < 0.15; T2 DXY jump −0.207 < 0.5; T3 price move from low ~3964 = +126 = +3.2% — **note T3 threshold 2.5% TRIGGERED**).

> [!warning] T3 xauusd counter-move: 4090.27 − 3963.83 = +126.44 (+3.2%) vs low of week, exceeds 2.5% T3 threshold. However T3 is measured from the weekly FORECAST price level, not intra-week low. Weekly open ~$4013 → current 4090 = +1.9% (< 2.5%). No re-forecast at this threshold. Monitor — a close above $4114 (2.5% from 4013) triggers T3 re-forecast for W26 remainder.
