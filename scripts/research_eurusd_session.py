"""Phase 2b — EUR session-edge research. Pivot from the gold swing archetype.

Session timing was the only robust Phase-2 signal: EUR active 12-15 UTC (NY/London overlap),
London open 07-08, Asia dead. Test concrete session strategies on intraday 2023-now:

  H1  London-open breakout: Asia range (22:00 prior → 07:00) → break beyond extreme after
      07:00 continues into NY. Long on break>asia_high, short on break<asia_low.
  H2  Overlap continuation: sign of 12:00 UTC H1 bar → hold to 16:00.
  H3  Overlap fade (mean-reversion): fade the 12:00→13:00 move, revert by 16:00.

Reports win%, avg move (pips), expectancy. Spread cost ~0.8 pip assumed.

Run: .venv/bin/python -m scripts.research_eurusd_session
"""
import numpy as np
import pandas as pd

PIP = 10000
SPREAD = 0.8  # pips round-trip cost estimate


def load_h1():
    # Prefer merged research CSV (2020-now, HistData+TD) over live TD-only (2023-now).
    import os
    path = "data/research/eurusd/1h.csv" if os.path.exists("data/research/eurusd/1h.csv") \
        else "data/twelvedata/eurusd/1h.csv"
    h1 = pd.read_csv(path, parse_dates=["datetime"]).sort_values("datetime")
    h1 = h1[h1.datetime.dt.dayofweek < 5].reset_index(drop=True)
    return h1


def london_breakout(h1):
    """Per trading day: Asia range = 22:00(prev)→07:00. After 07:00, first H1 close beyond
    Asia extreme = entry. Exit at 16:00 UTC same day. Stop = opposite Asia extreme."""
    h1 = h1.copy()
    h1["day"] = h1.datetime.dt.normalize()
    results = []
    for day, _ in h1.groupby("day"):
        asia_start = day - pd.Timedelta(hours=2)
        asia = h1[(h1.datetime >= asia_start) & (h1.datetime < day + pd.Timedelta(hours=7))]
        if len(asia) < 5:
            continue
        a_hi, a_lo = asia.high.max(), asia.low.min()
        sess = h1[(h1.datetime >= day + pd.Timedelta(hours=7)) & (h1.datetime < day + pd.Timedelta(hours=16))]
        if len(sess) < 3:
            continue
        entry = direction = None
        for _, b in sess.iterrows():
            if entry is None:
                if b.close > a_hi:
                    entry, direction, etime = b.close, 1, b.datetime
                elif b.close < a_lo:
                    entry, direction, etime = b.close, -1, b.datetime
        if entry is None:
            continue
        exit_px = sess.iloc[-1].close
        move = (exit_px - entry) * direction * PIP - SPREAD
        results.append(move)
    r = pd.Series(results)
    return r


def overlap_continuation(h1, fade=False):
    """At 12:00 UTC H1: sign of that bar (close-open). Enter same(or opposite if fade) direction
    at 13:00 open, exit 16:00 close."""
    h1 = h1.copy(); h1["day"] = h1.datetime.dt.normalize(); h1["hr"] = h1.datetime.dt.hour
    results = []
    for day, g in h1.groupby("day"):
        b12 = g[g.hr == 12]; b13 = g[g.hr == 13]; b16 = g[g.hr == 16]
        if len(b12) == 0 or len(b13) == 0 or len(b16) == 0:
            continue
        sig = np.sign(b12.iloc[0].close - b12.iloc[0].open)
        if sig == 0:
            continue
        direction = -sig if fade else sig
        entry = b13.iloc[0].open; exit_px = b16.iloc[0].close
        move = (exit_px - entry) * direction * PIP - SPREAD
        results.append(move)
    return pd.Series(results)


def report(name, r):
    if len(r) < 30:
        print(f"{name}: insufficient N={len(r)}"); return
    win = (r > 0).mean() * 100
    print(f"{name:<28} N={len(r):>4} win%={win:>5.1f} avg={r.mean():>+6.2f}p "
          f"med={r.median():>+6.2f}p tot={r.sum():>+8.0f}p sharpe={r.mean()/r.std():>+5.2f}")


if __name__ == "__main__":
    h1 = load_h1()
    print(f"EUR H1: {len(h1)} bars {h1.datetime.iloc[0].date()} → {h1.datetime.iloc[-1].date()}\n")
    report("London breakout (07→16)", london_breakout(h1))
    report("Overlap continuation (12→16)", overlap_continuation(h1, fade=False))
    report("Overlap fade (12→16)", overlap_continuation(h1, fade=True))
