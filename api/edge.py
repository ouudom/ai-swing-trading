"""
api/edge.py — calibration / edge-performance data for the /edge endpoint (Phase 4, review half).

Reuses scripts/calibration.build() (the same aggregator that writes calibration.md) for the
sliceable edge tables — single source of truth, no duplicated stats logic — and adds two views
the markdown report doesn't expose as data: a confluence→R scatter (completed shadow trades) and
a shadow(zone_ledger)-vs-real(trade) divergence summary.

Most slices read INSUFFICIENT / empty until zones resolve (zone_outcome is PENDING-heavy early) —
that's expected and rendered gracefully. Self-pins scripts/ path + CWD like the other api modules.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import pandas as pd

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = str(_ROOT / "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)
if Path.cwd() != _ROOT:
    os.chdir(_ROOT)

import db  # noqa: E402  (scripts/db.py)
import calibration  # noqa: E402  (scripts/calibration.py — build/session_of/stat_row)
from zone_outcomes import COMPLETED_STATUSES  # noqa: E402

DEFAULT_MIN_N = getattr(calibration, "DEFAULT_MIN_N", 10)

REAL_CLOSED = {"WIN", "LOSS", "EXPIRED"}


def _num(v):
    try:
        return float(v) if v not in (None, "") else None
    except (TypeError, ValueError):
        return None


def _scatter(zo: pd.DataFrame) -> list[dict]:
    """One point per completed shadow trade: (zone_confluence, r_result) + tags."""
    if zo.empty:
        return []
    done = zo[zo["status"].isin(COMPLETED_STATUSES)].copy()
    if done.empty:
        return []
    pts = []
    for _, r in done.iterrows():
        x = _num(r.get("zone_confluence"))
        y = _num(r.get("r_result"))
        if x is None or y is None:
            continue
        pts.append({
            "instrument": r.get("instrument"),
            "direction": r.get("direction"),
            "conviction": r.get("conviction"),
            "zone_confluence": x,
            "r_result": y,
        })
    return pts


def _shadow_vs_real() -> dict[str, Any]:
    """Per-instrument: published shadow zones vs real closed trades + realized R."""
    ledger = db.read_table("zone_ledger")
    trades = db.read_table("trade")

    rows: dict[str, dict] = {}

    def slot(inst: str) -> dict:
        return rows.setdefault(inst, {
            "instrument": inst, "shadow_zones": 0,
            "real_trades": 0, "real_total_r": 0.0,
        })

    if not ledger.empty:
        for inst, c in ledger["instrument"].value_counts().items():
            slot(str(inst))["shadow_zones"] = int(c)

    real_total = 0.0
    real_n = 0
    if not trades.empty:
        closed = trades[trades["status"].str.upper().isin(REAL_CLOSED)] if "status" in trades else trades
        for _, t in closed.iterrows():
            inst = str(t.get("instrument"))
            r = _num(t.get("r_actual"))
            s = slot(inst)
            s["real_trades"] += 1
            if r is not None:
                s["real_total_r"] = round(s["real_total_r"] + r, 2)
                real_total = round(real_total + r, 2)
            real_n += 1

    return {
        "by_instrument": sorted(rows.values(), key=lambda r: r["instrument"]),
        "real_trades_total": real_n,
        "real_total_r": real_total,
    }


def edge_for(min_n: int | None = None, week: str | None = None) -> dict[str, Any]:
    min_n = min_n or DEFAULT_MIN_N
    zo = db.read_table("zone_outcome")

    if zo is None or zo.empty:
        return {
            "ok": True, "min_n": min_n, "empty": True,
            "note": "no zone_outcome rows yet — run zone_outcomes.py at /weekly",
            "summary": {}, "scatter": [], "shadow_vs_real": _shadow_vs_real(),
        }

    for c in ("zone_confluence", "r_result", "mfe_r", "mae_r", "sl_dist", "entry"):
        if c in zo.columns:
            zo[c] = pd.to_numeric(zo[c], errors="coerce")
    if week:
        zo = zo[zo["week"] == week]

    # reuse the calibration aggregator → sliceable summary JSON (min-n gated)
    _md, summary = calibration.build(zo, min_n)

    return {
        "ok": True,
        "min_n": min_n,
        "empty": summary.get("completed_n", 0) == 0,
        "summary": summary,          # overall + by_r1/instrument/direction/conviction/session + ixd
        "scatter": _scatter(zo),
        "shadow_vs_real": _shadow_vs_real(),
    }
