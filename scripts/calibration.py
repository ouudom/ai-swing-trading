"""
Calibration — edge-performance aggregator + persistent report.

Reads the zone_outcome table (R1/zone quality, fills at midpoint) and the trade_outcome
table (R2/entry mechanics + gate accuracy, written by trade_outcome.py), then writes a
sliceable markdown report to wiki/system/core/calibration.md. This is the readout the
live system needs to KILL dead edges and size up working ones — the resolver's stdout
summary vanishes; this persists and is loaded at session start.

Slices (all derived from existing zone_outcomes columns):
  overall · R1 confluence bucket · instrument · direction · instrument×direction ·
  conviction · fill session · status mix (incl. INVALIDATED-before-fill = capital saved).

Min-n guard: no win-rate verdict is drawn below --min-n completed trades in a bucket; it
renders INSUFFICIENT instead. Per-instrument edge verdict: UNPROVEN (n<min) → WORKING /
DEAD (n>=min, by total-R sign). Avoids over-reading noise — at n=1 everything is UNPROVEN.

R2 (Entry Confluence) + Gate Accuracy come from the trade_outcome replay (E0/offset/EC
applied, every gate evaluated as a non-suppressing flag → counterfactual R per gate), not
from the retired hand-logged `trade` table (n≈2, never enough to calibrate).

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

import db  # noqa: E402
from zone_outcomes import COMPLETED_STATUSES, OUTCOMES_CSV, R1_BUCKETS  # noqa: E402

REPORT_MD = Path("wiki/system/core/calibration.md")
TRADE_OUTCOMES_CSV = Path("data/trade_outcomes.csv")
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

    # R2 / Entry Confluence + Gate Accuracy — from the trade_outcome replay
    r2_md, r2_j = build_r2(min_n)
    parts.append(r2_md)
    j["r2"] = r2_j

    parts += ["---",
              "_Verdict logic: UNPROVEN/INSUFFICIENT until n≥min-n; then WORKING (total R>0) "
              "or DEAD (total R≤0). Low n = noise; treat WORKING/DEAD as directional, not "
              "final, below ~20 trades._", ""]

    return "\n".join(parts), j


# EC (Entry Confluence) buckets — parallel to R1_BUCKETS. (label, lo_incl, hi_excl).
EC_BUCKETS = [(">=8.0", 8.0, 99.0), ("6.5–7.9", 6.5, 8.0),
              ("5.0–6.4", 5.0, 6.5), ("<5.0 (sub-floor)", 0.0, 5.0)]
GATES = ["V1", "V1b", "V3", "VETO_VIX", "VETO_ADX", "INTERVENTION", "EC_FLOOR"]


def build_r2(min_n: int) -> tuple[str, dict]:
    """R2 Entry Confluence + Gate Accuracy from the trade_outcome table (entry-mechanics
    replay). Replaces the dead real-trade stub — real fills were n≈2 and never calibrated."""
    to = db.read_table("trade_outcome")
    if (to is None or to.empty) and TRADE_OUTCOMES_CSV.exists():
        to = pd.read_csv(TRADE_OUTCOMES_CSV, dtype={"week": str})
    out = {"completed_n": 0}
    parts = ["## R2 — Entry Confluence (trade_outcome replay)", ""]
    if to is None or to.empty:
        parts.append("_No trade_outcome rows — run `scripts/trade_outcome.py` first._\n")
        return "\n".join(parts), out

    to["r_result"] = pd.to_numeric(to.get("r_result"), errors="coerce")
    to["ec_score"] = pd.to_numeric(to.get("ec_score"), errors="coerce")
    done = to[to["status"].isin(COMPLETED_STATUSES)].copy()
    missed = int((to["status"] == "LIMIT_MISSED").sum())
    out["completed_n"] = len(done)

    parts.append(f"Replayed fills: completed **{len(done)}** · LIMIT_MISSED (offset never "
                 f"reached = D030 near-miss) **{missed}** · min-n **{min_n}**.\n")
    parts.append(fmt_stat(stat_row(done, min_n)) if len(done) else
                 "_No completed replayed fills yet._")
    parts.append("")

    # EC bucket table
    parts += ["### By Entry Confluence (EC) bucket", "",
              "| EC bucket | n | win% | total R | avg R | verdict |", "|---|---|---|---|---|---|"]
    ec_j = {}
    if not done.empty:
        for lbl, lo, hi in EC_BUCKETS:
            sub = done[(done["ec_score"] >= lo) & (done["ec_score"] < hi)]
            d = stat_row(sub, min_n)
            ec_j[lbl] = d
            if d["n"]:
                parts.append(f"| {lbl} | {d['n']} | {d['win_pct']:.0%} | {d['total_r']:+.1f} | "
                             f"{d['avg_r']:+.2f} | {d['verdict']} |")
    else:
        parts.append("| _(no completed fills)_ | | | | | |")
    out["by_ec"] = ec_j
    parts.append("")

    # Gate accuracy — did blocking/invalidating actually save us?
    parts += ["### Gate accuracy (was the block correct?)", "",
              "> Counterfactual: each zone is filled in replay **despite** the gate. A gate "
              "KEEPS EDGE when its blocked trades net ≤0R (loss avoided); COSTING EDGE when "
              "they net >0R (winner refused). Replaces the old unverified \"INVALIDATED = "
              "capital saved\" assumption.", "",
              "| gate | n blocked | would-be win% | would-be total R | verdict |",
              "|---|---|---|---|---|"]
    gate_j = {}
    fl = to["block_flags"].fillna("")
    for g in GATES:
        m = fl.apply(lambda s: g in s.split(",") if s else False)
        sub = done[m.reindex(done.index, fill_value=False)]
        n_block = int(m.sum())
        if sub.empty:
            gate_j[g] = {"n_blocked": n_block, "completed": 0, "verdict": f"INSUFFICIENT (n<{min_n})"}
            parts.append(f"| {g} | {n_block} | — | — | INSUFFICIENT |")
            continue
        r = pd.to_numeric(sub["r_result"])
        win = (sub["status"] == "WIN_TP1").mean()
        if len(sub) < min_n:
            verdict = f"INSUFFICIENT (n<{min_n})"
        else:
            verdict = "KEEPS EDGE" if r.sum() <= 0 else "**COSTING EDGE**"
        gate_j[g] = {"n_blocked": n_block, "completed": len(sub),
                     "total_r": round(float(r.sum()), 2), "verdict": verdict}
        parts.append(f"| {g} | {n_block} | {win:.0%} | {r.sum():+.1f} | {verdict} |")
    out["gates"] = gate_j
    parts += ["", f"> D030 offset watch: **{missed}** zones filled at the zone midpoint in "
              "`zone_outcome` but the entry-mechanics offset limit was never reached — the "
              "offset is leaving fills (often the winners) on the table.", ""]
    return "\n".join(parts), out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-n", type=int, default=DEFAULT_MIN_N,
                    help=f"min completed trades before a verdict (default {DEFAULT_MIN_N})")
    ap.add_argument("--week", default="", help="restrict to one trade week")
    ap.add_argument("--json", default="", help="also write the summary as JSON to this path")
    args = ap.parse_args()

    df = db.read_table("zone_outcome")               # canonical; CSV fallback
    if (df is None or df.empty) and OUTCOMES_CSV.exists():
        df = pd.read_csv(OUTCOMES_CSV, dtype={"week": str})
    if df is None or df.empty:
        sys.exit("no zone_outcome rows in data/index.db — run zone_outcomes.py first")
    for c in ("zone_confluence", "r_result", "mfe_r", "mae_r", "sl_dist", "entry"):
        if c in df.columns:                          # DB read is all-string → restore numerics
            df[c] = pd.to_numeric(df[c], errors="coerce")
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
