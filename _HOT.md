# _HOT — Session State
*Always current. Updated at end of every session.*

## System Status — v2 ACTIVE (2026-06-02)
Project restarted as **structured + AI-analysis high-quality entry signal generation** (XAUUSD only).
- Markdown-only: Claude writes forecasts/validations directly (no DB).
- Unit: **Trading Zone** (max 3/week, ≤1 counter), Zone Confluence (max 10, floor 5).
- Entry Confluence (max 10, floor 5; E0 confirmation 3pt). New SL/TP/offset (see constitution).
- **R1 (Zone Confluence) + R2 (Entry Confluence) APPROVED + ACTIVE** in `confluence_criteria.md`.
  Pin tail ratio = ≥2.5×body. Ready for first v2 `/weekly`.

## Open Position
None

## Active Forecast
[2026-W23](forecasts/weekly/xauusd/2026-W23.md) — **BEARISH / MEDIUM-HIGH, conviction HIGH.** Sell bounces into resistance; price $4330 in strong downtrend.

### LIVE ORDER LIMITS (refreshed 2026-06-08 13:20 UTC scheduled NY-session run, expire 21:00 UTC — re-validate each morning)
- **PRIMARY SHORT** [9.5/10] — box **$4367–$4390**. **SELL LIMIT $4417.81 | 0.40 lots | SL $4466.95** | TP1 2.5R $4294.96 (manual) / TP2 3.0R $4270.39 (limit) / BE@1.5R $4344.10. Entry Confluence 6.0 (no E0, midpoint anchor). Invalidate: D1 close > $4390.
- **SECONDARY SHORT** [9.5/10] — box **$4450–$4485**. **SELL LIMIT $4506.81 | 0.40 lots | SL $4555.95** | TP1 2.5R $4383.96 (manual) / TP2 3.0R $4359.39 (limit) / BE@1.5R $4433.10. Entry Confluence 6.0 (no E0, midpoint anchor). Invalidate: D1 close > $4485.
- COUNTER — NONE (macro MEDIUM-HIGH + no RSI divergence).
- ⚠️ Both are resting limits well above spot ($4324) — fill only on a strong bounce. H4 ATR eased to $48.86 so SL tightened $51.08→$49.14, lots 0.39→0.40. **CPI Wed 06-10 = cancel any unfilled limit within 2h of London/NY open.**

## Week Status
- Week: 2026-W23
- Trades taken: 0 (2 limits placed, unfilled)
- Risk allocated: $3,931 (2 × $1,965.60 unfilled limits; cap $4,000/wk)
- weekly_reforecast_count: 0

## Pending Actions
- **`/validate` daily 07:30 UTC** — re-validate/refresh both live limits each morning (expire 21:00 UTC, never carry forward).
- **CPI Wed 2026-06-10 = HARD BLOCK (V3)** — cancel any live limit within 2h of London/NY open. PPI Thu, UMich Fri = caution.
- Watch CPI cool-print squeeze risk (%B below lower band = bounce risk) — sell the bounce, don't chase.

## Last Session
2026-06-08 (13:20 UTC, scheduled NY-session `/validate`) — Pulled LIVE bars to 06-08 13:20 UTC. Spot
$4324 (still well below both SHORT zones). All hard blocks pass (V1/V1b intact — last D1 close $4324 <
zone tops; V3 clear — CPI is Wed; VIX 15.4 no veto; DFII10 0 drift). No re-forecast triggers; gold moved
further in-bias. Both zones score **6.0/10 (no E0)** → **refreshed both midpoint SELL limits**: H4 ATR
eased to $48.86 so SL $51.08→$49.14, lots 0.39→0.40, PRIMARY $4419.36→$4417.81, SECONDARY
$4508.36→$4506.81 (~$3,931 risk). Rewrote `forecasts/daily/xauusd/2026-06-08.md` (superseded the 08:06 run).
2026-06-08 (08:06 UTC, scheduled London-session `/validate`) — Rebuilt `.pydeps` in fresh sandbox
(`pyrun.sh --setup`), pulled LIVE bars to 06-08 08:00 UTC. Spot $4295 (still falling away from
zones). All hard blocks pass (V1/V1b intact, V3 clear — CPI is Wed, VIX 15.4 no veto, 0 macro drift).
No re-forecast triggers; weekend gap +0.318% (note-only). Both zones score **6.0/10 (no E0)** →
**refreshed both midpoint SELL limits**: H4 ATR rose to $51.08 so SL $48.26→$51.08, lots 0.41→0.39,
PRIMARY $4417.11→$4419.36, SECONDARY $4506.11→$4508.36 (~$3,984 risk). Rewrote
`forecasts/daily/xauusd/2026-06-08.md` (superseded the 03:08 run).
2026-06-08 (earlier) — Fixed pipeline for the Linux scheduled sandbox: added `scripts/pyrun.sh` launcher
(macOS `.venv` → system python3 + persistent `.pydeps` fallback), built `.pydeps` (yfinance etc.),
patched CLAUDE.md + .gitignore. `.claude/commands/*.md` are write-protected so the launcher
convention lives in CLAUDE.md. Re-ran `/validate` on **LIVE data** (bars to 06-08 03:00 UTC):
all hard blocks pass, no re-forecast triggers, both zones score **6.0/10 (no E0)** → **placed two
midpoint SELL limits** (PRIMARY $4417.11, SECONDARY $4506.11; SL $48.26 / 0.41 lots each; ~$3,957
risk). Spot fell to $4310 (away from zones) — resting catch-the-bounce limits. Wrote
`forecasts/daily/xauusd/2026-06-08.md`.
- NOTE for user: `weekly_pull.py` names today's file `weekly_pull_2026_W24.txt` (ISO week 24) while
  the active forecast is labelled `2026-W23`. Pre-existing week-numbering mismatch — cosmetic for
  /validate (reads CSVs), but check before next `/weekly` so it doesn't write a W24 file.
2026-06-07 — First v2 `/weekly` (W23). Published 2 SHORT zones (Primary $4367–$4390, Secondary
$4450–$4485, both 9.5/10), no counter. BEARISH MEDIUM-HIGH / conviction HIGH after NFP-shock −5.08%
week. Rewrote yield_environment (W23), updated _INDEX. CPI Wed 06-10 hard block flagged.
