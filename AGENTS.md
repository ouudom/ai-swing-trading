# Claude Swing — Agent Operating Manual

## What This Is
Multi-instrument swing trading system — **10 active instruments** (XAUUSD + 9 FX pairs):
structured rules + AI analysis → high-quality entry signals. Weekly forecast produces
**Trading Zones**; daily validation gates entries. Markdown-only — the agent writes
forecasts/validations directly (no DB).
- **Instruments:** xauusd, eurusd, gbpusd, eurgbp, audusd, nzdusd, usdcad, usdchf, usdjpy,
  eurjpy, gbpjpy — per-pair character/macro/vetoes in the constitution multi-instrument table
- **Timeframes:** Weekly/Daily bias → Daily→H4→1H top-down → 1H/15M entry confirmation
- **Risk:** Tracked in R-multiples only. SL = `H4_ATR14` if `0.5×D1_ATR14 < H4_ATR14`, else `avg(0.5×D1_ATR14, H4_ATR14)`.
- **TP:** TP1 2.5R (manual), TP2 3.0R (limit), BE at +1.5R; TP at structural anchor (compute R)

This project was built for Claude Code and retains full Claude compatibility (`CLAUDE.md`,
`.claude/commands/`). This file exists so Kimi Code CLI can operate it equally.

## Canonical Protocol
**Read `CLAUDE.md` first** — it is the complete operating manual (file rules, frontmatter schemas,
core formulas, session protocols). Everything in `CLAUDE.md` applies to Kimi sessions unchanged.
If this file ever conflicts with `CLAUDE.md`, `CLAUDE.md` wins.

## Command Equivalents
Claude Code uses custom slash commands in `.claude/commands/`. When a Kimi user asks for any action
below, execute the steps from the corresponding command file:

| User Request | Reference File | Summary |
|---|---|---|
| "Run weekly forecast" / "/weekly [instrument]" | `.claude/commands/weekly.md` | Pull data → CB-calendar check → 5-section analysis → score Trading Zones → write `forecasts/weekly/{instrument}/YYYY-WNN.md` |
| "Validate today" / "/validate [instrument] [date]" | `.claude/commands/validate.md` | CB-calendar check → daily validity + Entry Confluence per zone → write `forecasts/daily/{instrument}/YYYY-MM-DD.md` |

## Session Start Protocol
1. Read `_HOT.md` — status, active zones, pending actions.
2. Read `_INDEX.md` — orient to current file state.
3. Read `wiki/system/core/macro/yield_environment.md` — macro baseline.
4. Never create duplicate pages; update existing ones in place.
5. End of session: update `_HOT.md` with what changed and what is pending.

## Key Rules (Abbreviated)
- **forecasts/weekly/{instrument}/**: immutable after Monday open. Never edit a prior week.
- **forecasts/daily/{instrument}/**: append-style. One file per day.
- **data/weekly_pull/{instrument}/**: IMMUTABLE. Never edit `weekly_pull_*.txt`.
- **wiki/**: update in place. One concept per page. Cross-link with `[[filename]]`.
- After creating or significantly updating any file: update `_INDEX.md`.
- End of every session: update `_HOT.md`.
- Run all Python via `bash scripts/pyrun.sh <script>` (never `.venv/bin/python` — breaks in sandbox).

## System Files
- `wiki/system/core/constitution.md` — risk, SL/TP/offset, zone + re-forecast rules, per-pair table
- `wiki/system/{instrument}/{instrument}_profile.md` — drivers, sessions, ATR ranges, events
- `wiki/system/{instrument}/confluence_criteria.md` — Zone Confluence (R1) + Entry Confluence (R2)
- `scripts/weekly_pull.py` — pipeline orchestrator (cache gate → fetch → compute). Splits:
  `scripts/fetch.py` (TD + FRED network only), `scripts/compute.py` (indicators + snapshot).
- `scripts/check_cb_calendar.py` + `scripts/config/cb_calendar_{year}.json` — central-bank
  decision gate (mandatory at /weekly + /validate).
- `scripts/fx_exposure.py` — FX currency-leg netting ledger (advisory).
- `scripts/zone_ledger.py` + `scripts/zone_outcomes.py` — shadow ledger: register every published
  zone at /weekly, replay OHLC → would-be R outcomes (`data/zone_ledger.csv`, `data/zone_outcomes.csv`).
  API keys in `.env`.
