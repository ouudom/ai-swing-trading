"""
api/macro.py — macro snapshot + pair-filtered news for the /macro and /news endpoints (Phase 5).

Read-only over `macro_series` (FRED yields/rates/vol/oil) and the `news` table. News filtering
reuses scripts/check_news.PAIR_KW / US_KW so the dashboard headline set matches what /weekly and
/validate read — no second keyword list to drift. Self-pins scripts/ path + CWD like the other
api modules.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta, timezone
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
import check_news  # noqa: E402  (scripts/check_news.py — PAIR_KW / US_KW)

# FRED series → display label + group, in dashboard order.
SERIES = [
    ("DGS2", "US 2Y", "rates"),
    ("DGS10", "US 10Y", "rates"),
    ("DFII10", "US 10Y real", "rates"),
    ("T5YIE", "5Y breakeven", "rates"),
    ("DFF", "Fed funds", "policy"),
    ("ECBDFR", "ECB depo", "policy"),
    ("IUDSOIA", "SONIA", "policy"),
    ("VIXCLS", "VIX", "risk"),
    ("DCOILWTICO", "WTI oil", "risk"),
]


def _f(v):
    try:
        return float(v) if v not in (None, "") else None
    except (TypeError, ValueError):
        return None


def macro_snapshot() -> dict[str, Any]:
    df = db.read_table("macro_series")
    series_out = []
    if df is not None and not df.empty:
        df = df.copy()
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        for sid, label, group in SERIES:
            sub = df[df["series_id"] == sid].dropna(subset=["value"]).sort_values("date")
            if sub.empty:
                series_out.append({"series_id": sid, "label": label, "group": group,
                                   "latest": None, "date": None, "chg_1": None, "chg_5": None})
                continue
            vals = sub["value"].to_list()
            dates = sub["date"].to_list()
            latest = vals[-1]
            prev = vals[-2] if len(vals) >= 2 else None
            five = vals[-6] if len(vals) >= 6 else None
            series_out.append({
                "series_id": sid, "label": label, "group": group,
                "latest": round(latest, 4), "date": str(dates[-1]),
                "chg_1": round(latest - prev, 4) if prev is not None else None,
                "chg_5": round(latest - five, 4) if five is not None else None,
            })
    return {"series": series_out, "as_of": max((s["date"] for s in series_out if s["date"]), default=None)}


def news_for(instrument: str, days: int = 7, limit: int = 15, query: str | None = None) -> dict[str, Any]:
    inst = instrument.lower()
    if inst not in check_news.PAIR_KW:
        return {"ok": False, "error": f"unknown instrument '{instrument}'", "headlines": []}

    df = db.read_table("news")
    if df is None or df.empty:
        return {"ok": True, "instrument": inst, "headlines": [],
                "note": "news store empty — run weekly_pull.py (RSS) to populate"}

    df = df.fillna("")
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    df = df[df["datetime_utc"].str[:10] >= cutoff]

    kws = check_news.PAIR_KW[inst] + (check_news.US_KW if inst != "eurgbp" else [])
    if query:
        kws = [query.lower()]
    mask = df["headline"].str.lower().apply(lambda h: any(k in h for k in kws))
    hits = df[mask].sort_values("datetime_utc", ascending=False).head(limit)

    headlines = [{
        "datetime_utc": r["datetime_utc"],
        "headline": r["headline"],
        "source": r["source"],
        "summary": (r["summary"][:240] if r["summary"] else None),
        "url": r["url"] or None,
        "category": r["category"] or None,
    } for _, r in hits.iterrows()]

    return {"ok": True, "instrument": inst, "days": days, "count": len(headlines),
            "headlines": headlines}
