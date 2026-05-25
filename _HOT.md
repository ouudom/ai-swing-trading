# _HOT — Session State
*Always current. Updated at end of every session.*

## Open Position
None

## Active Forecast
[2026-W22](forecasts/weekly/2026-W22.md) — BEARISH / MEDIUM-HIGH macro, ALIGNED MTF, conviction MEDIUM-HIGH.

- **Setup A** [8.0/10]: SELL limit **$4591.98** ($4575 + $16.98 OUTWARD) zone $4530–$4575 | SL **$4620.28** | TP $4501.11 (**3.21R**) | **0.70 lots** — **WATCH** (val 6.5/10, no H1 trigger. Spot $4563.16 inside zone)
- **Setup B** [5.5/10]: SELL limit **$4764.86** ($4720 + $44.86 OUTWARD) zone $4690–$4720 | SL **$4798.09** | TP $4607.50 (**4.74R**) | **0.60 lots** — **WATCH** (zone unreachable, 202pt above spot)
- **Setup C**: NONE — macro MEDIUM-HIGH disqualifies; no RSI divergence

`stop_distance = avg(0.5 × D1_ATR14, H4_ATR14_trading, structural_dist)` (mean of three). D1_ATR $70.49 → 0.5×D1 $35.24. H4_ATR trading-only $31.21. Setup A: structural $18.46, stop = avg($35.24, $31.21, $18.46) = $28.30. Setup B: fallback avg($35.24, $31.21) = $33.23. `entry_offset = (10−score) × 0.3 × stop_distance` applied OUTWARD (above zone_top for short).

## Week Status
- Week: 2026-W22
- Trades taken: 0/∞ (bounded by $4000 weekly risk cap)
- Risk used: $0 / $4000 cap

## Pending Actions
- Re-validate at 08:00 UTC post-London open — H1 tape will resume, check H1 pin/engulfing/B&R inside $4530–$4575 (Setup A). Trigger window 08:00–17:00 UTC.
- **HARD BLOCK Thu 2026-05-28 12:30 UTC**: PCE Deflator + GDP 2nd Release — cancel any live limits by 10:30 UTC
- Mon 2026-05-25: US Memorial Day — reduced CME liquidity, wider spreads expected
- Watch DFII10: above 2.25% = strengthens BEARISH; below 2.00% = softens
- Watch DXY: above 120 = additional pressure; below 118 = relief
- Repair COT + GLD fetch in `scripts/weekly_pull.py` (failed again — CFTC API empty, SPDR returning PDF)
- Repair `scripts/weekly_pull.py` rate limiting: script uses 9 Twelve Data credits/minute, plan limit is 8 — add sleep/batching

## Last Session
2026-05-25 (/validate formula update v3) — Offset coefficient 0.2 → 0.3. Setup A: offset $16.98, limit $4591.98, SL $4620.28, 0.70 lots, 3.21R. Setup B: offset $44.86, limit $4764.86, SL $4798.09, 0.60 lots, 4.74R. Both WATCH. D013 logged.

2026-05-25 (/validate formula update v2) — Stop formula `avg(...)` arithmetic mean. Offset reinstated outward at 0.2 coef. D012 logged.

2026-05-25 (/validate formula update v1) — Stop formula `max(0.5×D1_ATR14, H4_ATR14_trading, structural_dist)`. H4 ATR computed on trading-day bars only (range>=$1 filter, drops weekend/holiday flatline). Order limit at zone extreme (no inward offset). Setup A: limit $4575 / SL $4610.24 / 0.56 lots / 2.10R. Setup B: limit $4720 / SL $4755.24 / 0.56 lots / 3.19R. Both WATCH. Constitution + confluence_criteria + validate.md + weekly.md + templates + stop-loss research doc + CLAUDE.md all updated.

2026-05-25 (/validate re-run with fresh Twelve Data pull) — Spot $4563.16 (was stale $4505.72 in earlier pull). Sun-CME +1.46% gap-up (Fri $4505.73 → Mon open $4571.57) put price inside Setup A zone pre-confirmation. G1 broken: H1 = bullish breakout/consolidation, not LH+LL. Score downgraded to 6.5/10 (G1 ❌, G3/G2/V2 ✅). V1 still intact (D1 close $4568.58 inside zone, today wick $4577.53 closed back to $4563.16). Setup A → WATCH pending bearish H1 trigger. Setup B unreachable. INVALIDATION line: D1 close > $4593.46.

2026-05-25 (/validate, stale data) — Both setups WATCH. Validation 10.0/10 (G1 H4 LH+LL ✅, G3 DFII10 slope +0.290 ✅, G2 D1 ATR compressed ✅, V2 drift 0.000 ✅). Hard blocks all pass (V1 D1 close $4505.72 below zones, V3 Memorial Day no news, G4 session). H1 trigger absent — tape frozen since Sat 22:00 UTC through Memorial Day. H4 ATR live calc $5.42 distorted by flatline weekend bars → used $27.51 from last active period. Setup A limit $4570.38 / 0.86 lots / SL $4593.46 / TP $4501.11 ready to place on H1 trigger. Setup B zone unreachable ($200 above spot). Re-validate 08:00 UTC.

2026-05-25 (automated /weekly re-run) — Forecast file was missing (deleted). Re-ran full 5-agent analysis. Pull successful: price $4505.72, RSI 39.6 (no div), ADX 26.3 (trending), D1 ATR compressed ($72.46 < median $75.58), EMA200 $4541.88 above price, weekend gap −0.001% (noise). COT/GLD fetch both failed again. Core PCE Q1 +4.3% YoY confirmed via web search — materially above Fed 2% target, strengthens Warsh hike case. Setup A recalculated: limit $4570.38, SL $4593.46 (structural), stop_dist $23.08, TP $4501.11 (2.89R). Setup B unchanged. Forecast saved to forecasts/weekly/2026-W22.md.

2026-05-22 — Major speed optimization on `backtest.py` (4-5× faster). Replaced pandas datetime slicing with numpy `searchsorted` + boolean arrays in `ExecutionEngine`. Per-week M1 slicing instead of scanning full 2.8M-row dataframe. Weekend gap check also vectorized. 2-year backtest: ~20s → ~5s. 8-year backtest: ~5.5min → ~1.5min expected.
