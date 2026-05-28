"""Phase 2 — EURUSD edge research. Measure, don't assume.

Tests, on 2023-04 → 2026 data:
  1. MACRO (the gate): does DGS2-ESTR differential 20d slope predict forward EUR direction?
     Compared against DXY slope and US-side-only (DGS2 level, DFII10) slopes.
  2. MTF structure: fractal HH/HL gate (scripts/structure.py) vs forward EUR direction.
  3. ATR compression: D1 ATR < 20d median → next-period expansion?
  4. Session timing: which UTC hours carry EUR range.
  5. Random directional baseline (no secular trend expected, unlike gold).

Run: .venv/bin/python -m scripts.research_eurusd
"""
import numpy as np
import pandas as pd
from scripts.structure import structure_state

FWD = 5  # forward D1 bars (~1 swing week)


def load_d1():
    df = pd.read_csv("data/twelvedata/eurusd/1day.csv", parse_dates=["datetime"]).sort_values("datetime")
    df = df[df.datetime.dt.dayofweek < 5].reset_index(drop=True)  # weekdays
    return df


def load_fred(sid):
    f = pd.read_csv(f"data/fred/{sid}.csv", parse_dates=["date"]).dropna()
    f["value"] = pd.to_numeric(f["value"], errors="coerce")
    return f.dropna()


def merge_series(d1, series_dict):
    """Forward-fill each FRED series onto D1 dates."""
    out = d1.copy()
    out["date"] = out.datetime.dt.normalize()
    for name, f in series_dict.items():
        f2 = f.rename(columns={"value": name}).copy()
        f2["date"] = f2.date.dt.normalize()
        out = pd.merge_asof(out.sort_values("date"), f2[["date", name]].sort_values("date"),
                            on="date", direction="backward")
    return out


def slope20(s):
    """20-row rolling linear slope."""
    return s.rolling(20).apply(lambda w: np.polyfit(range(len(w)), w.values, 1)[0], raw=False)


def macro_test(d1):
    dgs2 = load_fred("DGS2"); estr = load_fred("ECBESTRVOLWGTTRMDMNRT")
    dfii = load_fred("DFII10");
    dxy  = pd.read_csv("data/yahoo/DXY.csv", parse_dates=["date"]).dropna()
    dxy["value"] = pd.to_numeric(dxy["value"], errors="coerce")
    m = merge_series(d1, {"dgs2": dgs2, "estr": estr, "dfii": dfii, "dxy": dxy.dropna()})
    m["diff"] = m["dgs2"] - m["estr"]
    m["fwd_ret"] = m.close.shift(-FWD) / m.close - 1

    signals = {
        "DGS2-ESTR diff slope": slope20(m["diff"]),
        "DXY slope":            slope20(m["dxy"]),
        "DGS2 level slope":     slope20(m["dgs2"]),
        "DFII10 slope":         slope20(m["dfii"]),
    }
    print(f"\n=== MACRO: signal slope vs forward {FWD}d EUR return (N, hit%, edge vs 50) ===")
    print("Hypothesis: rising USD-rate signal → EUR bearish → fwd_ret < 0\n")
    print(f"{'signal':<24} {'N':>5} {'short_hit%':>10} {'long_hit%':>10} {'overall%':>9} {'edge_pp':>8}")
    for name, sl in signals.items():
        sub = pd.DataFrame({"sl": sl, "fwd": m["fwd_ret"]}).dropna()
        sub = sub[sub.sl != 0]
        if len(sub) < 30:
            print(f"{name:<24} insufficient ({len(sub)})"); continue
        # rising signal (sl>0) predicts EUR down; falling predicts up
        short = sub[sub.sl > 0]; longs = sub[sub.sl < 0]
        sh = (short.fwd < 0).mean() * 100 if len(short) else float("nan")
        lh = (longs.fwd > 0).mean() * 100 if len(longs) else float("nan")
        correct = ((sub.sl > 0) & (sub.fwd < 0)) | ((sub.sl < 0) & (sub.fwd > 0))
        overall = correct.mean() * 100
        print(f"{name:<24} {len(sub):>5} {sh:>10.1f} {lh:>10.1f} {overall:>9.1f} {overall-50:>+8.1f}")


