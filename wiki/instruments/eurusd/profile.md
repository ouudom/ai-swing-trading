---
type: system
updated: 2026-05-27
confidence: low
tags: [eurusd, instrument, profile]
related: [confluence_criteria.md, macro_drivers.md, constitution_addendum.md]
---

# EURUSD Instrument Profile

> **STATUS: SCAFFOLD — system details TBD. Fill before running /weekly eurusd.**

## Instrument
- Symbol: EUR/USD
- Type: FX major pair
- Tick: 0.0001 (1 pip)
- Standard lot: 100,000 units | 1 pip = $10/lot
- CME: Euro FX Futures (6E), same Fri 22:00 UTC close as CME Globex

## Lot Sizing
```
lots = floor($2,000 / (stop_distance × 10,000))
```
stop_distance expressed as price (e.g. 0.0050 = 50 pips = $500/lot risk)

## Timeframes
Weekly → Daily → H4 (same MTF stack as XAUUSD)

## Sessions
- London open: 08:00 UTC — primary session for EUR pairs
- NY open: 13:00 UTC
- Overlap 13:00–17:00 UTC: highest volume, tightest spreads
- Asian session: low EUR volume, compression expected

## ATR Ranges (TODO — fill from data)
- D1 ATR typical range: TBD
- H4 ATR typical range: TBD
- Compression threshold: TBD (< 20d median, same logic as XAUUSD)

## Key Drivers (TODO — define for confluence system)
See `macro_drivers.md` for full breakdown.

High-level:
- Fed/ECB rate differential — primary driver
- EUR/USD relative inflation (CPI, PCE vs HICP)
- EU PMI (manufacturing + services) — growth proxy
- DXY inverse correlation (strong negative)
- Risk sentiment (VIX) — USD safe-haven bid
- COT EUR FX positioning (CME, spec net)

## Data Sources
- Price: Twelve Data `EUR/USD` → `data/twelvedata/eurusd/`
- FRED: DFF, VIXCLS, DGS10 (expand TBD)
- COT: CFTC `EURO FX - CHICAGO MERCANTILE EXCHANGE` (verify exact name from deahistfo zip)
- No ETF equivalent (use COT only for positioning)
- Volume Profile: CME `6E=F` (yfinance)

## Notes
- No GLD/ETF flows — positioning read purely from COT
- ECB meeting calendar is equivalent of FOMC — hard block on ECB days
- German/EU data: German CPI, EU CPI, German Ifo, EU PMI = tier-1 scheduled events
