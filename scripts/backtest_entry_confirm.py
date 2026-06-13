"""
Entry-confirmation (E0) conditional backtest — Tier 1 (D025 follow-up).

Question: E0 is the 1H trigger (pin / engulfing) fired AT a zone. It is NOT a standalone
directional signal (already tested weak as P1–P4). The real test is CONDITIONAL: given price is
already at an oscillator extreme (the fade setup the zone is built on), does requiring a confirming
reversal candle on the SAME 1H bar improve the forward outcome vs taking the extreme with no
trigger?

Universe (per direction, on H1 closed bars):
  LONG  setup = oversold   (RSI<35 OR Stoch<20 OR W%R<-80 OR close<Keltner-low)
  SHORT setup = overbought (RSI>65 OR Stoch>80 OR W%R>-20 OR close>Keltner-high)
Trigger (reversal toward the fade):
  LONG  = bullish pin (tail≥2.5×body) OR bullish engulfing
  SHORT = bearish pin OR bearish engulfing
Split the setup universe into TRIGGER vs NO-TRIGGER; win = fwd return in fade direction > 0 over
horizon H (H1 bars). Edge = win%(trigger) − win%(no-trigger); z = 2-proportion test. Positive,
significant z ⇒ E0 earns its confluence weight.

Caveat: this tests the FX MEAN-REVERSION reading of E0 (reversal against the approach). xauusd E0 is
CONTINUATION toward the zone — its row here is the mean-rev interpretation; read gold separately.
15M CHoCH leg NOT tested (data: only xauusd/usdjpy/gbpjpy hold deep 15M; majors keep ~recent only).

Usage:
  bash scripts/pyrun.sh scripts/backtest_entry_confirm.py --instrument all
  bash scripts/pyrun.sh scripts/backtest_entry_confirm.py --instrument eurusd --horizons 6 12 24
  bash scripts/pyrun.sh scripts/backtest_entry_confirm.py --instrument all --out wiki/research/general/entry-confirm-backtest.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

# reuse the vetted helpers — same definitions the signal scan used
from backtest_signals import (  # noqa: E402
    load_ohlc, rsi, stoch_k, williams_r, keltner,
    pin_bull, pin_bear, bull_engulf, bear_engulf, REGISTERED,
)

TF_FILE = "1h.csv"


def two_prop_z(w1, n1, w0, n0):
    """z for win-rate(trigger) vs win-rate(no-trigger), pooled."""
    if n1 == 0 or n0 == 0:
        return 0.0
    p1, p0 = w1 / n1, w0 / n0
    p = (w1 + w0) / (n1 + n0)
    se = np.sqrt(p * (1 - p) * (1 / n1 + 1 / n0))
    return (p1 - p0) / se if se > 0 else 0.0


def run_pair(inst, horizons):
    fpath = ROOT / "data" / "twelvedata" / inst / TF_FILE
    if not fpath.exists():
        return None
    df = load_ohlc(fpath)
    c = df["close"]
    r = rsi(c, 14)
    k = stoch_k(df)
    wr = williams_r(df)
    ku, kl = keltner(df)

    oversold = (r < 35) | (k < 20) | (wr < -80) | (c < kl)
    overbought = (r > 65) | (k > 80) | (wr > -20) | (c > ku)
    bull_trig = pin_bull(df) | bull_engulf(df)
    bear_trig = pin_bear(df) | bear_engulf(df)

    rows = []
    for H in horizons:
        fwd = (c.shift(-H) / c - 1).values
        valid = ~np.isnan(fwd)
        for dirn, setup, trig in (("LONG", oversold, bull_trig), ("SHORT", overbought, bear_trig)):
            su = setup.values & valid
            tr = su & trig.values
            nt = su & ~trig.values
            win = (fwd > 0) if dirn == "LONG" else (fwd < 0)
            w_tr, n_tr = int((win & tr).sum()), int(tr.sum())
            w_nt, n_nt = int((win & nt).sum()), int(nt.sum())
            if n_tr < 30 or n_nt < 30:
                rows.append((dirn, H, n_tr, n_nt, np.nan, np.nan, np.nan, 0.0, True))
                continue
            wp_tr, wp_nt = w_tr / n_tr * 100, w_nt / n_nt * 100
            z = two_prop_z(w_tr, n_tr, w_nt, n_nt)
            rows.append((dirn, H, n_tr, n_nt, wp_nt, wp_tr, wp_tr - wp_nt, z, False))
    return rows


def fmt(inst, rows):
    out = [f"\n{'='*70}", f"{inst.upper()} — Entry-Confirmation conditional test (H1)", f"{'='*70}"]
    out.append(f"{'dir':<5}{'H':>4}{'N_trig':>8}{'N_none':>8}{'win_none%':>11}{'win_trig%':>11}{'edge':>8}{'z':>7}")
    out.append("-" * 70)
    for dirn, H, n_tr, n_nt, wnt, wtr, edge, z, insuff in rows:
        if insuff:
            out.append(f"{dirn:<5}{H:>4}{n_tr:>8}{n_nt:>8}{'—':>11}{'—':>11}{'—':>8}{'INSUF':>7}")
        else:
            star = "**" if abs(z) >= 2.6 else "*" if abs(z) >= 2.0 else ""
            out.append(f"{dirn:<5}{H:>4}{n_tr:>8}{n_nt:>8}{wnt:>11.1f}{wtr:>11.1f}{edge:>+8.1f}{z:>7.2f} {star}")
    out.append("-" * 70)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", default="all")
    ap.add_argument("--horizons", nargs="+", type=int, default=[6, 12, 24],
                    help="forward windows in H1 bars (default 6=6h 12=12h 24=1d)")
    ap.add_argument("--out", default=None, help="write a markdown report to this path")
    args = ap.parse_args()

    insts = list(REGISTERED) if args.instrument == "all" else [args.instrument]
    blocks = []
    for inst in insts:
        rows = run_pair(inst, args.horizons)
        if rows is None:
            print(f"  [{inst}] no H1 data")
            continue
        b = fmt(inst, rows)
        print(b)
        blocks.append(b)

    if args.out:
        p = ROOT / args.out
        p.parent.mkdir(parents=True, exist_ok=True)
        header = ("# Entry-Confirmation (E0) Conditional Backtest — Tier 1\n\n"
                  "Edge = win%(setup WITH 1H pin/engulf trigger) − win%(setup, NO trigger). "
                  "Positive + |z|≥2 ⇒ the E0 trigger improves the fade outcome and earns its weight. "
                  "Setup = H1 oscillator extreme (RSI/Stoch/W%R/Keltner). FX mean-rev reading; gold E0 "
                  "is continuation (read separately). 15M CHoCH leg not tested (data-limited).\n")
        p.write_text(header + "\n```\n" + "\n".join(blocks) + "\n```\n")
        print(f"\n✅ wrote {p}")


if __name__ == "__main__":
    main()
