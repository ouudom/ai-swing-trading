"""X1 — empirically test whether G5 (VIX regime) and G6 (Asia-range compression)
add edge to the XAUUSD weekly-swing system.

The live confluence_criteria flags G5 (1.5 pts) and G6 (0.5 pts) as PROVISIONAL because
the backtest loader never modelled VIX or intraday Asia range. This script loads both,
runs the live-formula strategy (s_weekly_swing_v1), then for every executed trade tags
the VIX regime + Asia range AT ENTRY and compares outcome (avg R, PF, win%) across buckets.

If the G5/G6-favourable bucket clearly out-performs → the gates carry edge → keep weights.
If buckets are indistinguishable (or the sample is too small to tell) → demote to veto.

Run: .venv/bin/python scripts/sweep_g5g6.py
"""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.backtest import data as bt_data
from scripts.backtest.engine import Config
from scripts.backtest.strategies import s_weekly_swing_v1


def load_vix():
    df = pd.read_csv(ROOT / "data/fred/VIXCLS.csv", parse_dates=["date"]).dropna()
    return df.set_index("date")["value"].sort_index()


def asia_range(h1, entry_ts):
    """Asia session range $ for the trade day: 22:00 prior day → 07:00 entry day (UTC)."""
    day = pd.Timestamp(entry_ts).normalize()
    start = day - pd.Timedelta(hours=2)   # 22:00 prior day
    end = day + pd.Timedelta(hours=7)      # 07:00 entry day
    win = h1[(h1.index >= start) & (h1.index < end)]
    if len(win) < 4:
        return np.nan
    return float(win.high.max() - win.low.min())


def bucket_stats(label, trades):
    if not trades:
        return f"{label:<28} n=0"
    rs = np.array([t.r_mult for t in trades])
    pnls = np.array([t.pnl for t in trades])
    wins = pnls[pnls > 0].sum()
    losses = -pnls[pnls <= 0].sum()
    pf = wins / losses if losses > 0 else float("inf")
    wr = (pnls > 0).mean() * 100
    return (f"{label:<28} n={len(trades):<3} avgR={rs.mean():+.2f}  "
            f"win%={wr:>3.0f}  PF={pf:.2f}")


def main():
    cfg = Config()
    data = {tf: bt_data.load(tf) for tf in ("D1", "H4", "H1")}
    vix = load_vix()
    h1 = data["H1"]

    res = s_weekly_swing_v1(cfg, data)
    trades = res.trades
    print(f"\nBaseline s_weekly_swing_v1: {len(trades)} trades over "
          f"{(h1.index[-1]-h1.index[0]).days/365.25:.1f} yr "
          f"(~{len(trades)/((h1.index[-1]-h1.index[0]).days/365.25):.1f}/yr)\n")

    if not trades:
        print("No trades — cannot test G5/G6."); return

    # Tag each trade with VIX regime + Asia range at entry
    rows = []
    for t in trades:
        et = pd.Timestamp(t.entry_time)
        v = vix.reindex(vix.index.union([et.normalize()])).ffill().get(et.normalize(), np.nan)
        ar = asia_range(h1, et)
        rows.append({"trade": t, "vix": v, "asia": ar, "dir": t.direction, "r": t.r_mult})
    df = pd.DataFrame(rows)

    print("=== ALL TRADES ===")
    print(bucket_stats("all", list(df.trade)), "\n")

    print("=== G5 — VIX regime (at entry) ===")
    print(bucket_stats("VIX <18 (calm)",      list(df[df.vix < 18].trade)))
    print(bucket_stats("VIX 18-25 (mixed)",   list(df[(df.vix >= 18) & (df.vix <= 25)].trade)))
    print(bucket_stats("VIX >25 (risk-off)",  list(df[df.vix > 25].trade)))
    # live G5 idea: calm favours with-trend; >25 favours longs. Test longs in high VIX:
    print(bucket_stats("VIX>25 & LONG",        list(df[(df.vix > 25) & (df.dir > 0)].trade)))
    print(bucket_stats("VIX>25 & SHORT",       list(df[(df.vix > 25) & (df.dir < 0)].trade)))
    print()

    print("=== G6 — Asia range (at entry) ===")
    print(bucket_stats("Asia <$15 (compressed)", list(df[df.asia < 15].trade)))
    print(bucket_stats("Asia >=$15 (normal+)",   list(df[df.asia >= 15].trade)))
    print()

    print("=== G5+G6 favourable vs rest (live-aligned filter) ===")
    # favourable = Asia compressed AND not (VIX>35 short) — the live 'edge' claim
    fav = df[(df.asia < 15) & ~((df.vix > 35) & (df.dir < 0))]
    rest = df.drop(fav.index)
    print(bucket_stats("G5/G6 favourable", list(fav.trade)))
    print(bucket_stats("rest",             list(rest.trade)))
    print(f"\nNOTE: with n≈{len(trades)} total, sub-bucket sample sizes are tiny — read"
          f" differences as directional only, not significant.")


if __name__ == "__main__":
    main()
