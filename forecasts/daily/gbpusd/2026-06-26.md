---
type: daily_validation
instrument: gbpusd
date: 2026-06-26
week: 2026-W26
generated_utc: "2026-06-26T10:23:00Z"
updated_utc: "2026-06-26T11:10:00Z"
zones:
  - id: gbpusd-2026-W26-PRIMARY
    direction: SHORT
    verdict: NO_TRADE
    entry_confluence: 1.0
  - id: gbpusd-2026-W26-COUNTER
    direction: LONG
    verdict: ORDER_LIMIT
    entry_confluence: 7.5
    e0: true
    limit: 1.31985
    sl: 1.31633
    tp1: 1.32865
    tp2: 1.33041
    anchor_locked_until: "2026-06-26T17:21Z"
---

# GBPUSD Daily Validation — 2026-06-26

**Spot:** 1.32167 | H4_ATR: 0.00285 | D1_ATR: 0.00819 | VIX 18.63 | DXY slope20 +2.296

**Gates:** ✅ CB clear | ✅ Econ clear | ✅ T4-X FALSE

## Zone 1 — PRIMARY SHORT 1.338–1.3415 (ZC 5.0)

Spot 1.32167 is **163 pips BELOW zone bottom** (1.338). Zone not approached.

**Q4 EC:** E0 ❌ (SHORT-confirm none; only LONG pin fired) | E1 ❌ (D1 OVERSOLD Stoch 10.8 — opposite of SHORT requirement) | E2 ❌ (H4 W%R −17.3 overbought but price far from SHORT zone) | E3 ❌ (D1 ADX 26.7 > 25) | E4 ✅ 1.0 (zone intact) | E5 ❌ (no H4 squeeze)

**EC: 1.0/10 < 5.0 → ❌ NO TRADE** — Zone far, D1 oversold (opposite of SHORT setup).

## Zone 2 — COUNTER LONG 1.314–1.320 (ZC 7.0)

Spot 1.32204 at zone boundary (H4 04:00 close 1.32058 dipped inside zone; 08:00 close 1.32204). **10:00 H1 bar: bull pin confirmed** (close 1.32230) — reversal signal from zone support area. D1 OVERSOLD (Stoch 10.8, W%R −85.8, CCI −140.3). H4 CHoCH UP at 1.32095 (06-25). FX Exposure: INDEPENDENT (usdchf LONG = opposite USD direction).

**Q4 EC (11:10 UTC, original):** E0 ✅ 3.0 (bull pin 10:00 H1 close 1.32230) | E1 ✅ 2.5 (D1 OVERSOLD) | E2 ❌ | E3 ❌ (ADX 26.7) | E4 ✅ 1.0 | E5 ❌ → EC 6.5

**Q4 EC UPGRADE (13:21 UTC):** E0 ✅ 3.0 (bull pin 12:00 H1 close 1.32161) | E1 ✅ 2.5 (D1 OVERSOLD Stoch 10.8/W%R −85.8/CCI −140.3) | E2 ❌ (H1 RSI 60 — not oversold) | E3 ❌ (ADX 26.7 > 25) | E4 ✅ 1.0 (zone intact, H4 CHoCH UP, H4 Stoch 80.5 OVERBOUGHT) | E5 ✅ 1.0 (H4 TTM squeeze ON 1 bar)

**EC: 7.5/10 ≥ 5.0 → ✅ ORDER LIMIT UPGRADE** (EC 6.5→7.5, lock reset 17:21 UTC, D032)

```
GBPUSD ORDER LIMIT: BUY 1.31985 | SL 1.31633 | TP1 2.5R 1.32865 (manual) | TP2 3.0R 1.33041 (limit) | BE @1.5R 1.32513 | expires 2026-06-26 21:00 UTC
Entry Confluence: 7.5/10 (E0:✅ E1:✅ E2:❌ E3:❌ E4:✅ E5:✅)
Anchor: 1.32161 (E0 bull pin 12:00 H1 close) | SL 0.00352 | offset 0.00176 | R:R 2.5/3.0
"If price retraces to 1.31985, order triggers. Cancel if not hit by 21:00 UTC."
```

> [!note] Anchor locked until 17:21 UTC (EC 7.5 E0-confirmed, D032 UPGRADE). Replay COUNTER LONG RUNNING +1.2R is a separate earlier fill tracked in trade_outcome; this is a resting limit at zone.

## Summary (updated 13:21 UTC)

| Zone | Verdict | EC |
|------|---------|----|
| PRIMARY SHORT 1.338–1.3415 | ❌ NO TRADE | 1.0 |
| COUNTER LONG 1.314–1.320 | ✅ ORDER LIMIT UPGRADED | 7.5 |

---

## 14:12 UTC Re-run (automated hourly)

Spot 1.32233. Lock ACTIVE until 17:21 UTC (EC 7.5, E0 confirmed). Ledger: **HOLD** — limit 1.31985 unchanged.
V1/V1b/V3: all clear. DXY jump1d −0.331 (WITH counter-long; DXY weak today). No re-forecast (DGS2 drift −0.09 < 0.15).

## 15:09 UTC Re-run (automated hourly)

Spot 1.32010. Lock ACTIVE until 17:21 UTC (EC 7.5, E0 confirmed 12:00 H1 bull pin). Ledger: **HOLD**.
Fresh EC re-scored: E0 ✅ 3.0 (locked) | E1 ✅ 2.5 (D1 Stoch 10.8/W%R −85.8/CCI −140.3 OVERSOLD) | E2 ❌ (H1 mid) | E3 ❌ (ADX 27.5>25) | E4 ✅ 1.0 (zone intact, H4 CHoCH UP) | E5 ✅ 1.0 (H4 TTM squeeze ON 1b) → EC 7.5 = locked → HOLD.
V1/V1b/V3: all clear. DXY jump1d −0.128 (supportive, DXY weak post-PCE). No re-forecast.
Resting limit 1.31985 unchanged | SL 1.31633 | TP1 1.32865 | expires 21:00 UTC.

## 16:09 UTC Re-run (automated hourly)

Spot 1.32172 | H4_ATR 0.00297 | D1_ATR 0.00819 | DXY jump −0.207 | DGS2 4.11 (drift −0.09) | VIX 18.89

Lock ACTIVE until 17:21 UTC (EC 7.5 E0-confirmed, 12:00 H1 bull pin). Fresh EC re-score: E0 ✅ 3.0 (locked) | E1 ✅ 2.5 (D1 Stoch 10.8/W%R −85.8/CCI −140.3 OVERSOLD) | E2 ❌ 0 (H1 RSI 58 mid) | E3 ❌ 0 (ADX 27.5 > 25) | E4 ✅ 1.0 (H4 BOS UP @1.32192 confirmed 12:00 bar) | E5 ✅ 1.0 (H4 TTM squeeze ON 2b) → **EC 7.5 = locked score → D032 HOLD**.

V1/V1b/V3/VETO: all clear. DXY jump −0.207 < 0.5 (not a block). No re-forecast.

**Resting limit 1.31985 UNCHANGED | SL 1.31632 | TP1 2.5R 1.32867 | TP2 3.0R 1.33044 | BE 1.32515 | expires 21:00 UTC**
PRIMARY SHORT 1.338–1.3415: ❌ NO TRADE (EC 1.0 — zone unreached, spot 163 pips below).
