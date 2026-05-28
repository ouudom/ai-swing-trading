"""Phase 0 — entry-mechanism sweep. Tests the funnel-diagnosis fix:
the outward offset kills ~90% of triggered setups. Compare fill-at-trigger
vs a range of offset coefficients (0 = limit at zone extreme).

Run: .venv/bin/python -m scripts.sweep_entry
"""
from scripts.backtest.data import load
from scripts.backtest.engine import Config
from scripts.backtest.strategies import s_weekly_swing_v1
from scripts.sweep_structure import stats

ENTRIES = [
    ("trigger_fill", None),
    ("offset", 0.0),
    ("offset", 0.10),
    ("offset", 0.15),
    ("offset", 0.30),   # current live
]
G1_MODES = ["both", "either"]


def main():
    cfg = Config(initial=100_000.0, risk_pct=0.01, rr=2.5, be_r=1.5, cost=0.5)
    data = {tf: load(tf) for tf in ("D1", "H4", "H1")}
    print(f"Data {data['D1'].index[0].date()} → {data['D1'].index[-1].date()}\n")

    hdr = f"{'g1':>7} {'entry':>13} {'coef':>5} | {'trades':>6} {'win%':>6} {'PnL$':>9} {'avgR':>6} {'PF':>6} {'tr/yr':>6}"
    print(hdr); print("-" * len(hdr))
    rows = []
    for g1 in G1_MODES:
        for mode, coef in ENTRIES:
            params = {"pivot_n": 2, "struct_win": 60, "g1_mode": g1,
                      "r_floor": 1.8, "entry_mode": mode,
                      "offset_coef": coef if coef is not None else 0.3}
            res = s_weekly_swing_v1(cfg, data, params=params)
            n, win, total, avg_r, pf = stats(res.trades)
            rows.append((g1, mode, coef, n, win, total, avg_r, pf))

    for g1, mode, coef, n, win, total, avg_r, pf in rows:
        pf_s = f"{pf:6.2f}" if pf != float("inf") else "   inf"
        coef_s = "  -" if coef is None else f"{coef:.2f}"
        print(f"{g1:>7} {mode:>13} {coef_s:>5} | {n:>6} {win:>6.1f} {total:>9.0f} "
              f"{avg_r:>6.2f} {pf_s} {n/6.35:>6.1f}")

    print("\nUsable (N>=30 & PnL>0):")
    for g1, mode, coef, n, win, total, avg_r, pf in rows:
        if n >= 30 and total > 0:
            print(f"  g1={g1} {mode} coef={coef} → {n} trades, ${total:.0f}, "
                  f"avgR {avg_r:.2f}, PF {pf:.2f}")


if __name__ == "__main__":
    main()