def baseline(d1):
    r = (d1.close.shift(-FWD) / d1.close - 1).dropna()
    print(f"\n=== BASELINE: forward {FWD}d direction ===")
    print(f"  up%: {(r>0).mean()*100:.1f}  (N={len(r)})  — EUR directional bias")


def structure_test(d1):
    h4 = pd.read_csv("data/twelvedata/eurusd/4h.csv", parse_dates=["datetime"]).sort_values("datetime")
    h1 = pd.read_csv("data/twelvedata/eurusd/1h.csv", parse_dates=["datetime"]).sort_values("datetime")
    d1 = d1.copy(); d1["fwd_ret"] = d1.close.shift(-FWD) / d1.close - 1
    rows = []
    for _, r in d1.iterrows():
        ts = r.datetime
        h4h = h4[h4.datetime < ts].tail(60); h1h = h1[h1.datetime < ts].tail(60)
        if len(h4h) < 20 or len(h1h) < 20 or pd.isna(r.fwd_ret): continue
        s4 = structure_state(h4h); s1 = structure_state(h1h)
        rows.append((s4, s1, r.fwd_ret))
    df = pd.DataFrame(rows, columns=["s4", "s1", "fwd"])
    print(f"\n=== MTF STRUCTURE: state vs forward {FWD}d return ===")
    print(f"{'h4':>6} {'h1':>6} {'N':>5} {'up%':>6} {'avg_ret%':>9}")
    for (s4, s1), g in df.groupby(["s4", "s1"]):
        if len(g) < 15: continue
        print(f"{s4:>6} {s1:>6} {len(g):>5} {(g.fwd>0).mean()*100:>6.1f} {g.fwd.mean()*100:>9.3f}")
    # aligned-both vs random
    up = df[(df.s4=="up")&(df.s1=="up")]; dn = df[(df.s4=="down")&(df.s1=="down")]
    if len(up): print(f"  both-up  N={len(up):>4} up%={(up.fwd>0).mean()*100:.1f}")
    if len(dn): print(f"  both-down N={len(dn):>4} down%={(dn.fwd<0).mean()*100:.1f}")


def atr_compression(d1):
    def atr(df,p=14):
        tr=pd.concat([(df.high-df.low),(df.high-df.close.shift()).abs(),(df.low-df.close.shift()).abs()],axis=1).max(axis=1)
        return tr.rolling(p).mean()
    d=d1.copy(); d["atr"]=atr(d); d["med"]=d["atr"].rolling(20).median()
    d["compressed"]=d["atr"]<d["med"]
    d["fwd_range"]=(d.high.shift(-1).rolling(FWD).max() - d.low.shift(-1).rolling(FWD).min())
    d["exp"]=d["fwd_range"] > d["atr"]*1.5
    sub=d.dropna(subset=["compressed","exp"])
    c=sub[sub.compressed]; nc=sub[~sub.compressed]
    print(f"\n=== ATR COMPRESSION → expansion next {FWD}d ===")
    print(f"  compressed: N={len(c)} expand%={(c.exp).mean()*100:.1f}")
    print(f"  normal:     N={len(nc)} expand%={(nc.exp).mean()*100:.1f}")


def session(d1):
    h1 = pd.read_csv("data/twelvedata/eurusd/1h.csv", parse_dates=["datetime"]).sort_values("datetime")
    h1["rng"]=(h1.high-h1.low)*10000
    g=h1.groupby(h1.datetime.dt.hour)["rng"].mean()
    print(f"\n=== SESSION: avg H1 range (pips) by UTC hour ===")
    print("  " + "  ".join(f"{h:02d}:{v:.1f}" for h,v in g.items()))


if __name__ == "__main__":
    d1 = load_d1()
    print(f"EURUSD D1: {len(d1)} weekday bars, {d1.datetime.iloc[0].date()} → {d1.datetime.iloc[-1].date()}")
    baseline(d1)
    macro_test(d1)
    structure_test(d1)
    atr_compression(d1)
    session(d1)
