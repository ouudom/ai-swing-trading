---
type: decision
updated: 2026-06-16
confidence: high
tags: [frontend, architecture, roadmap]
related: [constitution, decisions, calibration]
---

# Frontend Plan — Trading Brain UI

Read-only dashboard over the canonical SQLite store. Two equal jobs: **live monitoring**
(cockpit) + **performance review** (calibration/edge). Solo tool, localhost only.

## Locked decisions
- **Stack:** FastAPI (Python) read-only over `data/database/index.db` → Next.js (React) frontend.
- **Live freshness:** pipeline runs hourly `/validate`. Frontend **polls every 60s** — no SSE/push.
- **Auth:** none. Localhost only. Do not expose without adding a login.
- **Charting:** `lightweight-charts` (TradingView) — best for OHLC + zone/SL/TP overlays.

## Core rule (carries from the pipeline)
**Recompute every derived value server-side, per request, from `ohlc`/`trade` — never persist a
stale number.** Live R, SL-touch, distance-to-fill, BE status are all recomputed. Same lesson as
the 06-15 USDCHF `_HOT` error (R read off cached spot, not the bar low that had hit SL). The API
is a thin recompute layer, NOT a cache.

## Architecture
```
data/database/index.db  (SQLite, canonical, gitignored)
   │  read-only connection
FastAPI  (reuse scripts/ for recompute: R, structure, gates)
   │  JSON REST, frontend polls 60s
Next.js (React) + lightweight-charts
```

## API surface (thin layer over existing scripts)
| Endpoint | Source table(s) | Reuses |
|---|---|---|
| `GET /positions` | trade + ohlc | `trade_log.py`, `live_r.py` |
| `GET /zones?week=` | forecasts + zone_ledger | `zone_ledger.py` |
| `GET /gates?date=` | cb/econ/intervention configs | `check_cb_calendar.py`, `check_econ_calendar.py`, `check_intervention_watch.py` |
| `GET /calibration` | zone_outcome | `calibration.py` |
| `GET /ohlc/{inst}?tf=` | ohlc | `lib/ohlc_store.py` |
| `GET /macro` | macro_series, market_series | weekly_pull sync |
| `GET /news/{inst}` | news | `check_news.py` |

## Phased roadmap

### Phase 0 — spine ✅ DONE (2026-06-16)
FastAPI skeleton, read-only DB conn, Next.js scaffold, 10-instrument layout shell.
`/positions` end-to-end proves the wire. Built:
- `api/main.py` — FastAPI, CWD pinned to repo root, reuses `scripts/db.py` + `scripts/live_r.live_metrics`.
  Endpoints `/health`, `/positions` (open=live-R recompute, pending=distance-to-fill, closed=stored R, r_curve=cumulative).
- `api/run.sh` — `.venv` uvicorn on 127.0.0.1:8000. `api/requirements.txt` (fastapi, uvicorn).
- `frontend/` — Next.js 16 (app router, TS, Tailwind v4). Cockpit at `app/page.tsx` polls `/positions` 60s.
  `lib/api.ts` (typed client + `NEXT_PUBLIC_API_BASE`), `lib/instruments.ts` (10 pairs), `lib/usePoll.ts`.
- ⚠ Next 16: read `frontend/node_modules/next/dist/docs/` before edits — version has breaking changes vs training data.
- Run: terminal 1 `bash api/run.sh` · terminal 2 `cd frontend && npm run dev` → http://localhost:3000.

### Phase 1 — Live cockpit (monitoring half)
- Positions table: live R, SL/TP1/TP2, BE status — all recomputed from `ohlc`.
- Pending limits: distance-to-fill, expiry countdown (PENDING rows).
- **Gate banner** (top of screen) — daily act/no-act signal. e.g. "W25 heavy CB — 8 USD pairs
  blocked, JPY trio NO ZONES."
- Closed-trades feed + cumulative R curve.

### Phase 2 — Zone board
- 10-pair grid, one cell per instrument: zone bands, R1 score, conviction, status
  (PENDING/filled/invalidated/expired).
- Counter-zone flag (≤1 rule).
- Click pair → render forecast markdown.

### Phase 3 — Charts
- `lightweight-charts`: D1/H4/1H toggle.
- Overlay zones + SL/TP/entry lines + BOS/CHoCH markers (already computed in the pull).

### Phase 4 — Calibration / edge (review half)
- Edge table sliceable by instrument / direction / R1 / conviction / session, min-n gated.
- Confluence-score → R scatter (does score predict outcome?).
- Shadow (zone_ledger) vs real (trade) divergence.

### Phase 5 — Macro / news context
- Yield-environment snapshot, pair-filtered headlines, macro-drift-vs-baseline flag.

## Open items
- Build location: **decided** — `frontend/` (Next, own `.gitignore`) + `api/` (FastAPI) at repo root.
- fastapi/uvicorn installed into the macOS `.venv`; not in pipeline `requirements.txt` (kept separate
  in `api/requirements.txt`). The sandbox `.pydeps` does NOT have them — API is a local-only tool.
- Next: Phase 1 — wire `/gates` (cb/econ/intervention) into the banner; the placeholder is live.
