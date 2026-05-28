"""Phase 0 — structure-param sweep for s_weekly_swing_v1 (XAUUSD).

Goal: find whether ANY objective structure-gate config yields positive expectancy
with a usable trade count (N>=30) over 2020-2026. If none does, the live method
(not just its parameters) is the problem — and EURUSD must not clone it.

Run: .venv/bin/python -m scripts.sweep_structure
"""
import itertools
from scripts.backtest.data import load
from scripts.backtest.engine import Config
from scripts.backtest.strategies import s_weekly_swing_v1

GRID = {
    "pivot_n":    [2, 3],
    "struct_win": [40, 60, 90, 120],
    "g1_mode":    ["both", "h4_only", "either"],
    "r_floor":    [1.8],
}


def stats(trades):
    n = len(trades)
    if n == 0:
        return n, 0.0, 0.0, 0.0, 0.0
    wins = [t for t in trades if t.pnl > 0]
    gross_win = sum(t.pnl for t in wins)
    gross_loss = -sum(t.pnl for t in trades if t.pnl <= 0)
    pf = (gross_win / gross_loss) if gross_loss > 0 else float("inf")
    win_pct = 100 * len(wins) / n
    total = sum(t.pnl for t in trades)
    avg_r = sum(t.r_mult for t in trades) / n
    return n, win_pct, total, avg_r, pf


def main():
    cfg = Config(initial=100_000.0, risk_pct=0.01, rr=2.5, be_r=1.5, cost=0.5)
    data = {tf: load(tf) for tf in ("D1", "H4", "H1")}
    print(f"Data: D1={len(data['D1'])} H4={len(data['H4'])} H1={len(data['H1'])} "
          f"({data['D1'].index[0].date()} → {data['D1'].index[-1].date()})\n")

    keys = list(GRID)
    rows = []
    for combo in itertools.product(*[GRID[k] for k in keys]):
        params = dict(zip(keys, combo))
        res = s_weekly_swing_v1(cfg, data, params=params)
        n, win, total, avg_r, pf = stats(res.trades)
        rows.append((params, n, win, total, avg_r, pf))

    rows.sort(key=lambda r: r[3], reverse=True)  # by total PnL
    hdr = f"{'n_piv':>5} {'win':>4} {'mode':>8} {'rflr':>4} | {'trades':>6} {'win%':>6} {'PnL$':>9} {'avgR':>6} {'PF':>5}"
    print(hdr)
    print("-" * len(hdr))
    for params, n, win, total, avg_r, pf in rows:
        pf_s = f"{pf:5.2f}" if pf != float("inf") else "  inf"
        print(f"{params['pivot_n']:>5} {params['struct_win']:>4} {params['g1_mode']:>8} "
              f"{params['r_floor']:>4} | {n:>6} {win:>6.1f} {total:>9.0f} {avg_r:>6.2f} {pf_s}")

    usable = [r for r in rows if r[1] >= 30 and r[3] > 0]
    print(f"\nConfigs with N>=30 AND positive PnL: {len(usable)}")
    for params, n, win, total, avg_r, pf in usable:
        print(f"  {params} → {n} trades, ${total:.0f}, avgR {avg_r:.2f}")


if __name__ == "__main__":
    main()
