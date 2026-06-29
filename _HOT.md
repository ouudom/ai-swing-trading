# _HOT — Boot State (thin)
*First file read each session. Pointers + non-derivable judgment only.*
*RULE: **never store a value that can be computed from source** — no live R, SL-hit status, spot,
EC, ATR, ADX, V1b status, zone prices. Those live in the replay tables / `forecasts/*` / the
pull and must be recomputed, never cached here. This file = current week + open human decisions +
watch notes + where to look. Hard cap **40 lines.** Prune every session.*

## Source of truth — read these, don't duplicate them here
- **System P&L / would-be R / gate accuracy** → `trade_outcome` table in `data/database/index.db`
  (`bash scripts/pyrun.sh scripts/trade_outcome.py`; entry-mechanics replay — no hand-logged trades).
- **Current zones / forecasts** → all 11 on `forecasts/weekly/{inst}/2026-W27.md` (PENDING)
- **Shadow ledger / calibration** → `zone_ledger`/`zone_outcome` tables, `wiki/system/core/calibration.md`
- **Latest validations** → `forecasts/daily/{inst}/2026-06-29.md`
- **Macro baseline** → `wiki/system/core/macro/yield_environment.md`

## Current week — W27 LIVE (Mon 06-29 → Fri 07-03). weekly_reforecast_count = 0.
**All 11 re-forecast 06-28.** Macro: DGS2 softened 4.20→4.09 (PCE) but DXY 101.36 13-mo high → majors BEARISH/MED.
W27 zones PENDING (read forecasts/weekly for boxes/scores; recompute live numbers):
- **xauusd** SHORT 4120–4160 + 4190–4220 (BEARISH, ADX 48, GLD-inflow watch).
- **eurusd** SHORT 1.1450–1.1490 + 1.1500–1.1545 (sell oversold bounce).
- **gbpusd** SHORT 1.3340–1.3390 + COUNTER LONG 1.3140–1.3180 (D1-oversold fade, two-sided).
- **eurgbp** LONG 0.8595–0.8620 + SHORT 0.8675–0.8710 (range, squeeze ON).
- **usdchf** LONG 0.7990–0.8020 (DXY-slope-up macro-aligned).
- **usdjpy** COUNTER SHORT 161.90–162.20 only (MoF HARD-BLOCK longs ≥160; MED-LOW).
- **eurjpy** LONG 183.0–183.6 + SHORT 186.0–186.5 (range, MoF caution caps long).
- **gbpjpy** SHORT 215.0–215.6 + COUNTER LONG 212.0–212.55 (range/squeeze, MoF caution).
- **NO ZONES:** audusd (ADX 40.7) · usdcad (ADX 51.5) · nzdusd (ADX 33.7) — fade-vetoes.

## Open human decisions
- none open.

## Watch / judgment notes
- **T6 re-forecast trigger live (D029):** DGS2 drift >0.15% from **4.09** OR DXY slope20 sign-flip → re-forecast USD pairs; counters opposed by a confirmed flip void on sight. Offset retune = D030 OPEN (deferred, n=1).
- **MoF regime ACTIVE (Katayama "decisive action" G7 06-19):** usdjpy 161.7 ABOVE 160 → longs HARD-BLOCKED (only MoF-line short); eurjpy 184.2 + gbpjpy 213.4 in CAUTION bands → cap longs. intervention_watch verified_through 2026-06-29 (refreshed, no escalation).
- **ADX-veto NO-ZONES (audusd/usdcad/nzdusd):** strong trends (ADX 33–51) veto the mean-reversion fades; watch for ADX<30 to re-enable floor/top fades. usdcad/audusd long anti-edge; never trend-follow.
- **Recurring lesson (xauusd W24+W25+W26):** resistance shorts unfilled 3 weeks running in the ADX-44→48 freefall (even "nearer" 4200 missed by 1pt) → W27 PRIMARY moved to FIRST resistance above spot (4120–4160).
- **xauusd base-risk watch:** GLD +16t INFLOW + COT longs +8.5k into a 4-wk drop = positioning warning; D1 close > 4448 (POC) kills bear thesis.
- **Recurring lesson (eurusd/gbpusd/nzdusd):** counter-macro dip-buys into strong USD keep getting stopped → all W26 long-fades capped + lower zones + mandatory E0 reclaim.
- **E0 reclaim (D027):** PENDING ledger validation (pin/engulf fallback still counts).

## Last session
2026-06-29 — **/validate ALL 11, W27 day 1.** All 14 zones (8 instruments) ❌ NO TRADE, EC 1.0–4.5 (<5.0 floor) — no zone touched yet this week; generic 1H pattern hits at current spot were not zone-proximate so were discounted rather than anchoring far-off limits. usdjpy long HARD-BLOCKED (spot 161.7 in MoF zone); eurjpy/gbpjpy CAUTION caps. No re-forecast (DGS2 drift +0.10<0.15).
