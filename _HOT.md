# _HOT — Boot State (thin)
*First file read each session. Pointers + non-derivable judgment only.*
*RULE: **never store a value that can be computed from source** — no live R, SL-hit status, spot,
EC, ATR, ADX, V1b status, zone prices, lots. Those live in `trades_log.csv` / `forecasts/*` / the
pull and must be recomputed, never cached here. This file = current week + open human decisions +
watch notes + where to look. Hard cap **40 lines.** Prune every session.*

## Source of truth — read these, don't duplicate them here
- **Positions / live order limits / closed trades + R** → `data/trades_log.csv` (PENDING = live limit,
  LOSS/WIN = closed). Recompute open-position SL/TP touch from price CSVs every /validate.
- **Current zones / forecasts** → `forecasts/weekly/{inst}/2026-W25.md`
- **Shadow ledger / calibration** → `data/zone_ledger.csv`, `wiki/system/core/calibration.md`
- **Latest validations** → `forecasts/daily/{inst}/<date>.md`
- **Macro baseline** → `wiki/system/core/macro/yield_environment.md`
- **Design beliefs / history** → `wiki/system/core/decisions.md`, `_INDEX.md`

## Current week — 2026-W25 (Mon 06-15 → Fri 06-19)
⚠ **HEAVY CB WEEK** — Tue BoJ+RBA · Wed FOMC (blocks 8 USD pairs) · Thu BoE+SNB. Clean trading
windows: **Mon + Fri**. JPY trio (usdjpy/eurjpy/gbpjpy) **NO ZONES** all week — BoJ 06-16 + active
MoF intervention regime (Mimura jawboning 06-10).

## Open human decisions (the reason this file exists)
- none open. (USDCHF W24 long resolved — stopped out, see trades_log.)

## Watch / judgment notes (not computable from data)
- **US–Iran ceasefire (06-14) + Hormuz reopen** — two-way tail: gold-short strengthens if it holds,
  oil-down supports usdcad long, mild risk-on headwind to AUD/NZD shorts. Fragile/on-off — wait for hold.
- **AUDUSD:** W25 SELL limit **expired unfilled** 06-15 21:00 UTC (max high ~0.70880, never tagged).
  RBA decision **today 06-16** = hard block; no new audusd order until post-RBA.
- **CB calendar** verified only through 06-18 in `cb_calendar_2026.json` — verify RBNZ H2 / SNB
  Sep–Dec before next /weekly.
- **Econ-calendar** on Forex Factory free feed (switched 06-15); thisweek solid, next-week/`--retro`
  feeds may need the operator's local run.
- **E0 reclaim (D027)** still PENDING ledger validation — pin/engulf fallback counts meanwhile.
- **MoF/JPY:** flat through BoJ 06-16; W26 setups = post-BoJ washouts.

## Last session
2026-06-16 02:26 UTC — /validate ALL (11 instruments, hourly). **0 order limits** — hard-block week.
Today = BoJ MPM + RBA decision day; FOMC tomorrow 06-17. JPY trio NO ZONES (BoJ/MoF). audusd RBA-blocked
(prior limit expired unfilled). xauusd/eurusd/gbpusd/nzdusd/usdcad/usdchf all pre-FOMC — a fresh fill
today carries unattended into FOMC → NO TRADE; zones intact & PENDING. eurgbp validated in full (only
non-USD pair): V1b intact both zones, price mid-range ~0.8646 (no E0), but UK CPI 06-17 06:00 + BoE 06-18
= pre-event carry block → NO TRADE. All zones remain PENDING (none invalidated). Details in
`forecasts/daily/*/2026-06-16.md`.
