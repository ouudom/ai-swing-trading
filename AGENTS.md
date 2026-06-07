# Trading Brain — Agent Operating Manual

## What This Is
Single-instrument (XAUUSD) swing trading system: structured rules + AI analysis → high-quality
entry signals. Weekly forecast produces **Trading Zones**; daily validation gates entries.
Markdown-only — the agent writes forecasts/validations directly (no DB).
- **Instrument:** XAUUSD
- **Timeframes:** Weekly/Daily bias → Daily→H4→1H top-down → 1H/15M entry confirmation
- **Risk:** $2000/trade. SL = `H4_ATR14` if `0.5×D1_ATR14 < H4_ATR14`, else `avg(0.5×D1_ATR14, H4_ATR14)`
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
| "Run weekly forecast" / "/weekly" | `.claude/commands/weekly.md` | Pull data → 5-section analysis → score Trading Zones → write `forecasts/weekly/xauusd/YYYY-WNN.md` |
| "Validate today" / "/validate [date]" | `.claude/commands/validate.md` | Daily validity + Entry Confluence per zone → write `forecasts/daily/xauusd/YYYY-MM-DD.md` |

## Session Start Protocol
1. Read `_HOT.md` — status, active zones, pending actions.
2. Read `_INDEX.md` — orient to current file state.
3. Read `wiki/system/core/macro/yield_environment.md` — macro baseline.
4. Never create duplicate pages; update existing ones in place.
5. End of session: update `_HOT.md` with what changed and what is pending.

## Key Rules (Abbreviated)
- **forecasts/weekly/xauusd/**: immutable after Monday open. Never edit a prior week.
- **forecasts/daily/xauusd/**: append-style. One file per day.
- **data/weekly_pull/xauusd/**: IMMUTABLE. Never edit `weekly_pull_*.txt`.
- **wiki/**: update in place. One concept per page. Cross-link with `[[filename]]`.
- After creating or significantly updating any file: update `_INDEX.md`.
- End of every session: update `_HOT.md`.

## System Files
- `wiki/system/core/constitution.md` — risk, SL/TP/offset, zone + re-forecast rules
- `wiki/system/xauusd/xauusd_profile.md` — gold drivers, sessions, ATR ranges
- `wiki/system/xauusd/confluence_criteria.md` — Zone Confluence (R1) + Entry Confluence (R2) rubric
- `scripts/weekly_pull.py` — pipeline orchestrator (cache gate → fetch → compute). Splits:
  `scripts/fetch.py` (TD + FRED network only), `scripts/compute.py` (indicators + snapshot).
  API keys in `.env`.
