---
type: system
updated: 2026-05-27
confidence: low
tags: [eurusd, macro, drivers]
related: [profile.md, confluence_criteria.md]
---

# EURUSD Macro Drivers

> **STATUS: SCAFFOLD — define before running /weekly eurusd.**

## Primary Drivers (TODO — research and fill)

### 1. Fed/ECB Rate Differential
- Direction: EUR strengthens when ECB > Fed, weakens when Fed > ECB
- Data: DFF (Fed funds), ECB deposit rate (non-FRED — pull from ECB data portal or web)
- Signal: rate differential widening/narrowing + forward guidance

### 2. Relative Inflation
- EUR: EU HICP (Eurostat) or German CPI
- USD: PCE, CPI
- Signal: higher EU inflation relative to US = ECB more hawkish = EUR bullish

### 3. EU Growth Proxy
- German/EU PMI manufacturing + services
- EU GDP QoQ
- Signal: EU PMI > 50 and expanding = EUR bullish

### 4. DXY (Inverse)
- Strong negative correlation to EUR/USD
- Data: `data/yahoo/DXY.csv` (already fetched)
- Signal: DXY rising = EUR bearish; DXY falling = EUR bullish

### 5. VIX / Risk Sentiment
- USD is safe-haven — VIX spike = USD bid = EUR bearish
- Same VIXCLS data from FRED

### 6. COT Positioning
- CFTC EUR FX futures spec net position
- Extremes signal reversal risk (same logic as gold COT)
- Contract: `EURO FX - CHICAGO MERCANTILE EXCHANGE` (verify)

## Re-Forecast Triggers (TODO — define equivalent of T1-T5)

XAUUSD uses T1=DFII10, T2=DXY, T3=gold move, T4=macro shock, T5=cumulative drift.
EURUSD equivalent triggers need definition:
- T1: ECB rate surprise / unscheduled ECB action
- T2: DXY 1-day jump > 1.0% (same as XAUUSD T2)
- T3: EUR/USD D1 move > X% against weekly bias (threshold TBD)
- T4: macro shock (same T4-X/T4-Y framework)
- T5: rate differential cumulative drift (threshold TBD)

## Baseline Variables (TODO — define frontmatter fields)

XAUUSD baseline uses `baseline_dfii10` + `baseline_dxy`.
EURUSD equivalent: `baseline_fed_ecb_spread` + `baseline_dxy` (same DXY)
