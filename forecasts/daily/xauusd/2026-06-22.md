---
type: daily_validation
instrument: xauusd
date: 2026-06-22
week: 2026-W26
active_zone: PRIMARY
order_limits: 2
v3_news_clear: true
cb_gate: clear
vix_veto: false (VIX 18.44 stale 06-17 → suspended)
run: 14:15 UTC (hourly auto)
---

# Validation — 2026-06-22 14:15 UTC (W26 zones from [[2026-W26]])

Gates: CB-calendar ✅ clear · econ-calendar ✅ no high-impact US in window (Core PCE Thu 06-25 = forward-carry, not today) · VIX 18.44 (FRED 06-17, STALE >1d → SHORT veto suspended). Spot $4207.97 (now INSIDE PRIMARY 4200–4235). D1 ATR $127.67 EXPANDING (med 102.69), H4 ATR $37.61, ADX 45.1 TRENDING-down (floor 6.0). DFII10 2.23 slope ↑ + DXY slope ↑ → USD-bull, BEARISH gold confirmed. SL = avg(0.5×D1 63.84, H4 37.61) = 50.72.

> [!note] CHANGE vs 13:12: a fresh SHORT-confirm (Stoch-reclaim 82→80) fired on the 13:00 1H close (close 4200.68) AT the PRIMARY zone → PRIMARY re-arms from a no-E0 50% midpoint (EC 6.0, limit 4258.08) to a confirmation-close continuation anchor (EC 9.0, limit 4217.59). SECONDARY unchanged (no E0 at 4300–4340).

## ✅ PRIMARY SHORT 4200-4235 — ORDER LIMIT (EC 9.0/10, ZC 8.5)
```
ORDER LIMIT: SELL 4217.59 | SL 4268.31 | TP1 2.5R 4090.79 (manual) | TP2 3.0R 4065.43 (limit) | BE @1.5R 4141.51 | expires 2026-06-22 21:00 UTC
Entry Confluence: 9.0/10 (E0:✅ E1:✅ E2:✅ E3:✅ E4:❌ E5:✅)
Anchor: confirmation close 4200.68 (13:00 1H Stoch-reclaim short) | SL 50.72 | offset 16.91 | R:R structural
```
E0 ✅ Stoch-reclaim short-confirm (82→80) toward zone dir, 13:00 1H · E1 ✅ dominant H4 bearish (Supertrend down 4261, H4 PSAR short 4216.75, D1 BOS-down, ADX45 down) · E2 ✅ real-yield slope rising · E3 ✅ macro drift bearish · E4 ❌ D1 ATR expanding · E5 ✅ DXY slope up → EC 9.0. Continuation short into resistance; limit rests just above spot (outward offset). V1b ✅ intact (threshold 4240). No V1 breach. Expires 21:00 UTC.

## ✅ SECONDARY SHORT 4300-4340 — ORDER LIMIT (EC 6.0/10, ZC 7.5)
```
ORDER LIMIT: SELL 4360.58 | SL 4411.30 | TP1 2.5R 4233.78 (manual) | TP2 3.0R 4208.42 (limit) | BE @1.5R 4284.50 | expires 2026-06-22 21:00 UTC
Entry Confluence: 6.0/10 (E0:❌ E1:✅ E2:✅ E3:✅ E4:❌ E5:✅)
Anchor: 50% zone midpoint 4320.0 | SL 50.72 | offset 40.58 | R:R structural
```
No E0 at this zone (price ~153 below); resting far-OTM on outward offset. V1b ✅ intact (threshold 4345). No V1 breach. Expires 21:00 UTC.
