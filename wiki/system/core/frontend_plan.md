---
type: decision
updated: 2026-06-16
confidence: high
tags: [frontend, architecture, roadmap]
related: [constitution, decisions, calibration]
---

# Frontend Plan — Claude Swing UI

Read-only dashboard over the canonical SQLite store. Two equal jobs: **live monitoring**
(cockpit) + **performance review** (calibration/edge). Solo tool, localhost only.

## Locked decisions
- **Stack:** FastAPI (Python) read-only over `data/database/index.db` → Next.js (React) frontend.
- **Live freshness:** pipeline runs hourly `/validate`. Frontend **polls every 60s** — no SSE/push.
- **Auth:** none. Localhost only. Do not expose without adding a login.
- **Charting:** `lightweight-charts` (TradingView) — best for OHLC + zone/SL/TP overlays.

## Core rule (carries from the pipeline)
**Recompute every derived value server-side, per request, from `ohlc`/replay tables — never persist a
stale number.** Would-be R, SL-touch, fill status are all recomputed from OHLC. Same lesson as
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
| `GET /positions` | trade_outcome | `trade_outcome.py` (replay P&L: filled/pending/missed + gate audit) |
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
- Positions table: live R, SL/TP1/TP2, BE status — all recomputed from `ohlc`. ✅ (Phase 0)
- Pending limits: distance-to-fill, expiry countdown (PENDING rows). ✅ (Phase 0)
- Closed-trades feed + cumulative R curve. ✅ (Phase 0)
- **Gate banner** ✅ DONE (2026-06-16) — `GET /gates?date=` live in the banner + per-instrument
  grid dots. `api/gates.py` (`gates_for(date)`) reuses the 3 gate scripts read-only (imports
  `check_cb_calendar.load_calendar`, `check_econ_calendar` helpers, reimplements the intervention
  classification + reads `intervention_watch.json`); self-pins scripts/ path + CWD so it works at
  any import order. Returns per-instrument `[{source: cb|econ|intervention, severity, detail, when}]`
  + `summary` + overall `severity` + `warnings[]` (surfaces stale-calendar / coverage-gap, never crashes).
  Frontend: `lib/api.ts getGates`/`worstSeverity`, banner colored by severity, grid dots per pair.
  Did NOT modify any `scripts/` file.

### Phase 2 — Zone board ✅ DONE (2026-06-16)
- `api/zones.py` (`zones_for(week)`, default current ISO week) reads `zone_ledger` joined to
  `zone_outcome` by zone_id → per-instrument zones with bands/R1/conviction/direction/
  invalidation/tp_anchor + derived `board_status` (WIN±R / LOSS / ARMED / INVALIDATED /
  NO_TRADE / TOUCHED / PENDING) from daily_verdict+limit_price+outcome replay. Self-pins path/CWD.
- `GET /zones?week=` + `GET /forecast?source_file=` (raw forecast markdown, **path-validated**
  under `forecasts/` — traversal like `../CLAUDE.md` rejected).
- Frontend `components/ZoneBoard.tsx` (client): polls /zones 60s, 10-pair grid of zone rows
  (label/dir/band/R1/conviction + status badge), click row → modal renders the forecast markdown
  via `react-markdown`+`remark-gfm` (styled `.prose-trading` in globals.css). `lib/api.ts`
  `getZones`/`getForecast`. globals.css forced dark-only (cockpit assumes near-black canvas).
- Sorted PRIMARY→SECONDARY→COUNTER. Did NOT modify `scripts/`.

### Phase 3 — Charts ✅ DONE (2026-06-16)
- `api/charts.py` (`chart_for(inst, tf, week)`) reads `ohlc` → candles (daily='YYYY-MM-DD',
  intraday=UTC epoch s) capped per tf; overlays reuse `zones_for` (zone bands), the `trade_outcome`
  table (entry/limit/SL/TP lines from the latest replayed week), and `structure.structure_events` (BOS/CHoCH markers,
  computed on the SAME returned window so `pos` maps 1:1 onto candles) + structure `state`.
- `GET /chart/{instrument}?tf=D1|H4|1H|15M&week=`. Self-pins path/CWD. Did NOT modify `scripts/`.
- Frontend `components/PriceChart.tsx` — **lightweight-charts v5** (`addSeries(CandlestickSeries)`,
  `createSeriesMarkers`, `series.createPriceLine`). Instrument dropdown + D1/H4/1H toggle; zone
  bands as dashed top/bottom + dotted invalidation, trade lines, BOS(grey)/CHoCH(amber) arrows.
  `lib/api.ts getChart`. Chart created once in useEffect; data re-render on inst/tf change.

### Phase 4 — Calibration / edge (review half) ✅ DONE (2026-06-16)
- `api/edge.py` (`edge_for(min_n, week)`) **reuses `calibration.build()`** (same aggregator that
  writes calibration.md — no duplicated stats) → sliceable summary JSON (overall + by_r1 /
  instrument / direction / conviction / session / instrument×direction, min-n gated). Adds two
  views the markdown doesn't expose as data: confluence→R `scatter` (completed shadow trades) +
  `midpoint_vs_entry` (zone_outcome midpoint R vs trade_outcome entry-mechanics R + missed fills,
  per instrument) + gate-accuracy (per gate: blocked n / would-be R / KEEPS-or-COSTING-EDGE).
- `GET /edge?min_n=&week=`. Self-pins path/CWD. Did NOT modify `scripts/`.
- Frontend `components/EdgePanel.tsx` — stat tables (verdict colored WORKING/DEAD/INSUFFICIENT),
  hand-rolled SVG scatter (R1 5–10 × R −2..+4, green/red dots), shadow-vs-real table. `lib/api.ts getEdge`.
- NOTE: zone_outcome is PENDING-heavy early (completed_n=4, all losses → INSUFFICIENT n<10); panel
  renders the empty/insufficient state gracefully and fills as zones resolve at /weekly.

### Phase 5 — Macro / news context ✅ DONE (2026-06-16)
- `api/macro.py`: `macro_snapshot()` reads `macro_series` → 9 FRED series (DGS2/10, DFII10, T5YIE,
  DFF, ECBDFR, SONIA, VIX, WTI) with latest + Δ1-obs + Δ5-obs (Δ5 = macro drift vs week-ago
  baseline). `news_for(inst,days,limit,query)` reuses `check_news.PAIR_KW`/`US_KW` → pair-filtered
  headlines from the `news` table (no second keyword list to drift).
- `GET /macro` + `GET /news/{instrument}?days=&limit=&query=`. Self-pins path/CWD. No `scripts/` edits.
- Frontend `components/MacroPanel.tsx` — macro snapshot table (Δ colored) + instrument-selectable
  news list (headline links open external). `lib/api.ts getMacro`/`getNews`.

## Open items
- Build location: **decided** — `frontend/` (Next, own `.gitignore`) + `api/` (FastAPI) at repo root.
- fastapi/uvicorn installed into the macOS `.venv`; not in pipeline `requirements.txt` (kept separate
  in `api/requirements.txt`). The sandbox `.pydeps` does NOT have them — API is a local-only tool.
- **ALL 5 PHASES DONE (2026-06-16).** API endpoints: /health /positions /gates /zones /forecast
  /chart /edge /macro /news. Frontend cockpit one page (`app/page.tsx`) + 4 components
  (ZoneBoard, PriceChart, EdgePanel, MacroPanel). Nothing committed yet — `api/` + `frontend/`
  untracked. Possible follow-ups: commit, real-time spot (see "Live data freshness"), auth if ever
  exposed, deploy/run scripts, tests.
