---
type: system
updated: 2026-05-28
confidence: medium
tags: [eurusd, instrument, profile]
related: [confluence_criteria.md, macro_drivers.md, constitution_addendum.md]
---

# EURUSD Instrument Profile

## Instrument
- Symbol: EUR/USD | FX major
- Tick: 0.0001 (1 pip) | Standard lot: 100,000 units | 1 pip = $10/lot | 1.0 move = $100,000/lot
- Futures: CME Euro FX (6E); week closes Fri 22:00 UTC

## Lot Sizing
```
lots = floor($2,000 / (stop_distance_price × 100000))
e.g. 20-pip stop (0.0020): 2000 / (0.0020 × 100000) = 10 standard lots
```

## ATR Ranges (measured 2020–2026, `scripts/calibrate_eurusd.py`, 6.4yr)
- D1 ATR14: **~69 pips** (median; mean 72) (0.0069)
- H4 ATR14: **~27 pips** (median)
- H1 ATR14: ~9 pips
- Directional baseline: 48.9% up over 5d — NO secular drift (unlike gold's 54%). EUR is range/mean-reverting.

## Timeframes
Weekly (bias) → Daily (setup) → H4 (limit placement + offset) — same MTF stack as XAUUSD.

## Sessions (UTC) — measured H1 range (pips)
- Asia 22:00–05:00: **dead**, 8–9 pips. (Gold's Asia-range gate G6 does NOT transfer → EUR G6 uses London/pre-NY 07–12.)
- London open 07:00–08:00: 17 pips
- **NY/London overlap 12:00–15:00: peak, 21–23 pips** — best fills/liquidity
- After 16:00: tapers, 11–13 pips

## Strategy
Same architecture as XAUUSD: weekly forecast → daily validation → outward-offset limit swing
entry, with fundamental + news + technical confluence. EUR-specific signals/weights/thresholds
in [[confluence_criteria]]; risk/stop/triggers in [[constitution_addendum]].

## Data
- Live: Twelve Data `EUR/USD` M15 → resampled (2023-04 → now, UTC).
- Research/backtest: `data/research/eurusd/{15min,1h,4h,1day}.csv` = HistData M1 2020-2023
  (EST-with-DST → UTC via America/New_York) merged with TD 2023→now. 6.4yr.
- Macro context: DGS2, DGS10, DFII10, ESTR, DFF, VIXCLS, DXY (none are directional gates — see macro_drivers).
