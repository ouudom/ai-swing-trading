"""
api/gates.py — Gate-status computation for the /gates endpoint.

Thin RECOMPUTE layer: never cache, compute per request.  Imports the
importable helpers from the three gate scripts (read-only, no argv/sys.exit
side effects) and reimplements only the tiny classification logic needed to
produce a structured JSON response for the cockpit banner.

Depends on scripts/ being on sys.path and CWD = repo root (both guaranteed by
api/main.py's module-level setup — import api.main before this, or replicate
the two lines below if called standalone).
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Self-sufficient setup (don't depend on api/main.py import order): scripts/ on the
# path + CWD pinned to repo root so `import db` / `import check_cb_calendar` resolve and
# db.py's CWD-relative DB path works whether or not api.main was imported first.
_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = str(_ROOT / "scripts")
if _SCRIPTS not in sys.path:
    sys.path.insert(0, _SCRIPTS)
if Path.cwd() != _ROOT:
    os.chdir(_ROOT)

# ── instruments ─────────────────────────────────────────────────────────────
INSTRUMENTS = [
    "xauusd", "eurusd", "gbpusd", "eurgbp", "audusd", "nzdusd",
    "usdcad", "usdchf", "usdjpy", "eurjpy", "gbpjpy",
]

JPY_PAIRS = ["usdjpy", "eurjpy", "gbpjpy"]

# Econ: instrument → country legs (mirrors check_econ_calendar.py)
PAIR_COUNTRIES: dict[str, list[str]] = {
    "xauusd": ["US"],
    "eurusd": ["US", "EU"], "gbpusd": ["US", "GB"], "eurgbp": ["EU", "GB"],
    "audusd": ["US", "AU"], "nzdusd": ["US", "NZ"], "usdcad": ["US", "CA"],
    "usdchf": ["US", "CH"], "usdjpy": ["US", "JP"],
    "eurjpy": ["EU", "JP"], "gbpjpy": ["GB", "JP"],
}

HIGH_IMPACT: set[str] = {"high", "3", "h"}

CONFIG_DIR = Path(__file__).resolve().parent.parent / "scripts" / "config"
WATCH_JSON = CONFIG_DIR / "intervention_watch.json"


# ── helpers ─────────────────────────────────────────────────────────────────

def _today_utc() -> date:
    return datetime.now(timezone.utc).date()


def _parse_date(d: str | None) -> date:
    if not d:
        return _today_utc()
    return datetime.strptime(d, "%Y-%m-%d").date()


def _last_close(instrument: str, tf: str = "1h") -> float | None:
    """Latest close for an instrument — recomputed from ohlc table, never cached."""
    try:
        import db  # scripts/db.py — on sys.path via api/main.py
        bars = db.read_ohlc(db.clean_symbol(instrument), tf)
        if bars.empty:
            return None
        last = bars.sort_values("datetime").iloc[-1]
        v = last["close"]
        return float(v) if v not in (None, "") else None
    except Exception:
        return None


# ── CB calendar ─────────────────────────────────────────────────────────────

def _cb_blocks(start: date, warnings: list[str]) -> list[dict[str, Any]]:
    """
    Return list of CB hit dicts for the 7-day lookahead window starting `start`.
    Each dict: {date, bank_code, bank_name, time_note, hard_block, caution, status}.
    Appends to warnings[] if calendar is missing or stale.
    """
    try:
        from check_cb_calendar import load_calendar  # scripts/check_cb_calendar.py
    except ImportError as exc:
        warnings.append(f"cb: cannot import check_cb_calendar ({exc})")
        return []

    end = start + timedelta(days=7)
    hits: list[dict[str, Any]] = []

    try:
        cal = load_calendar(start.year)
    except SystemExit:
        warnings.append("cb: calendar file missing — build scripts/config/cb_calendar_{}.json".format(start.year))
        return []
    except Exception as exc:
        warnings.append(f"cb: calendar load error ({exc})")
        return []

    banks = cal.get("banks", {})
    for code, bank in banks.items():
        vt = datetime.strptime(bank["verified_through"], "%Y-%m-%d").date()
        if end > vt:
            warnings.append(
                f"cb: {code} calendar only verified through {vt}; "
                f"window extends to {end} — update cb_calendar_{start.year}.json"
            )
        for d in bank.get("dates", []):
            dt = datetime.strptime(d["date"], "%Y-%m-%d").date()
            if start <= dt <= end:
                hits.append({
                    "date": str(dt),
                    "bank_code": code,
                    "bank_name": bank["name"],
                    "time_note": bank.get("time_note", ""),
                    "hard_block": bank.get("hard_block", []),
                    "caution": bank.get("caution", []),
                    "status": d.get("status", "confirmed"),
                })
    return hits


# ── Econ calendar ────────────────────────────────────────────────────────────

def _econ_blocks(start: date, warnings: list[str]) -> list[dict[str, Any]]:
    """
    Return list of high-impact econ release dicts for the 7-day window.
    Each dict: {date, time_utc, country, event, impact}.
    """
    try:
        import db
        import pandas as pd
        df = db.read_table("econ_calendar")
        if df is None or df.empty:
            raise ValueError("empty")
        df = df.fillna("")
        df["country"] = df["country"].str.upper().str.strip()
    except Exception as exc:
        warnings.append(f"econ: cannot load econ_calendar table ({exc})")
        return []

    end = start + timedelta(days=7)
    coverage_end = df["date"].max() if not df.empty else ""
    if coverage_end and str(end) > coverage_end:
        warnings.append(
            f"econ: calendar coverage ends {coverage_end} but window extends to {end} "
            f"— re-run weekly_pull.py to refetch before trusting 'no events'"
        )

    mask = (
        (df["date"] >= str(start)) &
        (df["date"] <= str(end)) &
        df["impact"].str.strip().str.lower().isin(HIGH_IMPACT)
    )
    hits_df = df[mask].sort_values(["date", "time_utc"])

    hits: list[dict[str, Any]] = []
    for _, row in hits_df.iterrows():
        hits.append({
            "date": row["date"],
            "time_utc": row.get("time_utc", ""),
            "country": row["country"],
            "event": row.get("event", ""),
            "impact": row.get("impact", ""),
        })
    return hits


# ── Intervention watch ────────────────────────────────────────────────────────

def _intervention_classify(
    instrument: str, spot: float | None, today: date, jawboning_days: int,
    warnings: list[str],
) -> tuple[str | None, str | None]:
    """
    Returns (severity, detail) for a JPY pair, or (None, None) if clear.
    severity: "HARD_BLOCK" | "CAUTION" | None
    """
    if not WATCH_JSON.exists():
        warnings.append(f"intervention: {WATCH_JSON} missing — build before trading JPY")
        return None, None

    try:
        cfg = json.loads(WATCH_JSON.read_text())
    except Exception as exc:
        warnings.append(f"intervention: cannot parse {WATCH_JSON} ({exc})")
        return None, None

    pair = cfg.get("pairs", {}).get(instrument)
    if not pair:
        warnings.append(f"intervention: {instrument} not in {WATCH_JSON}")
        return None, None

    vt = datetime.strptime(pair["verified_through"], "%Y-%m-%d").date()
    if today > vt:
        warnings.append(
            f"intervention: {instrument} watch verified only through {vt} "
            f"— refresh jawboning[] from web search and push verified_through forward"
        )
        # Still classify (stale but better than nothing)

    level = float(pair["intervention_level"])
    band = float(pair["caution_band"])

    # Recent jawboning
    cutoff = today - timedelta(days=jawboning_days)
    recent_jawboning = [
        j for j in pair.get("jawboning", [])
        if j.get("date") and datetime.strptime(j["date"], "%Y-%m-%d").date() >= cutoff
    ]

    if spot is None:
        # No spot → can't do level check; if jawboning exists, still CAUTION
        if recent_jawboning:
            jq = recent_jawboning[0]
            return "CAUTION", (
                f"MoF jawboning ({jq['date']}, {jq.get('official','?')}); "
                f"no live spot available to check vs level {level}"
            )
        return None, None

    if spot >= level:
        detail = f"spot {spot:.3f} ≥ intervention level {level} (MoF HARD BLOCK zone)"
        if recent_jawboning:
            jq = recent_jawboning[0]
            detail += f"; jawboning: {jq['date']} {jq.get('official','?')}"
        return "HARD_BLOCK", detail

    if spot >= level - band:
        detail = (
            f"spot {spot:.3f} in caution band [{level - band:.1f}–{level:.1f}] "
            f"(caution band width {band})"
        )
        if recent_jawboning:
            jq = recent_jawboning[0]
            detail += f"; jawboning: {jq['date']} {jq.get('official','?')}"
        return "CAUTION", detail

    # Clear of band — but recent jawboning = CAUTION anyway
    if recent_jawboning:
        jq = recent_jawboning[0]
        return "CAUTION", (
            f"spot {spot:.3f} clear of band [{level - band:.1f}–{level:.1f}] "
            f"but recent jawboning: {jq['date']} {jq.get('official','?')}: "
            f"\"{jq.get('quote','')}\""
        )

    return None, None


# ── Main entry point ─────────────────────────────────────────────────────────

def gates_for(query_date: str | None = None) -> dict[str, Any]:
    """
    Compute gate status for all 10 instruments.

    Returns:
    {
      "date": "YYYY-MM-DD",
      "summary": "<human-readable banner text>",
      "severity": "HARD_BLOCK" | "CAUTION" | "CLEAR",
      "instruments": {
        "<inst>": [
          { "source": "cb"|"econ"|"intervention",
            "severity": "HARD_BLOCK"|"CAUTION",
            "detail": "...",
            "when": "<date or date+time>" }
        ]
      },
      "warnings": ["..."]
    }
    """
    today = _parse_date(query_date)
    warnings: list[str] = []

    # Per-instrument block accumulator
    inst_blocks: dict[str, list[dict[str, Any]]] = {i: [] for i in INSTRUMENTS}

    # ── 1. CB calendar ──────────────────────────────────────────────────────
    cb_hits = _cb_blocks(today, warnings)
    for hit in cb_hits:
        est_note = " (ESTIMATED — verify)" if hit["status"] == "estimated" else ""
        for inst in hit["hard_block"]:
            if inst in inst_blocks:
                inst_blocks[inst].append({
                    "source": "cb",
                    "severity": "HARD_BLOCK",
                    "detail": (
                        f"{hit['bank_name']} [{hit['bank_code']}]{est_note} — {hit['time_note']}"
                    ),
                    "when": hit["date"],
                })
        for inst in hit["caution"]:
            if inst in inst_blocks:
                inst_blocks[inst].append({
                    "source": "cb",
                    "severity": "CAUTION",
                    "detail": (
                        f"{hit['bank_name']} [{hit['bank_code']}]{est_note} — {hit['time_note']}"
                    ),
                    "when": hit["date"],
                })

    # ── 2. Econ calendar ────────────────────────────────────────────────────
    econ_hits = _econ_blocks(today, warnings)
    # Build country→events map for quick lookup
    from collections import defaultdict
    country_events: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for ev in econ_hits:
        country_events[ev["country"]].append(ev)

    for inst in INSTRUMENTS:
        countries = PAIR_COUNTRIES.get(inst, [])
        for country in countries:
            for ev in country_events.get(country, []):
                when = ev["date"]
                if ev.get("time_utc"):
                    when += f" {ev['time_utc']} UTC"
                inst_blocks[inst].append({
                    "source": "econ",
                    "severity": "CAUTION",
                    "detail": f"[{country}] {ev['event']} (high-impact)",
                    "when": when,
                })

    # ── 3. Intervention watch (JPY pairs only) ───────────────────────────────
    for inst in JPY_PAIRS:
        spot = _last_close(inst)
        severity, detail = _intervention_classify(
            inst, spot, today, jawboning_days=10, warnings=warnings
        )
        if severity:
            inst_blocks[inst].append({
                "source": "intervention",
                "severity": severity,
                "detail": detail,
                "when": str(today),
            })

    # ── 4. Summary + overall severity ───────────────────────────────────────
    overall_sev = "CLEAR"
    hard_blocked: list[str] = []
    cautioned: list[str] = []

    for inst, blocks in inst_blocks.items():
        if any(b["severity"] == "HARD_BLOCK" for b in blocks):
            overall_sev = "HARD_BLOCK"
            hard_blocked.append(inst.upper())
        elif blocks:
            if overall_sev != "HARD_BLOCK":
                overall_sev = "CAUTION"
            cautioned.append(inst.upper())

    # Build human-readable summary
    iso_week = today.isocalendar()
    week_str = f"{iso_week[0]}-W{iso_week[1]:02d}"
    parts: list[str] = []

    # Group CB hard-block reasons
    cb_hard_by_bank: dict[str, list[str]] = defaultdict(list)
    for inst, blocks in inst_blocks.items():
        for b in blocks:
            if b["source"] == "cb" and b["severity"] == "HARD_BLOCK":
                # Extract bank code from detail like "US Federal Reserve FOMC [FOMC] — ..."
                try:
                    bank_code = b["detail"].split("[")[1].split("]")[0]
                except IndexError:
                    bank_code = "CB"
                cb_hard_by_bank[bank_code].append(inst.upper())

    cb_date_by_bank = {h["bank_code"]: h["date"] for h in cb_hits}
    for bank_code, insts in sorted(cb_hard_by_bank.items()):
        cb_date = cb_date_by_bank.get(bank_code, "")
        label = f"{bank_code} {cb_date}".strip()
        parts.append(f"{len(insts)} pairs HARD_BLOCK ({label})")

    if any(b["source"] == "intervention" and b["severity"] == "HARD_BLOCK"
           for blocks in inst_blocks.values() for b in blocks):
        jpy_hard = [i.upper() for i in JPY_PAIRS if any(
            b["source"] == "intervention" and b["severity"] == "HARD_BLOCK"
            for b in inst_blocks[i]
        )]
        parts.append(f"JPY {'|'.join(jpy_hard)} HARD_BLOCK (MoF intervention)")

    if any(b["source"] == "intervention" and b["severity"] == "CAUTION"
           for blocks in inst_blocks.values() for b in blocks):
        jpy_caution = [i.upper() for i in JPY_PAIRS if any(
            b["source"] == "intervention" and b["severity"] == "CAUTION"
            for b in inst_blocks[i]
        )]
        if jpy_caution:
            parts.append(f"JPY {'|'.join(jpy_caution)} CAUTION (MoF watch)")

    if overall_sev == "CLEAR":
        summary = f"{week_str} — no gate blocks active"
    else:
        summary = f"{week_str} — " + "; ".join(parts) if parts else f"{week_str} — {overall_sev}"

    return {
        "date": str(today),
        "week": week_str,
        "summary": summary,
        "severity": overall_sev,
        "instruments": inst_blocks,
        "warnings": warnings,
    }
