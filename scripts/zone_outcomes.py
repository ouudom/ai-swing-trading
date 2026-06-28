"""
Zone outcomes — shadow-trade resolver. Replays stored OHLC against every zone in
data/zone_ledger.csv and writes would-be results to data/zone_outcomes.csv.

Answers, per published zone: did price reach it? would the trade have won? After
~20–30 resolved zones the summary shows whether Zone Confluence 8.0 actually beats
6.5 — outcome data the live system cannot produce while zones get blocked (V3) or
expire untouched.

Shadow-trade model (simplifications, deliberately documented):
  - Fill   = first 1H bar inside the trade week (Mon 00:00 → Fri 22:00 UTC) whose
             range crosses the ZONE NEAR EDGE (top for LONG, bottom for SHORT —
             the edge price hits first on approach into the zone). Entry price =
             that edge. No E0/offset replay — this measures ZONE quality, not
             entry-timing quality (that's R2's job). (Changed from zone-midpoint
             fill 2026-06-28 — edge fill is the more conservative/realistic limit
             assumption; breaks numeric comparability with pre-change resolved rows.)
  - Kill   = D1 close beyond invalidation_level (ledger value, else zone far edge)
             before fill → INVALIDATED. D1 close treated as effective at
             bar_date + 22:00 UTC (FX session close).
  - SL     = constitution formula at fill time, on closed bars only:
             H4_ATR14 if 0.5×D1_ATR14 < H4_ATR14 else avg(0.5×D1_ATR14, H4_ATR14);
             H4 bars filtered to range >= MIN_BAR_RANGE (per instrument config).
  - Manage = TP1 +2.5R; SL −1R; BE: stop → entry after a bar's MFE reaches +1.5R
             (armed from the NEXT bar). Same-bar SL+TP ambiguity → SL (conservative).
             Trade may run past the forecast week until exit or data end (RUNNING).
  - Status = PENDING (week live, no fill yet) | NO_TOUCH | TOUCH_NO_FILL |
             INVALIDATED | WIN_TP1 | LOSS_SL | BREAKEVEN | RUNNING.
             Terminal statuses flip the ledger row to RESOLVED.

Usage:
    bash scripts/pyrun.sh scripts/zone_outcomes.py            # resolve all + summary
    bash scripts/pyrun.sh scripts/zone_outcomes.py --week 2026-W24
"""

from __future__ import annotations

import argparse
import importlib
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))  # for `config.*` imports

import db  # noqa: E402
from zone_ledger import load_ledger, save_ledger  # noqa: E402

OUTCOMES_CSV = Path("data/zone_outcomes.csv")
OUTCOMES_TABLE = "zone_outcome"
TERMINAL = {"NO_TOUCH", "TOUCH_NO_FILL", "INVALIDATED", "WIN_TP1", "LOSS_SL", "BREAKEVEN"}

# R1 (zone_confluence) buckets, shared with calibration.py. (label, lo_inclusive, hi_exclusive).
R1_BUCKETS = [(">=8.0", 8.0, 99.0), ("7.0–7.9", 7.0, 8.0), ("<7.0", 0.0, 7.0)]
# Completed = a shadow trade that actually filled and reached a terminal R outcome.
COMPLETED_STATUSES = ["WIN_TP1", "LOSS_SL", "BREAKEVEN"]

OUT_COLS = [
    "zone_id", "instrument", "week", "label", "direction", "zone_confluence",
    "conviction", "status", "touched", "fill_time", "entry", "sl_dist",
    "r_result", "mfe_r", "mae_r", "exit_time", "resolved_utc",
]


def week_window(week: str):
    """'2026-W24' → (Mon 00:00 UTC, Fri 22:00 UTC) as naive UTC timestamps."""
    year, wnum = week.split("-W")
    mon = datetime.fromisocalendar(int(year), int(wnum), 1)
    start = pd.Timestamp(mon)
    return start, start + pd.Timedelta(days=4, hours=22)


def atr14_before(df: pd.DataFrame, cutoff: pd.Timestamp):
    """ATR(14) on bars with datetime strictly before cutoff. None if <15 bars."""
    d = df[df["datetime"] < cutoff]
    if len(d) < 15:
        return None
    h, l, c = d["high"], d["low"], d["close"]
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return float(tr.rolling(14).mean().iloc[-1])


