"""
api/zones.py — zone-board data for the /zones + /forecast endpoints (Phase 2).

Thin RECOMPUTE/read layer over the canonical store: zone_ledger (published zones) joined
to zone_outcome (replayed touch/R result). Never caches a derived number — board status is
derived per request from the ledger's daily_verdict/limit_price + the outcome row.

Self-pins scripts/ on the path + CWD = repo root (so `import db` works at any import order),
same as api/gates.py.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = str(_ROOT / "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)
if Path.cwd() != _ROOT:
    os.chdir(_ROOT)

import db  # noqa: E402  (scripts/db.py)

INSTRUMENTS = [
    "xauusd", "eurusd", "gbpusd", "eurgbp", "audusd", "nzdusd",
    "usdcad", "usdchf", "usdjpy", "eurjpy", "gbpjpy",
]

FORECASTS_DIR = (_ROOT / "forecasts").resolve()


def _f(v):
    try:
        return float(v) if v not in (None, "") else None
    except (TypeError, ValueError):
        return None


def current_iso_week() -> str:
    iso = datetime.now(timezone.utc).date().isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def _board_status(z: dict, o: dict | None) -> str:
    """Derived single-word board status from the ledger verdict + outcome replay."""
    verdict = (z.get("daily_verdict") or "").upper()
    if o and (o.get("status") or "").upper() == "RESOLVED":
        r = _f(o.get("r_result"))
        if r is None:
            return "RESOLVED"
        if r > 0:
            return f"WIN +{r:.1f}R"
        if r < 0:
            return f"LOSS {r:.1f}R"
        return "FLAT"
    if "INVALIDATED" in verdict:
        return "INVALIDATED"
    if "ORDER LIMIT" in verdict or _f(z.get("limit_price")) is not None:
        return "ARMED"
    if "NO TRADE" in verdict:
        return "NO_TRADE"
    if o and str(o.get("touched")).lower() == "true":
        return "TOUCHED"
    return "PENDING"


def zones_for(week: str | None = None) -> dict[str, Any]:
    """Per-instrument published zones for a week (default current ISO week)."""
    wk = week or current_iso_week()
    ledger = db.read_table("zone_ledger")
    outcome = db.read_table("zone_outcome")

    out_by_id: dict[str, dict] = {}
    if not outcome.empty:
        for _, r in outcome.iterrows():
            out_by_id[r["zone_id"]] = r.to_dict()

    instruments: dict[str, list[dict]] = {i: [] for i in INSTRUMENTS}
    n = 0
    if not ledger.empty:
        rows = ledger[ledger["week"] == wk] if "week" in ledger.columns else ledger
        for _, row in rows.iterrows():
            z = row.to_dict()
            inst = z.get("instrument")
            if inst not in instruments:
                continue
            o = out_by_id.get(z.get("zone_id"))
            instruments[inst].append({
                "zone_id": z.get("zone_id"),
                "label": z.get("label"),
                "direction": z.get("direction"),
                "zone_bottom": _f(z.get("zone_bottom")),
                "zone_top": _f(z.get("zone_top")),
                "zone_confluence": _f(z.get("zone_confluence")),
                "conviction": z.get("conviction"),
                "invalidation_level": _f(z.get("invalidation_level")),
                "tp_anchor": _f(z.get("tp_anchor")),
                "status": z.get("status"),
                "daily_verdict": z.get("daily_verdict") or None,
                "limit_price": _f(z.get("limit_price")),
                "entry_confluence": _f(z.get("entry_confluence")),
                "validated_date": z.get("validated_date") or None,
                "source_file": z.get("source_file"),
                "notes": z.get("notes") or None,
                "board_status": _board_status(z, o),
                "touched": (o and str(o.get("touched")).lower() == "true") or False,
                "r_result": _f(o.get("r_result")) if o else None,
                "mfe_r": _f(o.get("mfe_r")) if o else None,
                "mae_r": _f(o.get("mae_r")) if o else None,
            })
            n += 1

    # sort each instrument PRIMARY → SECONDARY → COUNTER, then by label
    order = {"PRIMARY": 0, "SECONDARY": 1, "COUNTER": 2}
    for i in instruments:
        instruments[i].sort(key=lambda z: (order.get((z["label"] or "").upper(), 9), z["label"] or ""))

    return {"week": wk, "count": n, "instruments": instruments}


def forecast_markdown(source_file: str) -> dict[str, Any]:
    """Raw markdown for a zone's source forecast. Path-validated: must resolve under forecasts/."""
    if not source_file:
        return {"ok": False, "error": "no source_file", "markdown": None}
    p = (_ROOT / source_file).resolve()
    try:
        p.relative_to(FORECASTS_DIR)  # raises if outside forecasts/
    except ValueError:
        return {"ok": False, "error": "path outside forecasts/", "markdown": None}
    if not p.is_file():
        return {"ok": False, "error": f"not found: {source_file}", "markdown": None}
    return {"ok": True, "source_file": source_file, "markdown": p.read_text(encoding="utf-8")}
