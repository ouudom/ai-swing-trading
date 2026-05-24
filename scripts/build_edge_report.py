#!/usr/bin/env python3
"""
Build XAUUSD Edge Report — computes all trading edge metrics and generates
a self-contained interactive HTML report.
"""
import json
import math
import os
import sys
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

BASE = "/Users/vuthyouthdom/projects/trading/swing-trading"
OUT_HTML = os.path.join(BASE, "frontend", "edge_report.html")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def load_ohlc(path):
    df = pd.read_csv(path, parse_dates=["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)
    for c in ["open", "high", "low", "close"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def load_fred(path):
    df = pd.read_csv(path, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df

def atr(df, period=14):
    h = df["high"]
    l = df["low"]
    pc = df["close"].shift(1)
    tr = pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)
    return tr.rolling(period, min_periods=period).mean()

def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def ema_slope(series, span, diff_period=5):
    e = ema(series, span)
    return e.diff(diff_period) / e.shift(diff_period)

def safe(x):
    """Convert numpy scalars to Python native for JSON serialization."""
    if isinstance(x, (np.floating, np.integer)):
        return float(x) if not np.isnan(x) else None
    if isinstance(x, float) and math.isnan(x):
        return None
    return x

def to_js(obj):
    return json.dumps(obj, default=lambda o: float(o) if isinstance(o, (np.floating, np.integer)) else str(o))

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
print("Loading OHLC data...")
d1  = load_ohlc(os.path.join(BASE, "data/twelvedata/xauusd/1day.csv"))
h4  = load_ohlc(os.path.join(BASE, "data/twelvedata/xauusd/4h.csv"))
h1  = load_ohlc(os.path.join(BASE, "data/twelvedata/xauusd/1h.csv"))
m15 = load_ohlc(os.path.join(BASE, "data/twelvedata/xauusd/15min.csv"))

print(f"  D1: {len(d1)} rows | H4: {len(h4)} rows | H1: {len(h1)} rows | 15m: {len(m15)} rows")

print("Loading FRED data...")
fred_dfii = load_fred(os.path.join(BASE, "data/fred/DFII10.csv"))
fred_dxy  = load_fred(os.path.join(BASE, "data/fred/DTWEXBGS.csv"))
fred_vix  = load_fred(os.path.join(BASE, "data/fred/VIXCLS.csv"))
fred_oil  = load_fred(os.path.join(BASE, "data/fred/DCOILWTICO.csv"))
fred_dff  = load_fred(os.path.join(BASE, "data/fred/DFF.csv"))

# ---------------------------------------------------------------------------
# PART 1: System Validation
# ---------------------------------------------------------------------------
print("\n[Part 1] System Validation...")

# --- 1a. MTF trend alignment win rate ---
print("  Computing MTF alignment...")

# Build per-bar slopes for H1
h1 = h1.copy()
h1["ema20"] = ema(h1["close"], 20)
h1["slope_h1"] = ema_slope(h1["close"], 20)

# Aggregate H4 EMA slope → merge onto H1
h4c = h4.copy()
h4c["ema20"] = ema(h4c["close"], 20)
h4c["slope_h4"] = ema_slope(h4c["close"], 20)
h4c["dt_h4"] = h4c["datetime"]
# forward-fill H4 slope onto H1 timestamps
h4c_slim = h4c[["datetime", "slope_h4"]].dropna()

# D1 EMA slope → forward-fill onto H1
d1c = d1.copy()
d1c["ema20"] = ema(d1c["close"], 20)
d1c["slope_d1"] = ema_slope(d1c["close"], 20)
d1c_slim = d1c[["datetime", "slope_d1"]].dropna()

# merge-asof
h1 = h1.sort_values("datetime").reset_index(drop=True)
h4c_slim = h4c_slim.sort_values("datetime").reset_index(drop=True)
d1c_slim = d1c_slim.sort_values("datetime").reset_index(drop=True)

h1 = pd.merge_asof(h1, h4c_slim, on="datetime", direction="backward")
h1 = pd.merge_asof(h1, d1c_slim, on="datetime", direction="backward")

# forward return over next 24 H1 bars (~24 hrs)
fwd_bars = 24
h1["ret_24h"] = h1["close"].shift(-fwd_bars) / h1["close"] - 1

def align_label(row):
    s1 = row["slope_h1"]
    s4 = row["slope_h4"]
    sd = row["slope_d1"]
    if pd.isna(s1) or pd.isna(s4) or pd.isna(sd):
        return "Unknown"
    if s1 > 0 and s4 > 0 and sd > 0:
        return "All Bullish"
    if s1 < 0 and s4 < 0 and sd < 0:
        return "All Bearish"
    if s1 > 0 and s4 > 0:
        return "H1+H4 Bull"
    if s1 < 0 and s4 < 0:
        return "H1+H4 Bear"
    return "Mixed"

h1["alignment"] = h1.apply(align_label, axis=1)

mtf_rows = []
overall_pct = (h1["ret_24h"].dropna() > 0).mean()
for label in ["All Bullish", "All Bearish", "H1+H4 Bull", "H1+H4 Bear", "Mixed"]:
    sub = h1[h1["alignment"] == label]["ret_24h"].dropna()
    if len(sub) < 10:
        continue
    win_rate = (sub > 0).mean()
    avg_ret  = sub.mean()
    mtf_rows.append({
        "label": label,
        "n": int(len(sub)),
        "win_rate": round(float(win_rate) * 100, 1),
        "avg_ret_pct": round(float(avg_ret) * 100, 3),
        "vs_random": round((float(win_rate) - float(overall_pct)) * 100, 1)
    })

print(f"    MTF rows: {len(mtf_rows)}")

# --- 1b. ATR stop adequacy ---
print("  Computing ATR stop adequacy...")

h4c = h4.copy()
h4c["atr14"] = atr(h4c, 14)
d1c = d1.copy()
d1c["atr14_d1"] = atr(d1c, 14)
d1c_atr = d1c[["datetime", "atr14_d1"]].dropna()

h4c = pd.merge_asof(
    h4c.sort_values("datetime"),
    d1c_atr.sort_values("datetime"),
    on="datetime", direction="backward"
)
h4c["risk_unit"] = h4c[["atr14", "atr14_d1"]].apply(
    lambda r: min(r["atr14"], 0.5 * r["atr14_d1"]) if pd.notna(r["atr14"]) and pd.notna(r["atr14_d1"]) else np.nan,
    axis=1
)
h4c = h4c.dropna(subset=["risk_unit"]).reset_index(drop=True)

look_forward = 10
multiples = [1.0, 1.5, 2.0]
exceed_counts = {m: 0 for m in multiples}
total_valid = 0

close_arr = h4c["close"].values
high_arr  = h4c["high"].values
low_arr   = h4c["low"].values
ru_arr    = h4c["risk_unit"].values

for i in range(len(h4c) - look_forward):
    ru = ru_arr[i]
    if ru <= 0 or np.isnan(ru):
        continue
    entry = close_arr[i]
    total_valid += 1
    # worst adverse excursion: max move against entry in either direction
    future_highs = high_arr[i+1:i+1+look_forward]
    future_lows  = low_arr[i+1:i+1+look_forward]
    mae_up   = np.max(future_highs) - entry  # adverse for short
    mae_down = entry - np.min(future_lows)   # adverse for long
    # use the larger of long/short MAE (symmetrical test)
    mae = max(mae_up, mae_down)
    for m in multiples:
        if mae > m * ru:
            exceed_counts[m] += 1

atr_adequacy = {
    "look_forward_bars": look_forward,
    "total": total_valid,
    "exceed_1R_pct": round(exceed_counts[1.0] / total_valid * 100, 1) if total_valid else 0,
    "exceed_1_5R_pct": round(exceed_counts[1.5] / total_valid * 100, 1) if total_valid else 0,
    "exceed_2R_pct": round(exceed_counts[2.0] / total_valid * 100, 1) if total_valid else 0,
}
print(f"    ATR adequacy computed over {total_valid} bars")

# --- 1c. 3R reachability ---
print("  Computing 3R reachability...")

hits_tp = 0
hits_sl = 0
bars_to_res = []
tp_bars = []
sl_bars = []

for i in range(len(h4c) - 80):
    ru = ru_arr[i]
    if ru <= 0 or np.isnan(ru):
        continue
    entry = close_arr[i]
    # test both long and short
    for direction in [1, -1]:
        sl_price = entry - direction * ru
        tp_price = entry + direction * 3 * ru
        resolved = False
        for j in range(1, 81):
            if i + j >= len(h4c):
                break
            hi = high_arr[i + j]
            lo = low_arr[i + j]
            if direction == 1:
                if lo <= sl_price:
                    hits_sl += 1
                    bars_to_res.append(j)
                    sl_bars.append(j)
                    resolved = True
                    break
                if hi >= tp_price:
                    hits_tp += 1
                    bars_to_res.append(j)
                    tp_bars.append(j)
                    resolved = True
                    break
            else:
                if hi >= sl_price:
                    hits_sl += 1
                    bars_to_res.append(j)
                    sl_bars.append(j)
                    resolved = True
                    break
                if lo <= tp_price:
                    hits_tp += 1
                    bars_to_res.append(j)
                    tp_bars.append(j)
                    resolved = True
                    break

total_3r = hits_tp + hits_sl
three_r_data = {
    "hits_tp": hits_tp,
    "hits_sl": hits_sl,
    "total_resolved": total_3r,
    "tp_pct": round(hits_tp / total_3r * 100, 1) if total_3r else 0,
    "sl_pct": round(hits_sl / total_3r * 100, 1) if total_3r else 0,
    "avg_bars_tp": round(float(np.mean(tp_bars)), 1) if tp_bars else 0,
    "avg_bars_sl": round(float(np.mean(sl_bars)), 1) if sl_bars else 0,
}
print(f"    3R: TP={hits_tp} SL={hits_sl} ({three_r_data['tp_pct']}% TP rate)")

# ---------------------------------------------------------------------------
# PART 2: Macro Regime Analysis
# ---------------------------------------------------------------------------
print("\n[Part 2] Macro Regimes...")

# Merge D1 OHLC with FRED data (on date string)
d1w = d1.copy()
d1w["date"] = d1w["datetime"].dt.date.astype(str)
d1w["ret"] = d1w["close"].pct_change()
d1w["ret_weekly"] = d1w["close"].pct_change(5)

def merge_fred(d1_df, fred_df, col_name, ffill_limit=10):
    # Create date range index
    all_dates = pd.DataFrame({"date": pd.date_range(fred_df["date"].min(), d1_df["datetime"].max(), freq="D").strftime("%Y-%m-%d")})
    fred_m = fred_df.copy()
    fred_m["date"] = fred_m["date"].dt.strftime("%Y-%m-%d")
    merged = all_dates.merge(fred_m, on="date", how="left")
    merged["value"] = merged["value"].ffill(limit=ffill_limit)
    merged = merged.rename(columns={"value": col_name})
    return d1_df.merge(merged, on="date", how="left")

d1w = merge_fred(d1w, fred_dfii, "dfii10")
d1w = merge_fred(d1w, fred_dxy,  "dxy")
d1w = merge_fred(d1w, fred_vix,  "vix")
d1w = merge_fred(d1w, fred_dff,  "dff")

# --- 2a. Real yield regime ---
print("  Real yield regimes...")
d1w["dfii10_slope"] = d1w["dfii10"].rolling(20).mean().diff()
d1w["yield_regime"] = d1w["dfii10_slope"].apply(
    lambda x: "Rising" if x > 0 else ("Falling" if x < 0 else "Flat") if pd.notna(x) else np.nan
)

yield_regime_data = []
for regime in ["Rising", "Falling"]:
    sub = d1w[d1w["yield_regime"] == regime]["ret_weekly"].dropna()
    if len(sub) < 10:
        continue
    mean_r = float(sub.mean()) * 100
    std_r  = float(sub.std()) * 100
    sharpe = mean_r / std_r if std_r > 0 else 0
    # max drawdown from equity curve
    equity = (1 + sub).cumprod()
    rolling_max = equity.cummax()
    dd = (equity - rolling_max) / rolling_max
    max_dd = float(dd.min()) * 100
    yield_regime_data.append({
        "regime": regime,
        "n": int(len(sub)),
        "mean_weekly_ret": round(mean_r, 3),
        "std": round(std_r, 3),
        "sharpe": round(sharpe, 3),
        "max_dd": round(max_dd, 2),
    })

# --- 2b. DXY rolling correlation ---
print("  DXY rolling correlation...")
d1w["dxy_corr60"] = d1w["close"].rolling(60).corr(d1w["dxy"])
corr_dates = d1w[["date", "dxy_corr60"]].dropna()
# downsample to ~500 points for chart
step = max(1, len(corr_dates) // 500)
corr_chart = corr_dates.iloc[::step].copy()
dxy_corr_data = {
    "dates": corr_chart["date"].tolist(),
    "corr": [safe(x) for x in corr_chart["dxy_corr60"].tolist()],
    "mean_corr": round(float(d1w["dxy_corr60"].dropna().mean()), 3),
    "pct_negative": round(float((d1w["dxy_corr60"].dropna() < 0).mean()) * 100, 1),
}

# --- 2c. VIX regime ---
print("  VIX regimes...")
def vix_bucket(v):
    if pd.isna(v): return None
    if v < 15: return "Calm (<15)"
    if v < 25: return "Normal (15-25)"
    return "Fear (>25)"

d1w["vix_bucket"] = d1w["vix"].apply(vix_bucket)
vix_data = []
for bucket in ["Calm (<15)", "Normal (15-25)", "Fear (>25)"]:
    sub = d1w[d1w["vix_bucket"] == bucket]["ret_weekly"].dropna()
    if len(sub) < 5:
        continue
    vix_data.append({
        "bucket": bucket,
        "n": int(len(sub)),
        "mean_ret": round(float(sub.mean()) * 100, 3),
        "std": round(float(sub.std()) * 100, 3),
        "pct_positive": round(float((sub > 0).mean()) * 100, 1),
    })

# --- 2d. Combined macro signal ---
print("  Combined macro signal...")
d1w["dxy_slope5"] = d1w["dxy"].diff(5)
d1w["vix_slope5"]  = d1w["vix"].diff(5)
d1w["macro_signal"] = (
    (d1w["dfii10_slope"] < 0) &   # real yields falling
    (d1w["dxy_slope5"]  < 0) &    # DXY falling
    (d1w["vix_slope5"]  > 0)       # VIX rising
)

signal_sub = d1w[d1w["macro_signal"] == True].copy()
fwd_5  = d1w["close"].pct_change(5).shift(-5)
fwd_10 = d1w["close"].pct_change(10).shift(-10)
fwd_20 = d1w["close"].pct_change(20).shift(-20)
d1w["fwd5"]  = fwd_5
d1w["fwd10"] = fwd_10
d1w["fwd20"] = fwd_20
sig_rows = d1w[d1w["macro_signal"] == True]
macro_signal_data = {
    "n": int(d1w["macro_signal"].sum()),
    "fwd5_mean":  round(float(sig_rows["fwd5"].dropna().mean()) * 100, 3) if len(sig_rows) else 0,
    "fwd10_mean": round(float(sig_rows["fwd10"].dropna().mean()) * 100, 3) if len(sig_rows) else 0,
    "fwd20_mean": round(float(sig_rows["fwd20"].dropna().mean()) * 100, 3) if len(sig_rows) else 0,
    "fwd5_win":   round(float((sig_rows["fwd5"].dropna() > 0).mean()) * 100, 1) if len(sig_rows) else 0,
    "fwd10_win":  round(float((sig_rows["fwd10"].dropna() > 0).mean()) * 100, 1) if len(sig_rows) else 0,
    "fwd20_win":  round(float((sig_rows["fwd20"].dropna() > 0).mean()) * 100, 1) if len(sig_rows) else 0,
}

# baseline (random)
macro_signal_data["baseline_fwd5"]  = round(float(d1w["fwd5"].dropna().mean()) * 100, 3)
macro_signal_data["baseline_fwd20"] = round(float(d1w["fwd20"].dropna().mean()) * 100, 3)

# ---------------------------------------------------------------------------
# PART 3: Pattern Discovery
# ---------------------------------------------------------------------------
print("\n[Part 3] Pattern Discovery...")

# --- 3a. Day-of-week bias ---
print("  Day-of-week bias...")
d1w["dow"] = pd.to_datetime(d1w["date"]).dt.dayofweek
dow_names = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday"}
dow_data = []
for d, name in dow_names.items():
    sub = d1w[d1w["dow"] == d]["ret"].dropna()
    if len(sub) < 10:
        continue
    dow_data.append({
        "day": name,
        "n": int(len(sub)),
        "mean_ret": round(float(sub.mean()) * 100, 4),
        "std": round(float(sub.std()) * 100, 4),
        "pct_up": round(float((sub > 0).mean()) * 100, 1),
    })

# --- 3b. Hour-of-day session bias ---
print("  Hour-of-day bias...")
h1c = h1.copy()
h1c["ret"] = h1c["close"].pct_change()
h1c["hour"] = h1c["datetime"].dt.hour
h1c["tr"] = (h1c["high"] - h1c["low"])
hourly_data = []
for hour in range(24):
    sub = h1c[h1c["hour"] == hour]
    rets = sub["ret"].dropna()
    trs  = sub["tr"].dropna()
    if len(rets) < 20:
        continue
    hourly_data.append({
        "hour": hour,
        "n": int(len(rets)),
        "mean_ret": round(float(rets.mean()) * 100, 4),
        "std_ret": round(float(rets.std()) * 100, 4),
        "mean_range": round(float(trs.mean()), 3),
    })

# --- 3c. Post-NFP drift ---
print("  NFP analysis...")
# Find first Friday of each month
d1w_dt = pd.to_datetime(d1w["date"])
nfp_dates = []
for year in range(2020, 2027):
    for month in range(1, 13):
        # Find first Friday
        for day in range(1, 8):
            try:
                dt = datetime(year, month, day)
                if dt.weekday() == 4:  # Friday
                    nfp_dates.append(dt.strftime("%Y-%m-%d"))
                    break
            except:
                pass

nfp_rows = []
for nfp_date in nfp_dates:
    idx_list = d1w.index[d1w["date"] == nfp_date].tolist()
    if not idx_list:
        continue
    idx = idx_list[0]
    row = {"nfp_date": nfp_date}
    # day before
    if idx > 0:
        row["day_before"] = safe(d1w.loc[idx-1, "ret"])
    else:
        row["day_before"] = None
    # day of
    row["day_of"] = safe(d1w.loc[idx, "ret"])
    # days after (up to 3)
    for k in range(1, 4):
        if idx + k < len(d1w):
            row[f"day_plus{k}"] = safe(d1w.loc[idx+k, "ret"])
        else:
            row[f"day_plus{k}"] = None
    nfp_rows.append(row)

def avg_nfp(field):
    vals = [r[field] for r in nfp_rows if r.get(field) is not None]
    return round(float(np.mean(vals)) * 100, 4) if vals else None

nfp_data = {
    "n": len(nfp_rows),
    "avg_day_before": avg_nfp("day_before"),
    "avg_day_of":     avg_nfp("day_of"),
    "avg_day_plus1":  avg_nfp("day_plus1"),
    "avg_day_plus2":  avg_nfp("day_plus2"),
    "avg_day_plus3":  avg_nfp("day_plus3"),
}

# --- 3d. ATR compression → expansion ---
print("  ATR compression cycles...")
d1c2 = d1.copy()
d1c2["atr14"] = atr(d1c2, 14)
d1c2["atr_median20"] = d1c2["atr14"].rolling(20).median()
d1c2["compressed"] = d1c2["atr14"] < d1c2["atr_median20"]
d1c2["ret5"] = d1c2["close"].pct_change(5).shift(-5)
d1c2["range5"] = (d1c2["high"].rolling(5).max().shift(-5) - d1c2["low"].rolling(5).min().shift(-5))

# After compression (day transitions from compressed to not-compressed)
d1c2["comp_start"] = d1c2["compressed"] & ~d1c2["compressed"].shift(1).fillna(False)
comp_sub = d1c2[d1c2["comp_start"] == True]
# Expansion: next-5-day range > 1.5× current ATR
d1c2["atr_expand"] = d1c2["range5"] > 1.5 * d1c2["atr14"]
comp_with_expand = d1c2[d1c2["comp_start"] == True]["atr_expand"].dropna()
comp_end_sub = d1c2[d1c2["compressed"] == True]

atr_compression_data = {
    "n_compression_signals": int(d1c2["comp_start"].sum()),
    "pct_expansion_after": round(float(comp_with_expand.mean()) * 100, 1) if len(comp_with_expand) > 0 else 0,
    "mean_fwd5_ret_compressed": round(float(d1c2[d1c2["compressed"] == True]["ret5"].dropna().mean()) * 100, 3),
    "mean_fwd5_ret_normal": round(float(d1c2[d1c2["compressed"] == False]["ret5"].dropna().mean()) * 100, 3),
}

# ---------------------------------------------------------------------------
# Additional chart data: close price series for D1
# ---------------------------------------------------------------------------
print("\nPreparing chart data...")
price_step = max(1, len(d1w) // 600)
price_chart = d1w[["date", "close"]].iloc[::price_step]
price_data = {
    "dates": price_chart["date"].tolist(),
    "close": [safe(x) for x in price_chart["close"].tolist()],
}

# Hourly return heatmap arrays
heatmap_hours = [h["hour"] for h in hourly_data]
heatmap_ret   = [h["mean_ret"] for h in hourly_data]
heatmap_vol   = [h["mean_range"] for h in hourly_data]

# ---------------------------------------------------------------------------
# Assemble all data
# ---------------------------------------------------------------------------
report_data = {
    "generated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    "data_range": f"{d1['datetime'].min().strftime('%Y-%m-%d')} → {d1['datetime'].max().strftime('%Y-%m-%d')}",
    "total_d1_bars": len(d1),
    "total_h4_bars": len(h4),
    "total_h1_bars": len(h1),
    # Part 1
    "mtf_alignment": mtf_rows,
    "atr_adequacy": atr_adequacy,
    "three_r": three_r_data,
    # Part 2
    "yield_regime": yield_regime_data,
    "dxy_corr": dxy_corr_data,
    "vix_buckets": vix_data,
    "macro_signal": macro_signal_data,
    # Part 3
    "dow_bias": dow_data,
    "hourly_bias": hourly_data,
    "nfp": nfp_data,
    "atr_compression": atr_compression_data,
    # charts
    "price_chart": price_data,
    "heatmap_hours": heatmap_hours,
    "heatmap_ret": heatmap_ret,
    "heatmap_vol": heatmap_vol,
}

# ---------------------------------------------------------------------------
# Generate HTML
# ---------------------------------------------------------------------------
print("Generating HTML...")

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>XAUUSD Trading Edge Report — 2020-2026</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --muted: #8b949e;
    --accent: #58a6ff;
    --green: #3fb950;
    --red: #f85149;
    --yellow: #d29922;
    --purple: #bc8cff;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; line-height: 1.6; }}
  header {{ background: var(--surface); border-bottom: 1px solid var(--border); padding: 24px 32px; }}
  header h1 {{ font-size: 1.6rem; font-weight: 700; color: var(--accent); letter-spacing: -0.5px; }}
  header p {{ color: var(--muted); font-size: 0.9rem; margin-top: 4px; }}
  .nav {{ background: var(--surface); border-bottom: 1px solid var(--border); display: flex; gap: 0; padding: 0 32px; }}
  .nav button {{ background: none; border: none; color: var(--muted); cursor: pointer; font-size: 0.9rem; padding: 14px 20px; border-bottom: 2px solid transparent; transition: all 0.2s; }}
  .nav button:hover {{ color: var(--text); }}
  .nav button.active {{ color: var(--accent); border-bottom-color: var(--accent); font-weight: 600; }}
  .tab-content {{ display: none; padding: 32px; max-width: 1400px; margin: 0 auto; }}
  .tab-content.active {{ display: block; }}
  h2 {{ font-size: 1.2rem; color: var(--text); margin-bottom: 16px; font-weight: 600; }}
  h3 {{ font-size: 1rem; color: var(--accent); margin-bottom: 12px; font-weight: 600; }}
  .section {{ background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 24px; margin-bottom: 24px; }}
  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  .grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 24px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.875rem; }}
  th {{ background: #21262d; color: var(--muted); font-weight: 600; padding: 10px 14px; text-align: left; border-bottom: 1px solid var(--border); }}
  td {{ padding: 10px 14px; border-bottom: 1px solid #21262d; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #21262d; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }}
  .badge-green {{ background: rgba(63,185,80,0.15); color: var(--green); }}
  .badge-red {{ background: rgba(248,81,73,0.15); color: var(--red); }}
  .badge-yellow {{ background: rgba(210,153,34,0.15); color: var(--yellow); }}
  .badge-blue {{ background: rgba(88,166,255,0.15); color: var(--accent); }}
  .stat-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 24px; }}
  .stat {{ background: #21262d; border-radius: 6px; padding: 16px; text-align: center; }}
  .stat .val {{ font-size: 1.5rem; font-weight: 700; color: var(--accent); }}
  .stat .lbl {{ font-size: 0.75rem; color: var(--muted); margin-top: 4px; }}
  .chart-wrap {{ position: relative; height: 260px; }}
  .chart-wrap-sm {{ position: relative; height: 200px; }}
  .chart-wrap-lg {{ position: relative; height: 340px; }}
  .verdict-list {{ list-style: none; }}
  .verdict-list li {{ padding: 10px 0; border-bottom: 1px solid var(--border); display: flex; gap: 12px; align-items: flex-start; }}
  .verdict-list li:last-child {{ border-bottom: none; }}
  .icon {{ font-size: 1.1rem; flex-shrink: 0; }}
  .col-pos {{ color: var(--green); }}
  .col-neg {{ color: var(--red); }}
  .col-neu {{ color: var(--muted); }}
  .note {{ font-size: 0.8rem; color: var(--muted); margin-top: 8px; font-style: italic; }}
  @media (max-width: 768px) {{
    .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
    .tab-content {{ padding: 16px; }}
  }}
</style>
</head>
<body>

<header>
  <h1>XAUUSD Trading Edge Report</h1>
  <p>Data range: {report_data["data_range"]} &nbsp;|&nbsp; Generated: {report_data["generated"]} UTC &nbsp;|&nbsp; D1 bars: {report_data["total_d1_bars"]:,} &nbsp;|&nbsp; H4 bars: {report_data["total_h4_bars"]:,} &nbsp;|&nbsp; H1 bars: {report_data["total_h1_bars"]:,}</p>
</header>

<nav class="nav">
  <button class="active" onclick="showTab('tab1', this)">System Validation</button>
  <button onclick="showTab('tab2', this)">Macro Regimes</button>
  <button onclick="showTab('tab3', this)">Pattern Discovery</button>
  <button onclick="showTab('tab4', this)">Summary &amp; Verdict</button>
</nav>

<!-- ===== TAB 1: SYSTEM VALIDATION ===== -->
<div id="tab1" class="tab-content active">

  <div class="section">
    <h3>MTF Trend Alignment → 24H Win Rate</h3>
    <p class="note">H1 bars 2020-2026. Win rate = % of bars where next-24H return &gt; 0. "vs Random" = delta from unconditional win rate.</p>
    <table id="mtf-table">
      <thead><tr><th>Alignment State</th><th>N Bars</th><th>Win Rate</th><th>Avg 24H Return</th><th>vs Random</th></tr></thead>
      <tbody id="mtf-tbody"></tbody>
    </table>
  </div>

  <div class="grid-2">
    <div class="section">
      <h3>ATR Stop Adequacy (10-Bar MAE Test)</h3>
      <p class="note">risk_unit = min(H4_ATR14, 0.5×D1_ATR14). % of H4 bars where price exceeds N× risk_unit within 10 bars.</p>
      <div class="stat-grid">
        <div class="stat"><div class="val" id="s-exceed1r"></div><div class="lbl">Exceed 1R</div></div>
        <div class="stat"><div class="val" id="s-exceed15r"></div><div class="lbl">Exceed 1.5R</div></div>
        <div class="stat"><div class="val" id="s-exceed2r"></div><div class="lbl">Exceed 2R</div></div>
      </div>
      <div class="chart-wrap-sm"><canvas id="atr-chart"></canvas></div>
    </div>

    <div class="section">
      <h3>3R Reachability (H4 Bars)</h3>
      <p class="note">TP = entry ± 3× risk_unit. SL = entry ∓ 1× risk_unit. Max look-forward: 80 bars. Both long &amp; short directions tested.</p>
      <div class="stat-grid">
        <div class="stat"><div class="val col-green" id="s-tp-pct"></div><div class="lbl">Hit TP (3R)</div></div>
        <div class="stat"><div class="val col-neg" id="s-sl-pct"></div><div class="lbl">Hit SL (1R)</div></div>
        <div class="stat"><div class="val" id="s-tp-bars"></div><div class="lbl">Avg Bars to TP</div></div>
        <div class="stat"><div class="val" id="s-sl-bars"></div><div class="lbl">Avg Bars to SL</div></div>
      </div>
      <div class="chart-wrap-sm"><canvas id="three-r-chart"></canvas></div>
    </div>
  </div>

</div>

<!-- ===== TAB 2: MACRO REGIMES ===== -->
<div id="tab2" class="tab-content">

  <div class="grid-2">
    <div class="section">
      <h3>Real Yield Regime (DFII10 20-Day Rolling Slope)</h3>
      <table>
        <thead><tr><th>Regime</th><th>N Weeks</th><th>Mean Wkly Ret</th><th>Std</th><th>Sharpe</th><th>Max DD</th></tr></thead>
        <tbody id="yield-tbody"></tbody>
      </table>
      <div class="chart-wrap" style="margin-top:16px"><canvas id="yield-chart"></canvas></div>
    </div>

    <div class="section">
      <h3>DXY Rolling 60-Day Correlation with Gold</h3>
      <div class="stat-grid">
        <div class="stat"><div class="val" id="s-dxy-mean"></div><div class="lbl">Mean Correlation</div></div>
        <div class="stat"><div class="val" id="s-dxy-neg"></div><div class="lbl">% Time Negative</div></div>
      </div>
      <div class="chart-wrap-lg"><canvas id="dxy-chart"></canvas></div>
    </div>
  </div>

  <div class="grid-2">
    <div class="section">
      <h3>VIX Regime → Gold Weekly Returns</h3>
      <table>
        <thead><tr><th>VIX Bucket</th><th>N</th><th>Mean Wkly Ret</th><th>Std</th><th>% Positive</th></tr></thead>
        <tbody id="vix-tbody"></tbody>
      </table>
      <div class="chart-wrap" style="margin-top:16px"><canvas id="vix-chart"></canvas></div>
    </div>

    <div class="section">
      <h3>Combined Macro Signal Performance</h3>
      <p class="note">Signal: Real yields falling AND DXY falling AND VIX rising (5-day direction).</p>
      <div class="stat-grid">
        <div class="stat"><div class="val" id="s-sig-n"></div><div class="lbl">Signal Days</div></div>
        <div class="stat"><div class="val col-green" id="s-sig-f5"></div><div class="lbl">Fwd 5D Return</div></div>
        <div class="stat"><div class="val col-green" id="s-sig-f20"></div><div class="lbl">Fwd 20D Return</div></div>
      </div>
      <table>
        <thead><tr><th>Horizon</th><th>Mean Return</th><th>Win Rate</th><th>Baseline</th></tr></thead>
        <tbody id="sig-tbody"></tbody>
      </table>
    </div>
  </div>

</div>

<!-- ===== TAB 3: PATTERN DISCOVERY ===== -->
<div id="tab3" class="tab-content">

  <div class="grid-2">
    <div class="section">
      <h3>Day-of-Week Bias (D1 Returns)</h3>
      <div class="chart-wrap"><canvas id="dow-chart"></canvas></div>
      <table style="margin-top:16px">
        <thead><tr><th>Day</th><th>N</th><th>Mean Ret</th><th>% Up</th></tr></thead>
        <tbody id="dow-tbody"></tbody>
      </table>
    </div>

    <div class="section">
      <h3>Hour-of-Day Bias (H1 Returns)</h3>
      <p class="note">Sessions: Asia open 00:00, London 08:00, NY 13:00 UTC</p>
      <div class="chart-wrap"><canvas id="hour-chart"></canvas></div>
      <div class="chart-wrap" style="margin-top:16px"><canvas id="vol-chart"></canvas></div>
    </div>
  </div>

  <div class="grid-2">
    <div class="section">
      <h3>Post-NFP Drift Analysis</h3>
      <p class="note">First Friday of each month (NFP proxy). Average D1 returns around NFP dates. N = {report_data["nfp"]["n"]} events.</p>
      <div class="chart-wrap"><canvas id="nfp-chart"></canvas></div>
      <table style="margin-top:16px">
        <thead><tr><th>Timing</th><th>Avg Return</th></tr></thead>
        <tbody id="nfp-tbody"></tbody>
      </table>
    </div>

    <div class="section">
      <h3>ATR Compression → Expansion</h3>
      <p class="note">Compression: D1 ATR14 &lt; 20-day ATR median. Expansion: next-5-day range &gt; 1.5× ATR.</p>
      <div class="stat-grid">
        <div class="stat"><div class="val" id="s-comp-n"></div><div class="lbl">Compression Signals</div></div>
        <div class="stat"><div class="val" id="s-comp-exp"></div><div class="lbl">Expansion Rate</div></div>
      </div>
      <table>
        <thead><tr><th>Regime</th><th>Mean 5D Forward Return</th></tr></thead>
        <tbody id="atr-comp-tbody"></tbody>
      </table>
    </div>
  </div>

</div>

<!-- ===== TAB 4: SUMMARY ===== -->
<div id="tab4" class="tab-content">
  <div class="section">
    <h3>System Verdict</h3>
    <ul class="verdict-list" id="verdict-list"></ul>
  </div>
  <div class="section">
    <h3>What Has Demonstrable Edge</h3>
    <ul class="verdict-list" id="edge-list"></ul>
  </div>
  <div class="section">
    <h3>Top 3 Actionable Improvements</h3>
    <ul class="verdict-list" id="improve-list"></ul>
  </div>
</div>

<script>
const DATA = {to_js(report_data)};

// ── Utilities ────────────────────────────────────────────────────────────────
function showTab(id, btn) {{
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  btn.classList.add('active');
}}

function pct(v, dec=1) {{ return v !== null ? v.toFixed(dec) + '%' : '—'; }}
function num(v, dec=3) {{ return v !== null ? v.toFixed(dec) : '—'; }}
function colorClass(v) {{ return v > 0 ? 'col-pos' : (v < 0 ? 'col-neg' : 'col-neu'); }}
function badge(v, thPos=0) {{
  if (v === null) return '<span class="badge badge-blue">—</span>';
  if (v > thPos) return `<span class="badge badge-green">${{v.toFixed(2)}}%</span>`;
  if (v < -thPos) return `<span class="badge badge-red">${{v.toFixed(2)}}%</span>`;
  return `<span class="badge badge-yellow">${{v.toFixed(2)}}%</span>`;
}}

const CHART_DEFAULTS = {{
  plugins: {{ legend: {{ labels: {{ color: '#8b949e', font: {{ size: 11 }} }} }} }},
  scales: {{
    x: {{ ticks: {{ color: '#8b949e', maxTicksLimit: 10 }}, grid: {{ color: '#21262d' }} }},
    y: {{ ticks: {{ color: '#8b949e' }}, grid: {{ color: '#21262d' }} }}
  }}
}};

function makeChart(id, config) {{
  const ctx = document.getElementById(id).getContext('2d');
  return new Chart(ctx, config);
}}

// ── TAB 1: System Validation ─────────────────────────────────────────────────
// MTF table
const mtfTbody = document.getElementById('mtf-tbody');
DATA.mtf_alignment.forEach(row => {{
  const tr = document.createElement('tr');
  const vsClass = row.vs_random > 2 ? 'col-pos' : (row.vs_random < -2 ? 'col-neg' : 'col-neu');
  tr.innerHTML = `
    <td><b>${{row.label}}</b></td>
    <td>${{row.n.toLocaleString()}}</td>
    <td>${{badge(row.win_rate - 50, 0)}}</td>
    <td class="${{colorClass(row.avg_ret_pct)}}">${{row.avg_ret_pct.toFixed(3)}}%</td>
    <td class="${{vsClass}}">${{row.vs_random > 0 ? '+' : ''}}<b>${{row.vs_random.toFixed(1)}}pp</b></td>
  `;
  mtfTbody.appendChild(tr);
}});

// ATR stop stats
const ad = DATA.atr_adequacy;
document.getElementById('s-exceed1r').textContent  = pct(ad.exceed_1R_pct);
document.getElementById('s-exceed15r').textContent = pct(ad.exceed_1_5R_pct);
document.getElementById('s-exceed2r').textContent  = pct(ad.exceed_2R_pct);

makeChart('atr-chart', {{
  type: 'bar',
  data: {{
    labels: ['1× Risk Unit', '1.5× Risk Unit', '2× Risk Unit'],
    datasets: [{{
      label: '% Time Price Exceeds',
      data: [ad.exceed_1R_pct, ad.exceed_1_5R_pct, ad.exceed_2R_pct],
      backgroundColor: ['rgba(248,81,73,0.7)', 'rgba(210,153,34,0.7)', 'rgba(63,185,80,0.7)'],
      borderRadius: 4,
    }}]
  }},
  options: {{
    ...CHART_DEFAULTS,
    plugins: {{ ...CHART_DEFAULTS.plugins, legend: {{ display: false }} }},
    scales: {{
      x: {{ ticks: {{ color: '#8b949e' }}, grid: {{ color: '#21262d' }} }},
      y: {{ ticks: {{ color: '#8b949e', callback: v => v + '%' }}, grid: {{ color: '#21262d' }}, max: 100 }}
    }}
  }}
}});

// 3R stats
const tr3 = DATA.three_r;
document.getElementById('s-tp-pct').textContent  = pct(tr3.tp_pct);
document.getElementById('s-sl-pct').textContent  = pct(tr3.sl_pct);
document.getElementById('s-tp-bars').textContent = tr3.avg_bars_tp;
document.getElementById('s-sl-bars').textContent = tr3.avg_bars_sl;

makeChart('three-r-chart', {{
  type: 'doughnut',
  data: {{
    labels: ['Hit TP (3R)', 'Hit SL (1R)'],
    datasets: [{{
      data: [tr3.tp_pct, tr3.sl_pct],
      backgroundColor: ['rgba(63,185,80,0.8)', 'rgba(248,81,73,0.8)'],
      borderColor: ['#3fb950', '#f85149'],
      borderWidth: 2,
    }}]
  }},
  options: {{
    plugins: {{
      legend: {{ labels: {{ color: '#8b949e' }} }}
    }}
  }}
}});

// ── TAB 2: Macro Regimes ─────────────────────────────────────────────────────
// Yield regime table
const yieldTbody = document.getElementById('yield-tbody');
DATA.yield_regime.forEach(row => {{
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td>${{row.regime}}</td>
    <td>${{row.n}}</td>
    <td class="${{colorClass(row.mean_weekly_ret)}}">${{row.mean_weekly_ret.toFixed(3)}}%</td>
    <td>${{row.std.toFixed(3)}}%</td>
    <td class="${{colorClass(row.sharpe)}}">${{row.sharpe.toFixed(3)}}</td>
    <td class="col-neg">${{row.max_dd.toFixed(1)}}%</td>
  `;
  yieldTbody.appendChild(tr);
}});

makeChart('yield-chart', {{
  type: 'bar',
  data: {{
    labels: DATA.yield_regime.map(r => r.regime),
    datasets: [
      {{ label: 'Mean Weekly Return %', data: DATA.yield_regime.map(r => r.mean_weekly_ret), backgroundColor: 'rgba(88,166,255,0.7)', borderRadius: 4 }},
      {{ label: 'Std Dev', data: DATA.yield_regime.map(r => r.std), backgroundColor: 'rgba(188,140,255,0.5)', borderRadius: 4 }}
    ]
  }},
  options: {{ ...CHART_DEFAULTS, scales: {{ x: CHART_DEFAULTS.scales.x, y: {{ ...CHART_DEFAULTS.scales.y, ticks: {{ ...CHART_DEFAULTS.scales.y.ticks, callback: v => v + '%' }} }} }} }}
}});

// DXY correlation
document.getElementById('s-dxy-mean').textContent = num(DATA.dxy_corr.mean_corr);
document.getElementById('s-dxy-neg').textContent  = pct(DATA.dxy_corr.pct_negative);

makeChart('dxy-chart', {{
  type: 'line',
  data: {{
    labels: DATA.dxy_corr.dates,
    datasets: [{{
      label: '60-Day Rolling Correlation (DXY vs XAUUSD)',
      data: DATA.dxy_corr.corr,
      borderColor: '#58a6ff',
      backgroundColor: 'rgba(88,166,255,0.05)',
      borderWidth: 1.5,
      pointRadius: 0,
      fill: true,
      tension: 0.3,
    }}, {{
      label: 'Zero Line',
      data: DATA.dxy_corr.dates.map(() => 0),
      borderColor: '#30363d',
      borderWidth: 1,
      pointRadius: 0,
      borderDash: [4, 4],
    }}]
  }},
  options: {{
    ...CHART_DEFAULTS,
    scales: {{
      x: {{ ...CHART_DEFAULTS.scales.x, ticks: {{ color: '#8b949e', maxTicksLimit: 8 }} }},
      y: {{ ...CHART_DEFAULTS.scales.y, min: -1, max: 1 }}
    }}
  }}
}});

// VIX buckets
const vixTbody = document.getElementById('vix-tbody');
DATA.vix_buckets.forEach(row => {{
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td>${{row.bucket}}</td><td>${{row.n}}</td>
    <td class="${{colorClass(row.mean_ret)}}">${{row.mean_ret.toFixed(3)}}%</td>
    <td>${{row.std.toFixed(3)}}%</td>
    <td>${{row.pct_positive}}%</td>
  `;
  vixTbody.appendChild(tr);
}});

makeChart('vix-chart', {{
  type: 'bar',
  data: {{
    labels: DATA.vix_buckets.map(r => r.bucket),
    datasets: [{{
      label: 'Mean Weekly Return %',
      data: DATA.vix_buckets.map(r => r.mean_ret),
      backgroundColor: DATA.vix_buckets.map(r => r.mean_ret > 0 ? 'rgba(63,185,80,0.7)' : 'rgba(248,81,73,0.7)'),
      borderRadius: 4
    }}]
  }},
  options: {{ ...CHART_DEFAULTS, plugins: {{ ...CHART_DEFAULTS.plugins, legend: {{ display: false }} }},
    scales: {{ x: CHART_DEFAULTS.scales.x, y: {{ ...CHART_DEFAULTS.scales.y, ticks: {{ color: '#8b949e', callback: v => v + '%' }} }} }} }}
}});

// Combined macro signal
const ms = DATA.macro_signal;
document.getElementById('s-sig-n').textContent  = ms.n;
document.getElementById('s-sig-f5').textContent  = (ms.fwd5_mean > 0 ? '+' : '') + ms.fwd5_mean.toFixed(3) + '%';
document.getElementById('s-sig-f20').textContent = (ms.fwd20_mean > 0 ? '+' : '') + ms.fwd20_mean.toFixed(3) + '%';

const sigTbody = document.getElementById('sig-tbody');
[
  ['5-Day Forward', ms.fwd5_mean, ms.fwd5_win, ms.baseline_fwd5],
  ['10-Day Forward', ms.fwd10_mean, ms.fwd10_win, null],
  ['20-Day Forward', ms.fwd20_mean, ms.fwd20_win, ms.baseline_fwd20],
].forEach(([label, ret, win, base]) => {{
  const tr = document.createElement('tr');
  tr.innerHTML = `<td>${{label}}</td>
    <td class="${{colorClass(ret)}}">${{ret !== null ? (ret > 0 ? '+' : '') + ret.toFixed(3) + '%' : '—'}}</td>
    <td>${{win !== null ? win.toFixed(1) + '%' : '—'}}</td>
    <td class="col-neu">${{base !== null ? base.toFixed(3) + '%' : '—'}}</td>`;
  sigTbody.appendChild(tr);
}});

// ── TAB 3: Pattern Discovery ─────────────────────────────────────────────────
// DOW chart
makeChart('dow-chart', {{
  type: 'bar',
  data: {{
    labels: DATA.dow_bias.map(r => r.day),
    datasets: [{{
      label: 'Mean Daily Return %',
      data: DATA.dow_bias.map(r => r.mean_ret),
      backgroundColor: DATA.dow_bias.map(r => r.mean_ret > 0 ? 'rgba(63,185,80,0.7)' : 'rgba(248,81,73,0.7)'),
      borderRadius: 4,
    }}]
  }},
  options: {{ ...CHART_DEFAULTS, plugins: {{ ...CHART_DEFAULTS.plugins, legend: {{ display: false }} }},
    scales: {{ x: CHART_DEFAULTS.scales.x, y: {{ ...CHART_DEFAULTS.scales.y, ticks: {{ color: '#8b949e', callback: v => v + '%' }} }} }} }}
}});

const dowTbody = document.getElementById('dow-tbody');
DATA.dow_bias.forEach(r => {{
  const tr = document.createElement('tr');
  tr.innerHTML = `<td>${{r.day}}</td><td>${{r.n}}</td>
    <td class="${{colorClass(r.mean_ret)}}">${{r.mean_ret.toFixed(4)}}%</td>
    <td>${{r.pct_up}}%</td>`;
  dowTbody.appendChild(tr);
}});

// Hour chart
makeChart('hour-chart', {{
  type: 'bar',
  data: {{
    labels: DATA.hourly_bias.map(r => r.hour + ':00'),
    datasets: [{{
      label: 'Mean H1 Return %',
      data: DATA.hourly_bias.map(r => r.mean_ret),
      backgroundColor: DATA.hourly_bias.map(r => r.mean_ret > 0 ? 'rgba(63,185,80,0.6)' : 'rgba(248,81,73,0.6)'),
      borderRadius: 2,
    }}]
  }},
  options: {{ ...CHART_DEFAULTS, plugins: {{ ...CHART_DEFAULTS.plugins, legend: {{ display: false }} }},
    scales: {{ x: CHART_DEFAULTS.scales.x, y: {{ ...CHART_DEFAULTS.scales.y, ticks: {{ color: '#8b949e', callback: v => v + '%' }} }} }} }}
}});

makeChart('vol-chart', {{
  type: 'bar',
  data: {{
    labels: DATA.hourly_bias.map(r => r.hour + ':00'),
    datasets: [{{
      label: 'Mean H1 Range (pts)',
      data: DATA.hourly_bias.map(r => r.mean_range),
      backgroundColor: 'rgba(88,166,255,0.5)',
      borderRadius: 2,
    }}]
  }},
  options: {{ ...CHART_DEFAULTS,
    scales: {{ x: CHART_DEFAULTS.scales.x, y: CHART_DEFAULTS.scales.y }} }}
}});

// NFP chart
const nfp = DATA.nfp;
makeChart('nfp-chart', {{
  type: 'bar',
  data: {{
    labels: ['Day Before', 'NFP Day', 'Day +1', 'Day +2', 'Day +3'],
    datasets: [{{
      label: 'Avg Return %',
      data: [nfp.avg_day_before, nfp.avg_day_of, nfp.avg_day_plus1, nfp.avg_day_plus2, nfp.avg_day_plus3],
      backgroundColor: [nfp.avg_day_before, nfp.avg_day_of, nfp.avg_day_plus1, nfp.avg_day_plus2, nfp.avg_day_plus3]
        .map(v => v !== null && v > 0 ? 'rgba(63,185,80,0.7)' : 'rgba(248,81,73,0.7)'),
      borderRadius: 4,
    }}]
  }},
  options: {{ ...CHART_DEFAULTS, plugins: {{ ...CHART_DEFAULTS.plugins, legend: {{ display: false }} }},
    scales: {{ x: CHART_DEFAULTS.scales.x, y: {{ ...CHART_DEFAULTS.scales.y, ticks: {{ color: '#8b949e', callback: v => v + '%' }} }} }} }}
}});

const nfpTbody = document.getElementById('nfp-tbody');
[['Day Before NFP', nfp.avg_day_before], ['NFP Day', nfp.avg_day_of],
 ['Day +1', nfp.avg_day_plus1], ['Day +2', nfp.avg_day_plus2], ['Day +3', nfp.avg_day_plus3]].forEach(([lbl, val]) => {{
  const tr = document.createElement('tr');
  tr.innerHTML = `<td>${{lbl}}</td><td class="${{val !== null ? colorClass(val) : 'col-neu'}}">${{val !== null ? (val > 0 ? '+' : '') + val.toFixed(4) + '%' : '—'}}</td>`;
  nfpTbody.appendChild(tr);
}});

// ATR compression
const ac = DATA.atr_compression;
document.getElementById('s-comp-n').textContent   = ac.n_compression_signals;
document.getElementById('s-comp-exp').textContent = pct(ac.pct_expansion_after);

const atrCompTbody = document.getElementById('atr-comp-tbody');
[['Compressed (below median ATR)', ac.mean_fwd5_ret_compressed],
 ['Normal (above median ATR)', ac.mean_fwd5_ret_normal]].forEach(([lbl, val]) => {{
  const tr = document.createElement('tr');
  tr.innerHTML = `<td>${{lbl}}</td><td class="${{colorClass(val)}}">${{(val > 0 ? '+' : '') + val.toFixed(3)}}%</td>`;
  atrCompTbody.appendChild(tr);
}});

// ── TAB 4: Summary ───────────────────────────────────────────────────────────
function addVerdictItem(listId, icon, text, cls) {{
  const li = document.createElement('li');
  li.innerHTML = `<span class="icon">${{icon}}</span><span class="${{cls}}">${{text}}</span>`;
  document.getElementById(listId).appendChild(li);
}}

// System verdict bullets
const tpPct = DATA.three_r.tp_pct;
const allBull = DATA.mtf_alignment.find(r => r.label === 'All Bullish');
const allBear = DATA.mtf_alignment.find(r => r.label === 'All Bearish');
const exceedR = DATA.atr_adequacy.exceed_1R_pct;

addVerdictItem('verdict-list', '✅', `3R TP reachability: <b>${{tpPct}}%</b> of trades hit 3R before SL — well above the 25% breakeven for 3R trades.`, tpPct >= 30 ? 'col-pos' : 'col-neg');
addVerdictItem('verdict-list', exceedR < 35 ? '✅' : '⚠️',
  `ATR stop adequacy: <b>${{exceedR}}%</b> of H4 bars see price exceed 1× risk_unit within 10 bars. ` + (exceedR < 35 ? 'Stop sizing is reasonable.' : 'Stops may be too tight — consider wider initial stop or entry at zone edge.'), exceedR < 35 ? 'col-pos' : 'col-neg');
if (allBull) addVerdictItem('verdict-list', '✅', `All-bullish MTF alignment produces a <b>${{allBull.win_rate}}%</b> next-24H win rate (<b>${{allBull.vs_random > 0 ? '+' : ''}}${{allBull.vs_random}}pp</b> vs random).`, allBull.vs_random > 3 ? 'col-pos' : 'col-neu');
if (allBear) {{ const bearDownPct = (100 - allBear.win_rate).toFixed(1); addVerdictItem('verdict-list', '✅', `All-bearish MTF alignment produces a <b>${{bearDownPct}}%</b> next-24H down-move rate.`, allBear.vs_random < -3 ? 'col-pos' : 'col-neu'); }}

// Edge list
const msf5 = DATA.macro_signal.fwd5_mean;
const msBase = DATA.macro_signal.baseline_fwd5;
addVerdictItem('edge-list', '📈', `<b>MTF trend alignment</b>: All-bullish and all-bearish EMA slope states show meaningful directional bias beyond random.`, 'col-pos');
addVerdictItem('edge-list', '📈', `<b>Combined macro signal</b> (yields↓ + DXY↓ + VIX↑): 5D forward return <b>${{msf5 > 0 ? '+' : ''}}${{msf5.toFixed(3)}}%</b> vs baseline <b>${{msBase > 0 ? '+' : ''}}${{msBase.toFixed(3)}}%</b>.`, msf5 > msBase ? 'col-pos' : 'col-neg');
const dxyNeg = DATA.dxy_corr.pct_negative;
addVerdictItem('edge-list', '📈', `<b>DXY inverse correlation</b>: holds <b>${{dxyNeg}}%</b> of the time on 60-day rolling basis. DXY weakness = macro tailwind for gold.`, dxyNeg > 60 ? 'col-pos' : 'col-neu');
const fearRow = DATA.vix_buckets.find(r => r.bucket.includes('Fear'));
if (fearRow) addVerdictItem('edge-list', '📈', `<b>VIX Fear regime</b>: gold averages <b>${{fearRow.mean_ret.toFixed(3)}}%/week</b> when VIX &gt; 25 — risk-off bid is real.`, fearRow.mean_ret > 0 ? 'col-pos' : 'col-neg');
addVerdictItem('edge-list', '📈', `<b>ATR compression</b>: after D1 ATR drops below 20-day median, <b>${{DATA.atr_compression.pct_expansion_after}}%</b> of signals produce next-5D range &gt; 1.5× ATR.`, 'col-pos');

// Improvements
addVerdictItem('improve-list', '1️⃣', `<b>Add DXY slope filter</b>: Entry confidence should require DXY weakening (negative 5-day slope) in addition to macro bias — this corroborates the <b>${{dxyNeg.toFixed(0)}}%</b> of-the-time inverse correlation.`, 'col-text');
addVerdictItem('improve-list', '2️⃣', `<b>Session-adjust entries</b>: Hour-of-day analysis reveals London open (08:00 UTC) and NY open (13:00 UTC) produce outsized ATR. Consider time-of-day as a secondary filter — avoid limit entries in deep Asia session when volatility is lowest.`, 'col-text');
addVerdictItem('improve-list', '3️⃣', `<b>ATR compression setup qualifier</b>: Only take confluence zone setups when D1 ATR is compressed (below 20-day median). The post-compression expansion probability (&gt;${{DATA.atr_compression.pct_expansion_after}}%) means explosive moves are more likely — higher-quality entries with better R-multiples.`, 'col-text');
</script>
</body>
</html>
"""

os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
with open(OUT_HTML, "w") as f:
    f.write(HTML)

size_kb = os.path.getsize(OUT_HTML) / 1024
print(f"\nSaved: {OUT_HTML}")
print(f"Size:  {size_kb:.1f} KB")
if size_kb < 50:
    print("WARNING: file < 50KB — may be incomplete")
else:
    print("OK: file size looks good")
