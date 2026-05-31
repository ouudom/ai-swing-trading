"""Entry-confirmation research — does the H1 trigger add edge?

The system gates WATCH→ORDER LIMIT on an H1 trigger (pin/engulf/B&R), but that
gate has never been ablation-tested. This crosses trigger_mode × entry_mode to
isolate the trigger's contribution from the outward-offset's contribution.

  trigger_mode: none (any in-zone bar) | pin | engulf | pin_or_engulf
  entry_mode:   trigger_fill (fill at bar close) | offset (limit beyond zone)

Read: hold entry_mode fixed, vary trigger_mode → does requiring confirmation help?
      hold trigger_mode fixed, vary entry_mode → is offset still load-bearing?

Run: .venv/bin/python -m scripts.sweep_trigger
"""
from scripts.backtest.data import load
from scripts.backtest.engine import Config
from scripts.backtest.strategies import s_weekly_swing_v1
from scripts.sweep_structure import stats

TRIGGERS = ["none", "pin", "engulf", "pin_or_engulf"]
ENTRIES = [("trigger_fill", None), ("offset", 0.15), ("offset", 0.25)]
YEARS = 6.35


def main():
    cfg = Config(initial=100_000.0, risk_pct=0.01, rr=2.5, be_r=1.5, cost=0.5)
    data = {tf: load(tf) for tf in ("D1", "H4", "H1")}
    print(f"Data {data['D1'].index[0].date()} → {data['D1'].index[-1].date()}\n")

    hdr = (f"{'trigger':>14} {'entry':>13} {'coef':>5} | {'N':>4} {'win%':>6} "
           f"{'PnL$':>9} {'avgR':>6} {'PF':>6} {'tr/yr':>6}")
    print(hdr); print("-" * len(hdr))
    for tm in TRIGGERS:
        for mode, coef in ENTRIES:
            params = {"pivot_n": 2, "struct_win": 60, "g1_mode": "either",
                      "trigger_mode": tm, "entry_mode": mode,
                      "offset_coef": coef if coef is not None else 0.25}
            res = s_weekly_swing_v1(cfg, data, params=params)
            n, win, total, avg_r, pf = stats(res.trades)
            pf_s = f"{pf:6.2f}" if pf != float("inf") else "   inf"
            coef_s = "  -" if coef is None else f"{coef:.2f}"
            print(f"{tm:>14} {mode:>13} {coef_s:>5} | {n:>4} {win:>6.1f} "
                  f"{total:>9.0f} {avg_r:>6.2f} {pf_s} {n/YEARS:>6.1f}")
        print()


if __name__ == "__main__":
    main()
