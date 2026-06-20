"""
api/charts.py — OHLC candles + overlays for the /chart endpoint (Phase 3).

Read-only over the `ohlc` table; overlays reuse zones_for (zone bands), the `trade` table
(entry/SL/TP lines), and scripts/structure.structure_events (BOS/CHoCH markers) computed on
the SAME bar window that is returned, so marker positions map 1:1 onto the candles.

Times for lightweight-charts: daily bars → 'YYYY-MM-DD' (business-day); intraday → UTC epoch
seconds. Self-pins scripts/ path + CWD = repo root, like api/gates.py / api/zones.py.
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
import structure  # noqa: E402  (scripts/structure.py)

from api.zones import zones_for  # noqa: E402

# UI label → ohlc tf value, with a sane max bar count per timeframe.
TF_MAP = {"D1": "1day", "H4": "4h", "1H": "1h", "15M": "15min"}
MAX_BARS = {"1day": 400, "4h": 500, "1h": 500, "15min": 600}


def _num(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in ("open", "high", "low", "close", "volume"):
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out.dropna(subset=["open", "high", "low", "close"])


def _is_daily(tf: str) -> bool:
    return tf == "1day"


def _chart_time(dt_str: str, daily: bool):
    """lightweight-charts time: 'YYYY-MM-DD' for daily, UTC epoch seconds for intraday."""
    if daily:
        return str(dt_str)[:10]
    ts = pd.to_datetime(dt_str, utc=True, errors="coerce")
    return None if pd.isna(ts) else int(ts.timestamp())


def chart_for(instrument: str, tf_label: str = "D1", week: str | None = None) -> dict[str, Any]:
    tf = TF_MAP.get(tf_label.upper())
    if tf is None:
        return {"ok": False, "error": f"bad tf '{tf_label}' (use D1/H4/1H/15M)"}

    raw = db.read_ohlc(db.clean_symbol(instrument), tf)
    if raw.empty:
        return {"ok": False, "error": f"no {tf} bars for {instrument}",
                "instrument": instrument, "tf": tf_label, "candles": []}

    df = _num(raw).tail(MAX_BARS[tf]).reset_index(drop=True)
    daily = _is_daily(tf)

    candles = []
    times = []
    for _, b in df.iterrows():
        t = _chart_time(b["datetime"], daily)
        if t is None:
            continue
        times.append(t)
        candles.append({
            "time": t,
            "open": round(float(b["open"]), 6),
            "high": round(float(b["high"]), 6),
            "low": round(float(b["low"]), 6),
            "close": round(float(b["close"]), 6),
        })

    # ── overlays ──────────────────────────────────────────────────────────────
    inst = instrument.lower()

    # zone bands for the (default current) week
    z = zones_for(week)
    zone_bands = [
        {
            "label": zz["label"], "direction": zz["direction"],
            "bottom": zz["zone_bottom"], "top": zz["zone_top"],
            "status": zz["board_status"],
            "invalidation": zz["invalidation_level"], "tp_anchor": zz["tp_anchor"],
        }
        for zz in z["instruments"].get(inst, [])
        if zz["zone_bottom"] is not None and zz["zone_top"] is not None
    ]

    # entry-mechanics lines from the trade_outcome replay (latest week) for this instrument
    trade_lines = []
    to = db.read_table("trade_outcome")
    if not to.empty:
        ti = to[to["instrument"] == inst]
        if not ti.empty and "week" in ti.columns:
            ti = ti[ti["week"] == ti["week"].max()]   # most recent replayed week only

        def f(v):
            try:
                return float(v) if v not in (None, "") else None
            except (TypeError, ValueError):
                return None

        for _, t in ti.iterrows():
            sign = 1 if (t.get("direction") == "LONG") else -1
            limit = f(t.get("limit_px"))
            entry = f(t.get("entry"))
            sl_dist = f(t.get("sl_dist"))
            base = entry if entry is not None else limit
            sl = tp = None
            if base is not None and sl_dist is not None:
                sl = round(base - sign * sl_dist, 6)
                tp = round(base + sign * 2.5 * sl_dist, 6)
            trade_lines.append({
                "trade_id": t.get("zone_id"), "status": (t.get("status") or "").upper(),
                "direction": t.get("direction"), "ec_score": f(t.get("ec_score")),
                "entry": entry, "sl": sl, "tp": tp, "tp2": None,
                "limit_price": limit,
            })

    # BOS/CHoCH markers on the SAME window — pos indexes into `candles`
    structure_markers = []
    try:
        se = structure.structure_events(df, lookback=len(df))
        for ev in se.get("events", []):
            pos = ev.get("pos")
            if pos is None or pos < 0 or pos >= len(times):
                continue
            structure_markers.append({
                "time": times[pos], "type": ev["type"], "dir": ev["dir"],
                "level": ev["level"],
            })
        state = se.get("state")
    except Exception as e:  # structure is best-effort context, never break the chart
        state = None
        structure_markers = []
        zone_bands and None  # noqa
        # surface as a soft note rather than failing
        return {
            "ok": True, "instrument": instrument, "tf": tf_label,
            "candles": candles,
            "overlays": {"zones": zone_bands, "trades": trade_lines, "structure": [], "state": None},
            "warnings": [f"structure: {e}"],
            "as_of": candles[-1]["time"] if candles else None,
        }

    return {
        "ok": True, "instrument": instrument, "tf": tf_label,
        "candles": candles,
        "overlays": {
            "zones": zone_bands, "trades": trade_lines,
            "structure": structure_markers, "state": state,
        },
        "as_of": candles[-1]["time"] if candles else None,
    }
