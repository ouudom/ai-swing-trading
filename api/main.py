"""
api/main.py — read-only FastAPI layer over the canonical SQLite store.

Phase 0 of the frontend plan (wiki/system/core/frontend_plan.md). Localhost only, no auth.
The API is a thin RECOMPUTE layer, never a cache: every derived value (live R, SL-touch,
distance-to-fill) is recomputed per request from the `ohlc`/`trade` tables by reusing the
pipeline scripts — same source-of-truth rule that fixed the 2026-06-15 USDCHF stale-R bug.

Run:  bash api/run.sh   (uvicorn on :8000)
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# scripts/db.py resolves the DB via a CWD-relative path; pin CWD to repo root and put
# scripts/ on the path so we can import the pipeline helpers directly.
ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / "scripts"))

import db  # noqa: E402  (scripts/db.py)
from fastapi import FastAPI, Query  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from api.gates import gates_for  # noqa: E402
from api.zones import forecast_markdown, zones_for  # noqa: E402
from api.charts import chart_for  # noqa: E402
from api.edge import edge_for  # noqa: E402
from api.macro import macro_snapshot, news_for  # noqa: E402

app = FastAPI(title="Claude Swing API", version="0.0")

# Solo localhost tool — allow the Next dev server only.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3008", "http://127.0.0.1:3008"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

def _f(v):
    try:
        return float(v) if v not in (None, "") else None
    except (TypeError, ValueError):
        return None


@app.get("/gates")
def gates(date: str | None = Query(default=None, description="YYYY-MM-DD (default: today UTC)")):
    """Gate status for all 10 instruments — CB decisions, high-impact econ releases, JPY intervention."""
    return gates_for(date)


@app.get("/zones")
def zones(week: str | None = Query(default=None, description="ISO week e.g. 2026-W25 (default: current)")):
    """Published Trading Zones per instrument for a week, joined to replayed outcomes."""
    return zones_for(week)


@app.get("/forecast")
def forecast(source_file: str = Query(description="zone_ledger source_file path under forecasts/")):
    """Raw forecast markdown for a zone's source file (path-validated under forecasts/)."""
    return forecast_markdown(source_file)


@app.get("/chart/{instrument}")
def chart(
    instrument: str,
    tf: str = Query(default="D1", description="D1 | H4 | 1H | 15M"),
    week: str | None = Query(default=None, description="ISO week for zone overlay (default current)"),
):
    """OHLC candles + overlays (zone bands, trade lines, BOS/CHoCH markers) for one instrument."""
    return chart_for(instrument, tf, week)


@app.get("/edge")
def edge(
    min_n: int | None = Query(default=None, description="min completed trades before a verdict"),
    week: str | None = Query(default=None, description="restrict to one ISO week"),
):
    """Calibration / edge performance: sliceable shadow-trade stats + confluence→R scatter + midpoint-vs-entry-mechanics + gate accuracy."""
    return edge_for(min_n, week)


@app.get("/macro")
def macro():
    """Macro snapshot — key FRED yields/rates/vol/oil with 1- and 5-obs change."""
    return macro_snapshot()


@app.get("/news/{instrument}")
def news(
    instrument: str,
    days: int = Query(default=7, description="lookback window in days"),
    limit: int = Query(default=15, description="max headlines"),
    query: str | None = Query(default=None, description="extra substring filter"),
):
    """Pair-filtered news headlines (reuses check_news keyword sets)."""
    return news_for(instrument, days, limit, query)


@app.get("/health")
def health():
    return {"ok": True, "db": str(db.DB), "exists": Path(db.DB).exists()}


_TO_COMPLETED = {"WIN_TP1", "LOSS_SL", "BREAKEVEN"}


@app.get("/positions")
def positions(tf: str = "1h"):
    """System P&L from the trade_outcome replay — there are no hand-logged live positions:
    filled (completed replay fills + R), pending (live-week limits not yet filled), missed
    (offset limit never reached = D030), and a cumulative-R curve over completed fills."""
    df = db.read_table("trade_outcome")
    out = {"filled": [], "pending": [], "missed": [], "as_of": None}
    if df.empty:
        out["r_curve"] = []
        return out

    for _, row in df.iterrows():
        t = row.to_dict()
        status = (t.get("status") or "").upper()
        base = {
            "trade_id": t.get("zone_id"),
            "instrument": t.get("instrument"),
            "direction": t.get("direction"),
            "label": t.get("label"),
            "week": t.get("week"),
            "ec_score": _f(t.get("ec_score")),
            "anchor": _f(t.get("anchor")),
            "limit_px": _f(t.get("limit_px")),
            "entry": _f(t.get("entry")),
            "sl_dist": _f(t.get("sl_dist")),
            "offset": _f(t.get("offset")),
        }
        if status in _TO_COMPLETED:
            out["filled"].append({**base, **{
                "status": status,
                "r_result": _f(t.get("r_result")),
                "mfe_r": _f(t.get("mfe_r")),
                "mae_r": _f(t.get("mae_r")),
                "fill_time": t.get("fill_time"),
                "exit_time": t.get("exit_time"),
                "block_flags": t.get("block_flags"),
                "block_verdict": t.get("block_verdict"),
            }})
        elif status == "LIMIT_MISSED":
            out["missed"].append({**base, "e0_present": t.get("e0_present")})
        elif status in ("PENDING",):
            out["pending"].append({**base, "e0_present": t.get("e0_present")})

    # cumulative replayed R, oldest→newest by exit_time
    done = sorted(
        (c for c in out["filled"] if c["r_result"] is not None),
        key=lambda c: c.get("exit_time") or "",
    )
    cum, curve = 0.0, []
    for c in done:
        cum = round(cum + c["r_result"], 3)
        curve.append({"exit_time": c["exit_time"], "trade_id": c["trade_id"], "cum_r": cum})
    out["r_curve"] = curve
    return out
