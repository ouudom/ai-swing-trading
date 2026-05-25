# Trading Brain — Agent Operating Manual

## What This Is
XAUUSD swing trading system driven by multi-agent weekly forecasting.
- **Instrument:** XAUUSD
- **Timeframes:** Weekly → Daily → H4
- **Risk:** $2000/trade (stop = min(4H ATR, 0.5× Daily ATR))
- **TP:** 3R full close at structural level

This project was originally built for Claude Code and retains full Claude compatibility (`CLAUDE.md`, `.claude/commands/`). This file exists so Kimi Code CLI can operate it equally.

## Canonical Protocol
**Read `CLAUDE.md` first** — it contains the complete operating manual, file rules, frontmatter schemas, and session protocols. Everything in `CLAUDE.md` applies to Kimi sessions unchanged.

## Command Equivalents
Claude Code uses custom slash commands stored in `.claude/commands/`. When a Kimi user asks for any of the actions below, execute the steps from the corresponding command file:

| User Request | Reference File | Summary |
|---|---|---|
| "Run weekly forecast" / "/weekly" | `.claude/commands/weekly.md` | 5-agent analysis → new `forecasts/weekly/YYYY-WNN.md` |
| "Validate today" / "/validate [date]" | `.claude/commands/validate.md` | Daily validity check → `forecasts/daily/YYYY-MM-DD.md` |
| "Update macro" / "/macro" | `.claude/commands/macro.md` | Refresh `wiki/macro/yield_environment.md` from pull data |
| "Status" / "/status" | `.claude/commands/status.md` | Print concise system state from `_HOT.md` |

## Session Start Protocol
1. Read `_HOT.md` — check active forecast and pending actions.
2. Read `_INDEX.md` — orient to current file state.
3. Never create duplicate pages; update existing ones in place.
4. End of session: update `_HOT.md` with what changed and what is pending.

## Key Rules (Abbreviated)
- **forecasts/weekly/**: immutable after Monday open. Never edit a prior week.
- **forecasts/daily/**: append-style. One file per day.
- **data/weekly_pull/**: IMMUTABLE. Never edit `weekly_pull_*.txt`.
- **wiki/**: update in place. One concept per page. Cross-link with `[[filename]]`.
- After creating or significantly updating any file: update `_INDEX.md`.
- End of every session: update `_HOT.md`.

## System Files
- `wiki/system/constitution.md` — risk management, entry/stop/TP rules
- `wiki/system/xauusd_profile.md` — gold macro drivers, sessions, ATR ranges
- `wiki/system/confluence_criteria.md` — 7-signal scoring rubric
- `scripts/weekly_pull.py` — pipeline orchestrator (cache gate → fetch → compute). Splits: `scripts/fetch.py` (TD + FRED network only), `scripts/compute.py` (indicators + snapshot, no TD/FRED). API keys in `.env`.
