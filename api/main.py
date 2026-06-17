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
import live_r  # noqa: E402  (scripts/live_r.py — live_metrics)
from fastapi import FastAPI, Query  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from api.gates import gates_for  # noqa: E402
from api.zones import forecast_markdown, zones_for  # noqa: E402
from api.charts import chart_for  # noqa: E402
from api.edge import edge_for  # noqa: E402
from api.macro import macro_snapshot, news_for  # noqa: E402

app = FastAPI(title="Trading Brain API", version="0.0")

# Solo localhost tool — allow the Next dev server only.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3008", "http://127.0.0.1:3008"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

OPEN = {"OPEN"}
PENDING = {"PENDING"}
CLOSED = {"WIN", "LOSS", "EXPIRED"}


def _f(v):
    try:
        return float(v) if v not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _last_close(instrument: str, tf: str = "1h"):
    """Latest close for an instrument (recomputed reference price, not cached)."""
    bars = db.read_ohlc(db.clean_symbol(instrument), tf)
    if bars.empty:
        return None, None
    b = bars.sort_values("datetime")
    last = b.iloc[-1]
    return _f(last["close"]), str(last["datetime"])


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
    """Calibration / edge performance: sliceable shadow-trade stats + confluence→R scatter + shadow-vs-real."""
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


@app.get("/positions")
def positions(tf: str = "1h"):
    """Open positions (live R recomputed), pending limits (distance-to-fill), closed (stored R)."""
    df = db.read_table("trade")
    out = {"open": [], "pending": [], "closed": [], "as_of": None}
    if df.empty:
        return out

    for _, row in df.iterrows():
        t = row.to_dict()
        status = (t.get("status") or "").upper()
        base = {
            "trade_id": t.get("trade_id"),
            "instrument": t.get("instrument"),
            "direction": t.get("direction"),
            "setup": t.get("setup"),
            "week": t.get("week"),
            "entry": _f(t.get("entry")),
            "sl": _f(t.get("sl")),
            "tp": _f(t.get("tp")),
            "tp2": _f(t.get("tp2")),
            "lots": _f(t.get("lots")),
            "r_planned": _f(t.get("r_planned")),
        }

        if status in OPEN:
            bars = db.read_ohlc(db.clean_symbol(t["instrument"]), tf)
            m = live_r.live_metrics(t, bars)
            out["open"].append({**base, **{
                "r_current": m["r_current"],
                "sl_status": m["sl_status"],
                "outcome": m["outcome"],
                "tp1_touched": m["tp1_touched"],
                "tp2_touched": m["tp2_touched"],
                "mfe_r": m["mfe_r"],
                "mae_r": m["mae_r"],
                "last_px": m["last_px"],
                "as_of": m["as_of"],
                "ambiguous": m["ambiguous"],
            }})

        elif status in PENDING:
            spot, as_of = _last_close(t["instrument"], tf)
            entry = base["entry"]
            dist = None
            if spot is not None and entry is not None:
                dist = round(abs(spot - entry), 6)
            out["pending"].append({**base, **{
                "spot": spot,
                "distance_to_fill": dist,
                "expiry": t.get("expiry"),
                "as_of": as_of,
            }})

        else:  # closed / expired — stored outcome is authoritative
            out["closed"].append({**base, **{
                "status": status,
                "r_actual": _f(t.get("r_actual")),
                "exit_reason": t.get("exit_reason"),
                "exit_time": t.get("exit_time"),
                "fill_time": t.get("fill_time"),
            }})

    # cumulative realized R, oldest→newest by exit_time
    closed_sorted = sorted(
        (c for c in out["closed"] if c["r_actual"] is not None),
        key=lambda c: c.get("exit_time") or "",
    )
    cum = 0.0
    curve = []
    for c in closed_sorted:
        cum = round(cum + c["r_actual"], 3)
        curve.append({"exit_time": c["exit_time"], "trade_id": c["trade_id"], "cum_r": cum})
    out["r_curve"] = curve
    return out