def load_tf(instrument: str, tf: str) -> pd.DataFrame:
    df = db.read_ohlc(instrument, tf)        # canonical; CSV fallback for cold start
    if df is None or df.empty:
        p = Path(f"data/twelvedata/{instrument}/{tf}.csv")
        if not p.exists():
            raise FileNotFoundError(p)
        df = pd.read_csv(p)
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"])
    for c in ["open", "high", "low", "close", "volume"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.sort_values("datetime").reset_index(drop=True)


def min_bar_range(instrument: str) -> float:
    cfg = importlib.import_module(f"config.{instrument}.config")
    return float(getattr(cfg, "MIN_BAR_RANGE", 0.0))


def resolve_zone(z: pd.Series, h1: pd.DataFrame, h4: pd.DataFrame, d1: pd.DataFrame,
                 mbr: float) -> dict:
    out = {c: "" for c in OUT_COLS}
    out.update({k: z[k] for k in ["zone_id", "instrument", "week", "label", "direction",
                                  "zone_confluence", "conviction"]})
    start, end = week_window(z["week"])
    top, bot = float(z["zone_top"]), float(z["zone_bottom"])
    sign = 1 if z["direction"] == "LONG" else -1
    entry_px = top if sign > 0 else bot  # near edge: first hit on approach into the zone
    inval = z["invalidation_level"]
    inval = float(inval) if str(inval) not in ("", "nan") else (top if sign < 0 else bot)

    now = h1["datetime"].iloc[-1]
    week_live = now < end

    # invalidation: first D1 close beyond kill level, effective at date+22:00 UTC
    dwin = d1[(d1["datetime"] >= start - pd.Timedelta(days=1))]
    if sign < 0:
        killed = dwin[dwin["close"] > inval]
    else:
        killed = dwin[dwin["close"] < inval]
    kill_time = (killed["datetime"].iloc[0] + pd.Timedelta(hours=22)) if not killed.empty else None
    if kill_time is not None and kill_time > end:
        kill_time = None  # zone expires at week end anyway

    # fills only count from publish time — mid-week forecasts must not look back
    if str(z["published_utc"]) not in ("", "nan"):
        pub = pd.Timestamp(str(z["published_utc"]))
        if pub.tz is not None:
            pub = pub.tz_convert("UTC").tz_localize(None)
    else:
        pub = start
    live_from = max(start, pub)
    win = h1[(h1["datetime"] >= live_from) & (h1["datetime"] < end)]
    if kill_time is not None:
        win = win[win["datetime"] < kill_time]

    touched = win[(win["low"] <= top) & (win["high"] >= bot)]
    filled = win[(win["low"] <= entry_px) & (win["high"] >= entry_px)]
    out["touched"] = bool(len(touched))

    if filled.empty:
        if kill_time is not None:
            out["status"] = "INVALIDATED"
        elif week_live:
            out["status"] = "PENDING"
        else:
            out["status"] = "TOUCH_NO_FILL" if len(touched) else "NO_TOUCH"
        return out

    fill_bar = filled.iloc[0]
    fill_time = fill_bar["datetime"]
    out["fill_time"], out["entry"] = str(fill_time), entry_px

    d1_atr = atr14_before(d1, pd.Timestamp(fill_time.date()))
    h4_trade = h4[(h4["high"] - h4["low"]) >= mbr]
    h4_atr = atr14_before(h4_trade, fill_time)
    if d1_atr is None or h4_atr is None:
        out["status"] = "PENDING"
        out["fill_time"] = ""
        return out
    sl = h4_atr if 0.5 * d1_atr < h4_atr else (0.5 * d1_atr + h4_atr) / 2
    out["sl_dist"] = round(sl, 6)

    stop = entry_px - sign * sl
    tp = entry_px + sign * 2.5 * sl
    be_trigger = entry_px + sign * 1.5 * sl
    be_armed = False
    mfe = mae = 0.0

    walk = h1[h1["datetime"] >= fill_time]
    for _, bar in walk.iterrows():
        hi, lo = bar["high"], bar["low"]
        fav = (hi - entry_px) if sign > 0 else (entry_px - lo)
        adv = (entry_px - lo) if sign > 0 else (hi - entry_px)
        mfe, mae = max(mfe, fav / sl), max(mae, adv / sl)

        stopped = lo <= stop if sign > 0 else hi >= stop
        hit_tp = hi >= tp if sign > 0 else lo <= tp
        if stopped:  # same-bar ambiguity → stop first (conservative)
            out["status"] = "BREAKEVEN" if be_armed and stop == entry_px else "LOSS_SL"
            out["r_result"] = 0.0 if out["status"] == "BREAKEVEN" else -1.0
            out["exit_time"] = str(bar["datetime"])
            break
        if hit_tp:
            out["status"], out["r_result"] = "WIN_TP1", 2.5
            out["exit_time"] = str(bar["datetime"])
            break
        if not be_armed and (hi >= be_trigger if sign > 0 else lo <= be_trigger):
            be_armed = True
            stop = entry_px  # armed; effective next bar (this bar's stop already checked)
    else:
        out["status"] = "RUNNING"
        last_close = walk["close"].iloc[-1]
        out["r_result"] = round(sign * (last_close - entry_px) / sl, 2)

    out["mfe_r"], out["mae_r"] = round(mfe, 2), round(mae, 2)
    return out


def summarize(df: pd.DataFrame):
    print("\n── Zone outcome summary " + "─" * 40)
    print(df["status"].value_counts().to_string())
    done = df[df["status"].isin(COMPLETED_STATUSES)]
    if done.empty:
        print("\nNo completed shadow trades yet.")
        return
    r = pd.to_numeric(done["r_result"])
    wins = (done["status"] == "WIN_TP1").sum()
    print(f"\nCompleted: {len(done)} | wins {wins} ({wins / len(done):.0%}) | "
          f"total {r.sum():+.1f}R | avg {r.mean():+.2f}R")
    score = pd.to_numeric(done["zone_confluence"])
    for lbl, lo, hi in R1_BUCKETS:
        m = (score >= lo) & (score < hi)
        n = m.sum()
        if n:
            w = ((done["status"] == "WIN_TP1") & m).sum()
            print(f"  R1 {lbl}: n={n} win {w / n:.0%} avg {r[m].mean():+.2f}R")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", default="", help="resolve only this trade week")
    ap.add_argument("--instrument", default="")
    args = ap.parse_args()

    ledger = load_ledger()
    if ledger.empty:
        sys.exit("ledger empty — register zones with zone_ledger.py first")
    todo = ledger.copy()
    if args.week:
        todo = todo[todo["week"] == args.week]
    if args.instrument:
        todo = todo[todo["instrument"] == args.instrument]

    rows, data_cache = [], {}
    for _, z in todo.iterrows():
        inst = z["instrument"]
        if inst not in data_cache:
            data_cache[inst] = (load_tf(inst, "1h"), load_tf(inst, "4h"),
                                load_tf(inst, "1day"), min_bar_range(inst))
        h1, h4, d1, mbr = data_cache[inst]
        out = resolve_zone(z, h1, h4, d1, mbr)
        out["resolved_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows.append(out)
        ledger.loc[ledger["zone_id"] == z["zone_id"], "status"] = (
            "RESOLVED" if out["status"] in TERMINAL else "OPEN")
        print(f"{z['zone_id']:<32} {z['direction']:<5} "
              f"{z['zone_bottom']}–{z['zone_top']}  → {out['status']}"
              + (f" ({out['r_result']:+.1f}R)" if out["r_result"] != "" else ""))

    res = pd.DataFrame(rows)[OUT_COLS]
    old = db.read_table(OUTCOMES_TABLE)  # keep rows for zones outside this run's filter
    if not old.empty and "zone_id" in old.columns:
        old = old[~old["zone_id"].isin(res["zone_id"])]
        if not old.empty:
            res = pd.concat([old.astype(str), res.astype(str)], ignore_index=True)
    # Canonical store = data/index.db (table `zone_outcome`); DB-only, no CSV mirror.
    db.write_table(OUTCOMES_TABLE, res)
    save_ledger(ledger)
    print(f"\n→ {OUTCOMES_CSV} ({len(res)} rows); ledger statuses updated")

    summarize(res)


if __name__ == "__main__":
    main()
