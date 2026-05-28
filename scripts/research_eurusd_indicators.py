"""Phase 2e — which indicators form real confluence for EUR swing setups?

EUR gets its OWN confluence signals (not a copy of gold's 7). Scan candidate swing indicators
on 6.4yr daily; keep those with forward-edge, drop those without. Forward horizon 5 D1 bars.

Measures each signal's directional win% vs the 48.9% EUR baseline, avg fwd return, N.

Run: .venv/bin/python -m scripts.research_eurusd_indicators
"""
import numpy as np
import pandas as pd

FWD = 5
BASE = 48.9  # measured EUR up-rate


def load():
    d = pd.read_csv("data/research/eurusd/1day.csv", parse_dates=["datetime"]).sort_values("datetime")
    d = d[d.datetime.dt.dayofweek < 5].reset_index(drop=True)
    return d


def rsi(s, p=14):
    dlt = s.diff()
    up = dlt.clip(lower=0).rolling(p).mean()
    dn = (-dlt.clip(upper=0)).rolling(p).mean()
    return 100 - 100 / (1 + up / dn)


def atr(df, p=14):
    tr = pd.concat([(df.high - df.low), (df.high - df.close.shift()).abs(),
                    (df.low - df.close.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(p).mean()


def edge(d, mask, direction):
    """direction +1 expects up, -1 expects down. Report win% in expected direction."""
    sub = d[mask].dropna(subset=["fwd"])
    if len(sub) < 25:
        return f"N={len(sub):>4} (insufficient)"
    if direction > 0:
        win = (sub.fwd > 0).mean() * 100
    else:
        win = (sub.fwd < 0).mean() * 100
    avg = sub.fwd.mean() * 100 * direction
    return f"N={len(sub):>4}  win%={win:>5.1f}  edge={win-BASE:>+5.1f}pp  avg_fwd={avg:>+.3f}%"


def main():
    d = load()
    d["fwd"] = d.close.shift(-FWD) / d.close - 1
    d["rsi"] = rsi(d.close)
    d["atr"] = atr(d)
    d["ema50"] = d.close.ewm(span=50, adjust=False).mean()
    d["ema200"] = d.close.ewm(span=200, adjust=False).mean()
    d["sma20"] = d.close.rolling(20).mean()
    d["sd20"] = d.close.rolling(20).std()
    d["bb_lo"] = d.sma20 - 2 * d.sd20
    d["bb_hi"] = d.sma20 + 2 * d.sd20
    d["roll_lo20"] = d.low.rolling(20).min()
    d["roll_hi20"] = d.high.rolling(20).max()
    d["don_hi"] = d.high.rolling(20).max().shift(1)
    d["don_lo"] = d.low.rolling(20).min().shift(1)

    print(f"EUR D1 {d.datetime.iloc[0].date()}→{d.datetime.iloc[-1].date()}  baseline up%={BASE}\n")
    print("MEAN-REVERSION candidates (expect bounce):")
    print(f"  RSI<30 → long      {edge(d, d.rsi < 30, +1)}")
    print(f"  RSI>70 → short     {edge(d, d.rsi > 70, -1)}")
    print(f"  close<BB_lo → long {edge(d, d.close < d.bb_lo, +1)}")
    print(f"  close>BB_hi → short{edge(d, d.close > d.bb_hi, -1)}")
    print(f"  at 20d low → long  {edge(d, d.low <= d.roll_lo20 * 1.001, +1)}")
    print(f"  at 20d high → short{edge(d, d.high >= d.roll_hi20 * 0.999, -1)}")

    print("\nTREND / BREAKOUT candidates (expect continuation):")
    print(f"  EMA50>EMA200 → long  {edge(d, d.ema50 > d.ema200, +1)}")
    print(f"  EMA50<EMA200 → short {edge(d, d.ema50 < d.ema200, -1)}")
    print(f"  Donchian20 brk up    {edge(d, d.close > d.don_hi, +1)}")
    print(f"  Donchian20 brk dn    {edge(d, d.close < d.don_lo, -1)}")
    print(f"  close>EMA50 → long   {edge(d, d.close > d.ema50, +1)}")
    print(f"  close<EMA50 → short  {edge(d, d.close < d.ema50, -1)}")

    print("\nPullback-in-trend (trend + counter stretch):")
    up = d.ema50 > d.ema200
    print(f"  uptrend + RSI<40 → long  {edge(d, up & (d.rsi < 40), +1)}")
    dn = d.ema50 < d.ema200
    print(f"  downtrend + RSI>60 → short{edge(d, dn & (d.rsi > 60), -1)}")
    print(f"  uptrend + close<BB_mid    {edge(d, up & (d.close < d.sma20), +1)}")


if __name__ == "__main__":
    main()
