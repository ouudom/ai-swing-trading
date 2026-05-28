"""Phase 3 — backtest EUR NY-overlap large-move mean-reversion.

Candidate edge (6.4yr): fade the 12:00 UTC H1 bar when its move >= threshold pips.
Enter at 13:00 open opposite the move; exit at stop / target / 16:00 time-stop.

Sweeps move-threshold, stop, target. Reports trades/yr, win%, avg pips/trade, total,
profit factor, expectancy. Costs = spread (round-trip).

Run: .venv/bin/python -m scripts.backtest_eur_session
"""
import itertools
import numpy as np
import pandas as pd

PIP = 10000
SPREAD = 0.8  # round-trip pips


def load():
    h1 = pd.read_csv("data/research/eurusd/1h.csv", parse_dates=["datetime"]).sort_values("datetime")
    h1 = h1[h1.datetime.dt.dayofweek < 5].reset_index(drop=True)
    h1["day"] = h1.datetime.dt.normalize(); h1["hr"] = h1.datetime.dt.hour
    return h1


def run(h1, thresh, stop_p, target_p):
    """Fade 12:00 move>=thresh. Enter 13:00 open. Stop/target in pips, else exit 16:00 close.
    Intrabar path approximated on H1 bars 13:00-15:00 (stop checked before target if both hit)."""
    trades = []
    for day, g in h1.groupby("day"):
        b12 = g[g.hr == 12]
        if len(b12) == 0:
            continue
        mv = (b12.iloc[0].close - b12.iloc[0].open) * PIP
        if abs(mv) < thresh:
            continue
        sig = -np.sign(mv)  # fade
        entry_bars = g[(g.hr >= 13) & (g.hr <= 15)]
        exit_bar = g[g.hr == 16]
        if len(entry_bars) == 0 or len(exit_bar) == 0:
            continue
        entry = entry_bars.iloc[0].open
        stop_px = entry - sig * stop_p / PIP
        tgt_px = entry + sig * target_p / PIP
        result = None
        for _, b in entry_bars.iterrows():
            hit_stop = (b.low <= stop_px) if sig > 0 else (b.high >= stop_px)
            hit_tgt = (b.high >= tgt_px) if sig > 0 else (b.low <= tgt_px)
            if hit_stop and hit_tgt:
                result = -stop_p; break          # conservative: stop first
            if hit_stop:
                result = -stop_p; break
            if hit_tgt:
                result = target_p; break
        if result is None:
            result = (exit_bar.iloc[0].close - entry) * sig * PIP  # time-stop at 16:00
        trades.append(result - SPREAD)
    return pd.Series(trades)


def stats(r):
    if len(r) < 30:
        return None
    win = (r > 0).mean() * 100
    gw = r[r > 0].sum(); gl = -r[r <= 0].sum()
    pf = gw / gl if gl > 0 else float("inf")
    yrs = 6.4
    return dict(N=len(r), tr_yr=len(r) / yrs, win=win, avg=r.mean(),
                tot=r.sum(), pf=pf, sharpe=r.mean() / r.std())


if __name__ == "__main__":
    h1 = load()
    print(f"EUR H1 {h1.datetime.iloc[0].date()} → {h1.datetime.iloc[-1].date()}\n")
    print(f"{'thr':>4} {'stop':>5} {'tgt':>5} | {'N':>4} {'tr/yr':>6} {'win%':>5} {'avg_p':>6} {'tot_p':>7} {'PF':>5} {'shrp':>5}")
    print("-" * 62)
    rows = []
    for thresh, stop_p, target_p in itertools.product([20, 25, 30], [20, 30, 40], [20, 30, 40]):
        r = run(h1, thresh, stop_p, target_p)
        s = stats(r)
        if s:
            rows.append((thresh, stop_p, target_p, s))
    rows.sort(key=lambda x: x[3]["tot"], reverse=True)
    for thresh, stop_p, target_p, s in rows:
        pf = f"{s['pf']:.2f}" if s["pf"] != float("inf") else "inf"
        print(f"{thresh:>4} {stop_p:>5} {target_p:>5} | {s['N']:>4} {s['tr_yr']:>6.1f} "
              f"{s['win']:>5.1f} {s['avg']:>+6.2f} {s['tot']:>+7.0f} {pf:>5} {s['sharpe']:>+5.2f}")
