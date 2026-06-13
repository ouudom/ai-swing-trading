"""
Calibration — edge-performance aggregator + persistent report.

Reads data/zone_outcomes.csv (shadow trades, written by zone_outcomes.py) and, when
present, data/trades_log.csv (real trades), then writes a sliceable markdown report to
wiki/system/core/calibration.md. This is the readout the live system needs to KILL dead
edges and size up working ones — the resolver's stdout summary vanishes; this persists
and is loaded at session start.

Slices (all derived from existing zone_outcomes columns):
  overall · R1 confluence bucket · instrument · direction · instrument×direction ·
  conviction · fill session · status mix (incl. INVALIDATED-before-fill = capital saved).

Min-n guard: no win-rate verdict is drawn below --min-n completed trades in a bucket; it
renders INSUFFICIENT instead. Per-instrument edge verdict: UNPROVEN (n<min) → WORKING /
DEAD (n>=min, by total-R sign). Avoids over-reading noise — at n=1 everything is UNPROVEN.

R2 (Entry Confluence) calibration needs REAL trades (shadow fills at zone midpoint with no
E0/offset replay), so its section stays "awaiting live trades" until trades_log.csv fills.

Usage:
    bash scripts/pyrun.sh scripts/calibration.py                 # full report, min-n 10
    bash scripts/pyrun.sh scripts/calibration.py --min-n 5
    bash scripts/pyrun.sh scripts/calibration.py --json data/calibration/summary.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from zone_outcomes import COMPLETED_STATUSES, OUTCOMES_CSV, R1_BUCKETS  # noqa: E402

REPORT_MD = Path("wiki/system/core/calibration.md")
TRADES_CSV = Path("data/trades_log.csv")
DEFAULT_MIN_N = 10

# fill-session tag by UTC hour of fill (informational; overlaps are real-market overlaps).
SESSIONS = [("Asia", 22, 7), ("London", 7, 16), ("NY", 12, 21)]


def session_of(hour: int) -> str:
    """First session window containing the UTC hour (wraps midnight for Asia)."""
    for name, lo, hi in SESSIONS:
        inside = (lo <= hour < hi) if lo < hi else (hour >= lo or hour < hi)
        if inside:
            return name
    return "Other"


def stat_row(done: pd.DataFrame, min_n: int) -> dict:
    """Win/R stats for a completed-trade subset, gated by min_n."""
    n = len(done)
    if n == 0:
        return {"n": 0, "verdict": "no data"}
    r = pd.to_numeric(done["r_result"])
    wins = int((done["status"] == "WIN_TP1").sum())
    d = {
        "n": n,
        "wins": wins,
        "win_pct": round(wins / n, 3),
        "total_r": round(float(r.sum()), 2),
        "avg_r": round(float(r.mean()), 2),
    }
    if n < min_n:
        d["verdict"] = f"INSUFFICIENT (n<{min_n})"
    else:
        d["verdict"] = "WORKING" if d["total_r"] > 0 else "DEAD"
    return d


def fmt_stat(d: dict) -> str:
    """One-line markdown cell for a stat_row dict."""
    if d["n"] == 0:
        return "—"
    base = f"n={d['n']} · win {d['win_pct']:.0%} · {d['total_r']:+.1f}R (avg {d['avg_r']:+.2f})"
    return f"{base} · **{d['verdict']}**"


def group_table(done: pd.DataFrame, col: str, min_n: int, header: str) -> tuple[str, dict]:
    """Markdown table of stat_row per distinct value of `col`, plus a json-able dict."""
    lines = [f"### By {header}", "", f"| {header} | n | win% | total R | avg R | verdict |",
             "|---|---|---|---|---|---|"]
    out = {}
    if done.empty:
        lines.append("| _(no completed trades)_ | | | | | |")
        return "\n".join(lines) + "\n", out
    for key in sorted(done[col].dropna().unique()):
        d = stat_row(done[done[col] == key], min_n)
        out[str(key)] = d
        lines.append(f"| {key} | {d['n']} | {d['win_pct']:.0%} | {d['total_r']:+.1f} | "
                     f"{d['avg_r']:+.2f} | {d['verdict']} |")
    return "\n".join(lines) + "\n", out


def build(df: pd.DataFrame, min_n: int) -> tuple[str, dict]:
    completed = df[df["status"].isin(COMPLETED_STATUSES)].copy()
    if not completed.empty:
        completed["r_result"] = pd.to_numeric(completed["r_result"], errors="coerce")
        completed["zone_confluence"] = pd.to_numeric(completed["zone_confluence"], errors="coerce")
        ft = pd.to_datetime(completed["fill_time"], errors="coerce")
        completed["session"] = ft.dt.hour.map(lambda h: session_of(int(h)) if pd.notna(h) else "—")
        score = completed["zone_confluence"]
        completed["r1_bucket"] = "—"
        for lbl, lo, hi in R1_BUCKETS:
            completed.loc[(score >= lo) & (score < hi), "r1_bucket"] = lbl

    invalidated = df[df["status"] == "INVALIDATED"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")

    j = {"generated_utc": now, "min_n": min_n, "total_zones": len(df),
         "completed_n": len(completed), "invalidated_n": len(invalidated)}

    overall = stat_row(completed, min_n)
    j["overall"] = overall

    parts = [
        "---", "type: system", f"updated: {datetime.now(timezone.utc):%Y-%m-%d}",
        "confidence: low", "tags: [calibration, edge-validation, shadow-ledger]",
        "related: [zone_outcomes, zone_ledger, constitution]", "---", "",
        "# Calibration — Edge Performance",
        "",
        f"> **AUTO-GENERATED** by `scripts/calibration.py` at {now}. Do not hand-edit — "
        "re-run the script. Source: `data/zone_outcomes.csv`.",
        "",
        f"Zones tracked: **{len(df)}** · completed shadow trades: **{len(completed)}** · "
        f"invalidated-before-fill (capital saved): **{len(invalidated)}** · "
        f"min-n for verdicts: **{min_n}**.",
        "",
        "## Overall (completed shadow trades)",
        "",
        fmt_stat(overall) if overall["n"] else "_No completed shadow trades yet — "
        "everything PENDING/NO_TOUCH/INVALIDATED._",
        "",
    ]

    # status mix (all rows)
    parts += ["## Status mix (all tracked zones)", "",
              "| status | count |", "|---|---|"]
    for st, c in df["status"].value_counts().items():
        parts.append(f"| {st} | {c} |")
    parts += ["",
              "> INVALIDATED before fill = the system refused a zone that later broke its "
              "kill level — a capital-saving outcome, not a loss.", ""]

    for col, header, key in [("r1_bucket", "R1 confluence bucket", "by_r1"),
                             ("instrument", "instrument", "by_instrument"),
                             ("direction", "direction", "by_direction"),
                             ("conviction", "conviction", "by_conviction"),
                             ("session", "fill session", "by_session")]:
        if col in completed.columns or completed.empty:
            tbl, d = group_table(completed, col, min_n, header)
            parts += [tbl]
            j[key] = d

    # instrument × direction — where the per-pair asymmetries live
    parts += ["### By instrument × direction",
              "", "| instrument | dir | n | win% | total R | verdict |",
              "|---|---|---|---|---|---|"]
    ixd = {}
    if not completed.empty:
        for (inst, dirn), sub in completed.groupby(["instrument", "direction"]):
            d = stat_row(sub, min_n)
            ixd[f"{inst}-{dirn}"] = d
            parts.append(f"| {inst} | {dirn} | {d['n']} | {d['win_pct']:.0%} | "
                         f"{d['total_r']:+.1f} | {d['verdict']} |")
    else:
        parts.append("| _(no completed trades)_ | | | | | |")
    j["by_instrument_direction"] = ixd
    parts.append("")

    # R2 / real-trade section
    parts += ["## R2 Entry Confluence (real trades only)", ""]
    real_n = 0
    if TRADES_CSV.exists():
        rt = pd.read_csv(TRADES_CSV)
        rt = rt.dropna(how="all")
        real_n = len(rt[rt.get("r_actual").notna()]) if "r_actual" in rt.columns else 0
    if real_n == 0:
        parts.append("_Awaiting live trades. Shadow trades fill at the zone midpoint with no "
                     "E0/offset replay, so Entry Confluence (R2) cannot be calibrated from "
                     "them — only from real fills in `data/trades_log.csv`._")
    else:
        parts.append(f"_{real_n} real trades logged — extend this section to bucket by R2._")
    parts += ["", "---",
              "_Verdict logic: UNPROVEN/INSUFFICIENT until n≥min-n; then WORKING (total R>0) "
              "or DEAD (total R≤0). Low n = noise; treat WORKING/DEAD as directional, not "
              "final, below ~20 trades._", ""]
    j["real_trades_n"] = real_n

    return "\n".join(parts), j


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-n", type=int, default=DEFAULT_MIN_N,
                    help=f"min completed trades before a verdict (default {DEFAULT_MIN_N})")
    ap.add_argument("--week", default="", help="restrict to one trade week")
    ap.add_argument("--json", default="", help="also write the summary as JSON to this path")
    args = ap.parse_args()

    if not OUTCOMES_CSV.exists():
        sys.exit(f"{OUTCOMES_CSV} not found — run zone_outcomes.py first")
    df = pd.read_csv(OUTCOMES_CSV, dtype={"week": str})
    if args.week:
        df = df[df["week"] == args.week]
    if df.empty:
        sys.exit("no outcome rows match")

    md, j = build(df, args.min_n)
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    tmp = str(REPORT_MD) + ".tmp"
    Path(tmp).write_text(md)
    Path(tmp).replace(REPORT_MD)
    print(f"→ {REPORT_MD} ({len(df)} zones, {j['completed_n']} completed)")

    if args.json:
        jp = Path(args.json)
        jp.parent.mkdir(parents=True, exist_ok=True)
        jp.write_text(json.dumps(j, indent=2))
        print(f"→ {jp}")

    print(f"\nOverall: {fmt_stat(j['overall']) if j['overall']['n'] else 'no completed trades'}")


if __name__ == "__main__":
    main()
