# _HOT — Boot State (thin)
*First file read each session. Pointers + non-derivable judgment only.*
*RULE: **never store a value that can be computed from source** — no live R, SL-hit status, spot,
EC, ATR, ADX, V1b status, zone prices, lots. Those live in the `trade` table / `forecasts/*` / the
pull and must be recomputed, never cached here. This file = current week + open human decisions +
watch notes + where to look. Hard cap **40 lines.** Prune every session.*

## Source of truth — read these, don't duplicate them here
- **Positions / live order limits / closed trades + R** → `trade` table in `data/database/index.db`
  (`bash scripts/pyrun.sh scripts/trade_log.py list`; PENDING = live limit, LOSS/WIN = closed).
  Recompute open-position SL/TP touch from the `ohlc` table every /validate.
- **Current zones / forecasts** → `forecasts/weekly/{inst}/2026-W25.md`
- **Shadow ledger / calibration** → `zone_ledger`/`zone_outcome` tables, `wiki/system/core/calibration.md`
- **Latest validations** → `forecasts/daily/{inst}/<date>.md`
- **Macro baseline** → `wiki/system/core/macro/yield_environment.md`
- **Design beliefs / history** → `wiki/system/core/decisions.md`, `_INDEX.md`

## Current week — 2026-W25 (Mon 06-15 → Fri 06-19)
⚠ **HEAVY CB WEEK** — Tue BoJ+RBA · Wed FOMC · Thu BoE+SNB. **NEW POLICY D028 (Pre-Event Flatten):**
forward-carry is no longer auto-NO-TRADE — entries ALLOWED, order expiry = `event−60min`, fills
force-flat before the event (gates still apply: event-window ±30min/within-2h-of-open, own-CB-today,
JPY NO ZONES, EC≥5.0). e.g. a Tue USD-pair entry may run if flat by ~17:00 UTC Wed (FOMC 18:00).
JPY trio (usdjpy/eurjpy/gbpjpy) **NO ZONES** all week — BoJ 06-16 + active MoF regime (Mimura 06-10).

## Open human decisions (the reason this file exists)
- none open. (USDCHF W24 long resolved — stopped out, see trades_log.)

## Watch / judgment notes (not computable from data)
- **US–Iran ceasefire (06-14) + Hormuz reopen** — holds → gold-short/usdcad-long support, risk-on headwind to AUD/NZD shorts. Fragile — wait for hold.
- **AUDUSD:** W25 SELL expired 06-15; RBA decided 06-16 = own-CB-today HARD all day (D028 doesn't relax). **CB cal** verified only through 06-18 — verify RBNZ H2 / SNB Sep–Dec before /weekly.
- **Econ-calendar** on Forex Factory free feed (06-15); next-week/`--retro` may need operator's local run.
- **E0 reclaim (D027)** PENDING ledger validation (pin/engulf fallback counts). **MoF/JPY:** flat through
  BoJ 06-16; W26 setups = post-BoJ washouts.

## Last session
2026-06-16 18:50 UTC — /validate ALL, **first live D028 pass** (carry relaxed → per-zone EC): **0 order
limits**, now real verdicts not a blanket block. Nearest = SHORT zones price approaches from BELOW (eurusd
0.32 / gbpusd 0.44 / xauusd 0.55 H4ATR) — no SHORT E0, D1 osc mid, EC < raised ADX floors → NO TRADE; rest
2–6 ATR away. audusd HARD (RBA own-CB-today); JPY trio NO ZONES. WATCH: those 3 shorts arm on a 1H rejection
inside the zone, fill flattens pre-FOMC (17:00 Wed). No open positions; 14 PENDING; VIX 16.2; next D1 06-17 00:00.
