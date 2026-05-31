"""E5 — calibrate EURUSD provisional thresholds from 6.4yr research data.

Replaces placeholders in wiki/system/eurusd/{confluence_criteria,constitution_addendum}.md
with values DERIVED from the EUR distribution rather than copied/guessed from gold.

Outputs proposed values for:
  - G6 London/pre-NY (07–13 UTC) range cutoff for "compressed"
  - T3 D1 counter-move % trigger (rare 1-day reversal)
  - Weekend gap % thresholds (Fri close → Mon open)
  - V1b intraday invalidation buffer (pips past zone)
  - Confluence proximity tolerance (pips) for VP/pivot "near the extreme"
  - H4 trading-day ATR filter sanity (current 5 pips)

Run: .venv/bin/python scripts/calibrate_eurusd.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "data/research/eurusd"
PIP = 0.0001


def load(tf):
    return pd.read_csv(RES / f"{tf}.csv", parse_dates=["datetime"]).set_index("datetime").sort_index()


def pips(x):
    return x / PIP


def atr(df, n=14):
    h, l, c = df.high, df.low, df.close
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def pctiles(s, ps=(10, 25, 50, 75, 90, 95, 99)):
    return {p: round(float(np.nanpercentile(s, p)), 4) for p in ps}


def main():
    d1 = load("1day")
    h1 = load("1h")
    h4 = load("4h")
    yrs = (d1.index[-1] - d1.index[0]).days / 365.25
    print(f"EURUSD research sample: {d1.index[0].date()} → {d1.index[-1].date()} ({yrs:.1f}yr)\n")

    # ── G6 — London/pre-NY (07:00–13:00 UTC) hourly-window RANGE per day ──
    win = h1[(h1.index.hour >= 7) & (h1.index.hour < 13)].copy()
    win["d"] = win.index.date
    grp = win.groupby("d").agg(hi=("high", "max"), lo=("low", "min"))
    rng = pips(grp.hi - grp.lo).dropna()
    rp = pctiles(rng)
    print("── G6  London/pre-NY 07–13 UTC daily range (pips) ──")
    print(f"   median {rp[50]} | p25 {rp[25]} | p75 {rp[75]}")
    print(f"   → 'compressed' cutoff = p33 ≈ {round(float(np.nanpercentile(rng,33)),1)} pips "
          f"(placeholder was 30)\n")

    # ── G7 / ATR regime ──
    d1a = pips(atr(d1).dropna())
    print("── D1 ATR14 (pips) ──")
    print(f"   median {round(float(d1a.median()),1)} | mean {round(float(d1a.mean()),1)}\n")
    h4a = pips(atr(h4).dropna())
    print("── H4 ATR14 (pips) ── (trading-day filter sanity)")
    print(f"   median {round(float(h4a.median()),1)} | p10 {round(float(np.nanpercentile(h4a,10)),1)}")
    print(f"   → flatline filter 5 pips drops bottom "
          f"{round(float((pips(h4.high-h4.low) < 5).mean())*100,1)}% of H4 bars\n")

    # ── T3 — D1 counter-move % (rare 1-day reversal) ──
    dpct = (d1.close.pct_change().abs() * 100).dropna()
    dp = pctiles(dpct)
    print("── T3  D1 |% move| distribution ──")
    print(f"   median {dp[50]}% | p90 {dp[90]}% | p95 {dp[95]}% | p99 {dp[99]}%")
    print(f"   → counter-move trigger ≈ p97 = {round(float(np.nanpercentile(dpct,97)),2)}% "
          f"(placeholder was 1.2%)\n")

    # ── Weekend gap % (Fri close → next session open) ──
    d1r = d1.reset_index()
    d1r["wd"] = d1r.datetime.dt.weekday
    gaps = []
    for i in range(1, len(d1r)):
        prev, cur = d1r.iloc[i - 1], d1r.iloc[i]
        if (cur.datetime - prev.datetime).days >= 2:  # gap across weekend/holiday
            gaps.append(abs(cur.open / prev.close - 1) * 100)
    gaps = pd.Series(gaps)
    gp = pctiles(gaps)
    print("── Weekend/holiday gap |%| (Fri close → next open) ──")
    print(f"   median {gp[50]}% | p75 {gp[75]}% | p90 {gp[90]}% | p95 {gp[95]}% | p99 {gp[99]}%")
    print(f"   → tiers: NOTE>p50({gp[50]}%) WARN>p90({gp[90]}%) REFORECAST>p99({gp[99]}%)\n")

    # ── V1b buffer — intraday H4 noise past a level ──
    h4rng = pips(h4.high - h4.low).dropna()
    print("── V1b buffer — H4 bar range (pips), noise gauge ──")
    print(f"   median {round(float(h4rng.median()),1)} | p75 {round(float(np.nanpercentile(h4rng,75)),1)}")
    print(f"   → buffer ≈ 0.3×median H4 range = {round(float(h4rng.median())*0.3,1)} pips "
          f"(placeholder was 5)\n")

    # ── Confluence proximity tolerance — fraction of H4 ATR ──
    print("── Confluence 'near the extreme' tolerance ──")
    print(f"   0.5×median H4 ATR = {round(float(h4a.median())*0.5,1)} pips "
          f"→ suggested VP/pivot tolerance (placeholder 8)\n")


if __name__ == "__main__":
    main()
