"""
api/edge.py — calibration / edge-performance data for the /edge endpoint (Phase 4, review half).

Reuses scripts/calibration.build() (the same aggregator that writes calibration.md) for the
sliceable edge tables — single source of truth, no duplicated stats logic — and adds two views
the markdown report doesn't expose as data: a confluence→R scatter (completed shadow trades) and
a midpoint(zone_outcome)-vs-entry-mechanics(trade_outcome) divergence summary + gate accuracy.

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


def _midpoint_vs_entry(min_n: int) -> dict[str, Any]:
    """Per-instrument: zone_outcome (midpoint fill = zone quality) vs trade_outcome
    (E0/offset/EC entry mechanics = system P&L), + the gate-accuracy table. Replaces the
    retired shadow-vs-real(`trade`) view — real fills were n≈2 and never enough."""
    zo = db.read_table("zone_outcome")
    to = db.read_table("trade_outcome")

    rows: dict[str, dict] = {}

    def slot(inst: str) -> dict:
        return rows.setdefault(inst, {
            "instrument": inst,
            "midpoint_fills": 0, "midpoint_total_r": 0.0,
            "entry_fills": 0, "entry_total_r": 0.0, "missed": 0,
        })

    if zo is not None and not zo.empty:
        done = zo[zo["status"].isin(COMPLETED_STATUSES)]
        for _, t in done.iterrows():
            s = slot(str(t.get("instrument")))
            s["midpoint_fills"] += 1
            r = _num(t.get("r_result"))
            if r is not None:
                s["midpoint_total_r"] = round(s["midpoint_total_r"] + r, 2)

    entry_total, entry_n, missed_total = 0.0, 0, 0
    if to is not None and not to.empty:
        for _, t in to.iterrows():
            inst = str(t.get("instrument"))
            st = str(t.get("status"))
            s = slot(inst)
            if st == "LIMIT_MISSED":
                s["missed"] += 1
                missed_total += 1
            elif st in COMPLETED_STATUSES:
                s["entry_fills"] += 1
                entry_n += 1
                r = _num(t.get("r_result"))
                if r is not None:
                    s["entry_total_r"] = round(s["entry_total_r"] + r, 2)
                    entry_total = round(entry_total + r, 2)

    # gate accuracy via the calibration aggregator (single source of truth)
    _md, r2 = calibration.build_r2(min_n)

    return {
        "by_instrument": sorted(rows.values(), key=lambda r: r["instrument"]),
        "entry_fills_total": entry_n,
        "entry_total_r": entry_total,
        "missed_total": missed_total,
        "gates": r2.get("gates", {}),
    }


def edge_for(min_n: int | None = None, week: str | None = None) -> dict[str, Any]:
    min_n = min_n or DEFAULT_MIN_N
    zo = db.read_table("zone_outcome")

    if zo is None or zo.empty:
        return {
            "ok": True, "min_n": min_n, "empty": True,
            "note": "no zone_outcome rows yet — run zone_outcomes.py at /weekly",
            "summary": {}, "scatter": [], "midpoint_vs_entry": _midpoint_vs_entry(min_n),
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
        "midpoint_vs_entry": _midpoint_vs_entry(min_n),
    }
