"""
E0 trigger bake-off — is there a better entry-confirmation than 1H pin/engulf? (D025 follow-up)

Tier-2 showed offset-LIMIT entry + the pin/engulf E0 gate lifts per-trade R. This asks: swap the
GATE for other reversal definitions, hold everything else identical (same extreme universe, same
s/3 offset limit, same SL=ATR / 2.5R sim), and compare avgR / PF / fill% per trigger. The winner is
the trigger that buys the most R per trade without collapsing fill-rate.

Triggers (long side at oversold; short = mirror), evaluated at the signal bar i:
  pin_engulf   1H bullish pin (tail≥2.5×body) OR bullish engulfing      ← CURRENT E0
  rsi_reclaim  RSI crosses back UP through 35 (momentum turn out of OS)
  stoch_reclaim Stoch K crosses back up through 20
  band_reclaim close re-enters above Keltner-low (was below)            ← "back inside band"
  micro_bos    close > prior bar HIGH (1H micro break-of-structure up)
  close_strong close in top third of bar range (rejection without full pin)
  any_combo    union of all of the above

Baselines for context: MARKET (signal close, no offset), LIMIT_all (offset limit, no trigger gate).
FX mean-reversion reading; xauusd & usdjpy excluded from the POOLED row (fade model wrong there) but
shown per-pair. R is normalized (units of SL) so pooling across pairs is valid.

Usage:
  bash scripts/pyrun.sh scripts/backtest_e0_variants.py
  bash scripts/pyrun.sh scripts/backtest_e0_variants.py --out wiki/research/general/e0-variants-backtest.md
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
import backtest_entry_sim as bes  # noqa: E402
from backtest_entry_sim import simulate, OFFSET_FRAC  # noqa: E402

TRIGGERS = ["pin_engulf", "rsi_reclaim", "stoch_reclaim", "band_reclaim",
            "micro_bos", "close_strong", "any_combo"]
POOL_EXCLUDE = {"xauusd", "usdjpy"}   # fade model does not apply
# per-TF windows (bars): H1 baseline; 15M = ×4 to hold wall-clock equal (4 bars/hr)
TF_CFG = {
    "H1":  {"file": "1h.csv",    "w_fill": 12, "t_trig": 6,  "max_hold": 48},
    "15M": {"file": "15min.csv", "w_fill": 48, "t_trig": 24, "max_hold": 192},
}
# 15M usable depth only on these (others keep ~recent only → excluded automatically by row count)
MIN_BARS = 5000


def build_triggers(df):
    """Return dict name -> (long_mask, short_mask) boolean np arrays."""
    o, h, l, c = (df[x].values for x in ("open", "high", "low", "close"))
    r = rsi(df["close"], 14).values
    k = stoch_k(df).values
    ku, kl = keltner(df); ku, kl = ku.values, kl.values
    rng = np.where((h - l) > 0, h - l, np.nan)

    def prev(a):
        p = np.empty_like(a); p[0] = np.nan; p[1:] = a[:-1]; return p

    pe_l = (pin_bull(df) | bull_engulf(df)).values
    pe_s = (pin_bear(df) | bear_engulf(df)).values
    rsi_l = (r >= 35) & (prev(r) < 35);          rsi_s = (r <= 65) & (prev(r) > 65)
    st_l = (k >= 20) & (prev(k) < 20);           st_s = (k <= 80) & (prev(k) > 80)
    bnd_l = (c >= kl) & (prev(c) < prev(kl));     bnd_s = (c <= ku) & (prev(c) > prev(ku))
    bos_l = c > prev(h);                          bos_s = c < prev(l)
    cs_l = (c - l) / rng >= 0.66;                 cs_s = (h - c) / rng >= 0.66

    t = {
        "pin_engulf":   (pe_l, pe_s),
        "rsi_reclaim":  (rsi_l, rsi_s),
        "stoch_reclaim":(st_l, st_s),
        "band_reclaim": (bnd_l, bnd_s),
        "micro_bos":    (bos_l, bos_s),
        "close_strong": (cs_l, cs_s),
    }
    t["any_combo"] = (np.logical_or.reduce([t[n][0] for n in t]),
                      np.logical_or.reduce([t[n][1] for n in t]))
    # nan→False
    return {n: (np.nan_to_num(a).astype(bool), np.nan_to_num(b).astype(bool)) for n, (a, b) in t.items()}


def run_pair(inst, tf="H1"):
    cfg = TF_CFG[tf]
    W_FILL, T_TRIG = cfg["w_fill"], cfg["t_trig"]
    bes.MAX_HOLD = cfg["max_hold"]   # simulate() reads this module global
    fpath = ROOT / "data" / "twelvedata" / inst / cfg["file"]
    if not fpath.exists():
        return None
    df = load_ohlc(fpath)
    if len(df) < MIN_BARS:
        return "THIN"
    o, h, l, c = (df[x].values for x in ("open", "high", "low", "close"))
    s_arr = atr(df, 14).values
    r = rsi(df["close"], 14).values
    k = stoch_k(df).values
    wr = williams_r(df).values
    ku, kl = keltner(df); ku, kl = ku.values, kl.values
    oversold = (r < 35) | (k < 20) | (wr < -80) | (c < kl)
    overbought = (r > 65) | (k > 80) | (wr > -20) | (c > ku)
    trig = build_triggers(df)
    n = len(c)

    def trans(m):
        out = m.copy(); out[1:] = m[1:] & ~m[:-1]; out[0] = False; return out

    buckets = {a: [] for a in (["MARKET", "LIMIT_all"] + TRIGGERS)}
    for dirn, setup, is_long, side in (("LONG", trans(oversold), True, 0),
                                       ("SHORT", trans(overbought), False, 1)):
        for i in np.where(setup)[0]:
            s = s_arr[i]
            if not np.isfinite(s) or s <= 0 or i + 1 >= n:
                continue
            off = s * OFFSET_FRAC
            # baselines anchored at the extreme bar i
            buckets["MARKET"].append(simulate(h, l, c, c[i], s, i, is_long))
            lim_i = c[i] - off if is_long else c[i] + off
            f = next((j for j in range(i + 1, min(i + 1 + W_FILL, n))
                      if (is_long and l[j] <= lim_i) or (not is_long and h[j] >= lim_i)), None)
            if f is not None:
                buckets["LIMIT_all"].append(simulate(h, l, c, lim_i, s, f, is_long))
            # trigger arms: confirm-then-enter — find first trigger bar t in [i, i+T_TRIG],
            # anchor the offset limit at t's close, fill within W_FILL after t
            for name in TRIGGERS:
                tmask = trig[name][side]
                t = next((u for u in range(i, min(i + 1 + T_TRIG, n)) if tmask[u]), None)
                if t is None or t + 1 >= n:
                    continue
                lim = c[t] - off if is_long else c[t] + off
                ft = next((j for j in range(t + 1, min(t + 1 + W_FILL, n))
                           if (is_long and l[j] <= lim) or (not is_long and h[j] >= lim)), None)
                if ft is not None:
                    buckets[name].append(simulate(h, l, c, lim, s, ft, is_long))
    return buckets


def stat(rs):
    rs = np.array(rs, float)
    if len(rs) == 0:
        return 0, 0.0, 0.0, 0.0
    wins, losses = rs[rs > 0].sum(), rs[rs < 0].sum()
    pf = wins / abs(losses) if losses < 0 else float("inf")
    return len(rs), (rs > 0).mean() * 100, rs.mean(), pf


def fmt(title, buckets, base_n):
    out = [f"\n{'='*64}", title, f"{'='*64}",
           f"{'gate':<14}{'N':>7}{'fill%':>7}{'win%':>8}{'avgR':>9}{'PF':>8}", "-" * 64]
    for a in (["MARKET", "LIMIT_all"] + TRIGGERS):
        n, win, avg, pf = stat(buckets[a])
        fp = n / base_n * 100 if base_n else 0
        pf_s = "inf" if pf == float("inf") else f"{pf:.2f}"
        tag = "  ← current" if a == "pin_engulf" else ""
        out.append(f"{a:<14}{n:>7}{fp:>6.0f}%{win:>8.1f}{avg:>+9.3f}{pf_s:>8}{tag}")
    out.append("-" * 64)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--instrument", default="all")
    ap.add_argument("--tf", default="H1", choices=["H1", "15M"])
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    insts = list(REGISTERED) if args.instrument == "all" else [args.instrument]

    pooled = {a: [] for a in (["MARKET", "LIMIT_all"] + TRIGGERS)}
    blocks = []
    thin = []
    for inst in insts:
        b = run_pair(inst, args.tf)
        if b is None:
            continue
        if b == "THIN":
            thin.append(inst); continue
        blocks.append(fmt(f"{inst.upper()} [{args.tf}]", b, len(b["MARKET"])))
        if inst not in POOL_EXCLUDE:
            for a in pooled:
                pooled[a] += b[a]
    pool_block = fmt(f"POOLED [{args.tf}] — FX mean-rev (excl xauusd, usdjpy)", pooled, len(pooled["MARKET"]))
    print(pool_block)
    for blk in blocks:
        print(blk)
    if thin:
        print(f"\n(skipped — <{MIN_BARS} {args.tf} bars: {', '.join(thin)})")

    if args.out:
        p = ROOT / args.out
        p.parent.mkdir(parents=True, exist_ok=True)
        header = ("# E0 Trigger Bake-Off — is there a better entry confirmation?\n\n"
                  "Identical Tier-2 sim (oscillator-extreme universe, s/3 offset limit, SL=ATR, "
                  "2.5R); only the GATE changes. Compare avgR / PF / fill% per trigger vs the current "
                  "pin/engulf E0 and the un-gated LIMIT_all. Higher avgR at usable fill% = better E0. "
                  "FX mean-rev reading; xauusd & usdjpy excluded from POOLED.\n")
        p.write_text(header + "\n```" + pool_block + "\n" + "\n".join(blocks) + "\n```\n")
        print(f"\n✅ wrote {p}")


if __name__ == "__main__":
    main()
