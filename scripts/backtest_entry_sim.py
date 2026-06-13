"""
Entry-confirmation (E0) Tier-2 entry simulation — the R/PF test Tier-1 couldn't see.

Tier-1 proved the 1H trigger adds no WIN-RATE edge. But E0's real payoff is fill-price → R: the
outward offset lets the limit sit beyond the wick, so a filled trade has a better entry, same SL
distance, and therefore higher R per win. This sim prices that.

Per setup (H1 oscillator-extreme TRANSITION bar, fade direction), three arms, identical SL distance
s = H1 ATR(14) and identical 2.5R target — only the ENTRY differs:

  MARKET        enter at the signal-bar close (no offset). Always fills.
  LIMIT-offset  place limit beyond the close by offset = s/3 (the mandated floor); fills only if a
                later bar pokes through within W_FILL bars (else MISSED — the cost of being patient).
  LIMIT+E0      same offset limit, but only taken when a 1H pin/engulf (the E0 trigger) is present
                at/just before the signal.

Outcome: walk forward ≤ MAX_HOLD bars from fill — first touch of SL (−1.0R) or TP (+2.5R); neither →
mark-to-market R at the horizon. PF = Σwins / |Σlosses|; expectancy = mean R over FILLED trades.
If LIMIT/​E0 PF & expectancy beat MARKET despite a lower fill-rate, the offset (and E0 as its gate)
earns its weight — even with equal win-rate.

Caveat: FX mean-reversion reading (oversold→long fade). xauusd E0 is continuation — read separately.
Scale-invariant in s, so the ATR multiplier only shifts fill-rate, not the cross-arm comparison.

Usage:
  bash scripts/pyrun.sh scripts/backtest_entry_sim.py --instrument all
  bash scripts/pyrun.sh scripts/backtest_entry_sim.py --instrument eurusd --out wiki/research/general/entry-sim-backtest.md
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from backtest_signals import (  # noqa: E402
    load_ohlc, atr, rsi, stoch_k, williams_r, keltner,
    pin_bull, pin_bear, bull_engulf, bear_engulf, REGISTERED,
)

W_FILL = 12       # bars a limit stays live before the setup is stale
MAX_HOLD = 48     # bars to resolve a filled trade (~2 trading days on H1)
TP_R = 2.5
OFFSET_FRAC = 1 / 3   # offset = s/3 (constitution floor)


def simulate(high, low, close, e, s, start, is_long):
    """Walk forward from bar `start` (already filled at price e, SL dist s). Return R."""
    if is_long:
        sl, tp = e - s, e + TP_R * s
    else:
        sl, tp = e + s, e - TP_R * s
    end = min(start + MAX_HOLD, len(close) - 1)
    for j in range(start + 1, end + 1):
        if is_long:
            if low[j] <= sl:
                return -1.0
            if high[j] >= tp:
                return TP_R
        else:
            if high[j] >= sl:
                return -1.0
            if low[j] <= tp:
                return TP_R
    last = close[end]
    return (last - e) / s if is_long else (e - last) / s


def run_pair(inst):
    fpath = ROOT / "data" / "twelvedata" / inst / "1h.csv"
    if not fpath.exists():
        return None
    df = load_ohlc(fpath)
    o, h, l, c = (df[x].values for x in ("open", "high", "low", "close"))
    s_arr = atr(df, 14).values
    r = rsi(df["close"], 14).values
    k = stoch_k(df).values
    wr = williams_r(df).values
    ku, kl = keltner(df)
    ku, kl = ku.values, kl.values

    oversold = (r < 35) | (k < 20) | (wr < -80) | (c < kl)
    overbought = (r > 65) | (k > 80) | (wr > -20) | (c > ku)
    btrig = (pin_bull(df) | bull_engulf(df)).values
    strig = (pin_bear(df) | bear_engulf(df)).values

    def trans(mask):  # fire only on entry INTO the extreme (de-cluster)
        out = mask.copy()
        out[1:] = mask[1:] & ~mask[:-1]
        out[0] = False
        return out

    setups = [("LONG", trans(oversold), btrig, True), ("SHORT", trans(overbought), strig, False)]
    arms = {a: [] for a in ("MARKET", "LIMIT", "LIMIT+E0")}
    n = len(c)

    for dirn, setup_mask, trig, is_long in setups:
        idx = np.where(setup_mask)[0]
        for i in idx:
            s = s_arr[i]
            if not np.isfinite(s) or s <= 0 or i + 1 >= n:
                continue
            # MARKET — enter at close[i]
            arms["MARKET"].append(simulate(h, l, c, c[i], s, i, is_long))
            # LIMIT-offset — limit beyond close by s/3, fill within W_FILL
            off = s * OFFSET_FRAC
            limit = c[i] - off if is_long else c[i] + off
            fill_bar = None
            for j in range(i + 1, min(i + 1 + W_FILL, n)):
                if (is_long and l[j] <= limit) or (not is_long and h[j] >= limit):
                    fill_bar = j
                    break
            if fill_bar is not None:
                R = simulate(h, l, c, limit, s, fill_bar, is_long)
                arms["LIMIT"].append(R)
                if trig[i] or trig[i - 1]:
                    arms["LIMIT+E0"].append(R)
    return arms, len(np.where(setups[0][1])[0]) + len(np.where(setups[1][1])[0])


def stats(rs):
    rs = np.array(rs, dtype=float)
    n = len(rs)
    if n == 0:
        return n, 0.0, 0.0, 0.0
    win = (rs > 0).mean() * 100
    wins, losses = rs[rs > 0].sum(), rs[rs < 0].sum()
    pf = wins / abs(losses) if losses < 0 else float("inf")
    return n, win, rs.mean(), pf


def fmt(inst, arms, n_setups):
    out = [f"\n{'='*66}", f"{inst.upper()} — Entry-Sim (H1, SL=ATR14, TP=2.5R, {n_setups} setups)",
           f"{'='*66}", f"{'arm':<11}{'N_fill':>8}{'fill%':>8}{'win%':>8}{'avgR':>9}{'PF':>8}"]
    out.append("-" * 66)
    base = len(arms["MARKET"])
    for a in ("MARKET", "LIMIT", "LIMIT+E0"):
        n, win, avg, pf = stats(arms[a])
        fillpct = n / base * 100 if base else 0
        pf_s = "inf" if pf == float("inf") else f"{pf:.2f}"
        out.append(f"{a:<11}{n:>8}{fillpct:>7.0f}%{win:>8.1f}{avg:>+9.3f}{pf_s:>8}")
    out.append("-" * 66)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", default="all")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    insts = list(REGISTERED) if args.instrument == "all" else [args.instrument]

    blocks = []
    for inst in insts:
        res = run_pair(inst)
        if res is None:
            print(f"  [{inst}] no H1 data")
            continue
        arms, n_setups = res
        b = fmt(inst, arms, n_setups)
        print(b)
        blocks.append(b)

    if args.out:
        p = ROOT / args.out
        p.parent.mkdir(parents=True, exist_ok=True)
        header = ("# Entry-Confirmation (E0) Tier-2 Entry Simulation\n\n"
                  "MARKET = enter at signal close. LIMIT = outward offset (s/3) limit, fills on a "
                  "poke within 12 bars. LIMIT+E0 = same, only when a 1H pin/engulf is present. "
                  "Same SL=H1 ATR14 and 2.5R target across arms — only entry price differs. "
                  "**If LIMIT / LIMIT+E0 beat MARKET on avgR & PF despite lower fill%, the offset "
                  "(and E0 gating it) earns its weight.** FX mean-rev reading; gold separate.\n")
        p.write_text(header + "\n```" + "\n".join(blocks) + "\n```\n")
        print(f"\n✅ wrote {p}")


if __name__ == "__main__":
    main()
