"""
XAUUSD Weekly Data Pull — single entry point
Fetches, resamples, updates FRED, computes all indicators, writes pull file.

Usage:
    .venv/bin/python scripts/weekly_pull.py           # normal run
    .venv/bin/python scripts/weekly_pull.py --force   # re-fetch full history

Pipeline:
    TD 15M fetch (1 API call) → append 15min.csv → resample → 1h/4h/1day.csv
    FRED fetch                → append data/fred/*.csv
    Compute indicators locally (ATR, ADX, EMA, RSI, MACD, pivots, fibs, swings)
    Fetch VP (yfinance), COT (CFTC), GLD (SPDR)  — no API key required
    Write data/weekly_pull/weekly_pull_{YEAR}_W{WW}.txt

Requirements: pip install requests pandas numpy yfinance python-dotenv
"""

import os, sys, json, argparse
import requests, pandas as pd, numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from pathlib import Path
from io import StringIO
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))
from ohlc_store import upsert, last_dt as manifest_last_dt

load_dotenv()

TWELVE_KEY = os.getenv("TWELVE_DATA_KEY")
FRED_KEY   = os.getenv("FRED_KEY")

TODAY    = datetime.today()
WEEK_NUM = TODAY.isocalendar()[1]
YEAR     = TODAY.year

SYMBOL    = "XAU/USD"
SYM_CLEAN = "xauusd"
TD_DIR    = Path(f"data/twelvedata/{SYM_CLEAN}")
FRED_DIR  = Path("data/fred")
PULL_DIR  = Path("data/weekly_pull")

FRED_SERIES = ["DFII10", "DGS10", "T5YIE", "DFF", "DTWEXBGS", "VIXCLS"]
TF_RESAMPLE = {"1h": "1h", "4h": "4h", "1day": "1D"}

# ── STEP 1: FETCH 15M + RESAMPLE ─────────────────────────────────────────────

def fetch_15m(force=False):
    last      = manifest_last_dt("twelvedata", SYMBOL, "15min")
    outputsize = 800 if (force or last is None) else 200
    r = requests.get("https://api.twelvedata.com/time_series", params={
        "symbol": SYMBOL, "interval": "15min",
        "outputsize": outputsize, "timezone": "UTC", "apikey": TWELVE_KEY,
    }, timeout=20)
    data = r.json()
    if "code" in data:
        raise ValueError(f"TD 15min: {data.get('message', data)}")
    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col])
    df["volume"] = pd.to_numeric(df.get("volume", 0))
    df = df.sort_values("datetime").reset_index(drop=True)
    if not force and last is not None:
        df = df[df["datetime"] > last]
    return df

def resample_all():
    src = pd.read_csv(TD_DIR / "15min.csv", parse_dates=["datetime"])
    src = src.sort_values("datetime").set_index("datetime")
    results = []
    for tf, rule in TF_RESAMPLE.items():
        agg = src.resample(rule, label="left", closed="left").agg({
            "open": "first", "high": "max", "low": "min",
            "close": "last", "volume": "sum",
        }).dropna(subset=["open", "close"]).reset_index()
        info = upsert("twelvedata", SYMBOL, tf, agg)
        results.append((tf, len(agg), info["last_dt"]))
    return results

# ── STEP 2: FRED UPDATE ───────────────────────────────────────────────────────

def _fred_manifest():
    p = FRED_DIR / "_manifest.json"
    return json.loads(p.read_text()) if p.exists() else {}

def _save_fred_manifest(data):
    (FRED_DIR / "_manifest.json").write_text(json.dumps(data, indent=2))

def update_fred(force=False):
    manifest = _fred_manifest()
    results  = []
    for sid in FRED_SERIES:
        csv_path  = FRED_DIR / f"{sid}.csv"
        last_date = manifest.get(sid, {}).get("last_dt")
        obs_start = ((datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
                     if (force or not last_date) else last_date)
        try:
            r   = requests.get("https://api.stlouisfed.org/fred/series/observations",
                               params={"series_id": sid, "observation_start": obs_start,
                                       "api_key": FRED_KEY, "file_type": "json"}, timeout=15)
            obs = r.json().get("observations", [])
            new = pd.DataFrame(obs)[["date", "value"]]
            new["value"] = pd.to_numeric(new["value"], errors="coerce")
            new = new.dropna()
            if not force and last_date:
                new = new[new["date"] > last_date]
            if not new.empty:
                if csv_path.exists():
                    existing = pd.read_csv(csv_path)
                    combined = (pd.concat([existing, new], ignore_index=True)
                                .drop_duplicates("date", keep="last")
                                .sort_values("date").reset_index(drop=True))
                else:
                    combined = new
                combined.to_csv(csv_path, index=False)
                manifest[sid] = {"last_dt": str(combined["date"].iloc[-1]),
                                 "rows": len(combined),
                                 "last_pull_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}
                _save_fred_manifest(manifest)
            results.append((sid, len(new), manifest.get(sid, {}).get("last_dt", "?")))
        except Exception as e:
            results.append((sid, f"ERROR: {e}", last_date or "?"))
    return results

# ── STEP 3: LOAD LOCAL DATA ───────────────────────────────────────────────────

def load_ohlc(path):
    df = pd.read_csv(path, parse_dates=["datetime"]).set_index("datetime").sort_index()
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.dropna(subset=["open", "high", "low", "close"])

def load_fred_local(sid):
    df = pd.read_csv(FRED_DIR / f"{sid}.csv", parse_dates=["date"]).set_index("date").sort_index()
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna()

# ── STEP 4: INDICATORS ────────────────────────────────────────────────────────

def calc_atr(df, p=14):
    h, l, c = df["high"], df["low"], df["close"]
    tr = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    return round(float(tr.rolling(p).mean().iloc[-1]), 2)

def calc_atr_series(df, p=14):
    h, l, c = df["high"], df["low"], df["close"]
    tr = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(p).mean()

def calc_adx(df, p=14):
    h, l, c = df["high"], df["low"], df["close"]
    up, down = h.diff(), -l.diff()
    plus  = pd.Series(np.where((up > down) & (up > 0), up, 0.0), index=df.index)
    minus = pd.Series(np.where((down > up) & (down > 0), down, 0.0), index=df.index)
    tr_s  = pd.concat([(h-l), (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    tr14  = tr_s.ewm(alpha=1/p, adjust=False).mean()
    dip   = 100 * plus.ewm(alpha=1/p, adjust=False).mean() / tr14
    dim   = 100 * minus.ewm(alpha=1/p, adjust=False).mean() / tr14
    adx   = (100 * (dip-dim).abs() / (dip+dim)).ewm(alpha=1/p, adjust=False).mean()
    return round(float(adx.iloc[-1]), 1)

def calc_ema(series, span):
    return round(float(series.ewm(span=span, adjust=False).mean().iloc[-1]), 2)

def calc_rsi_series(df, p=14, n=10):
    delta = df["close"].diff()
    avg_g = delta.clip(lower=0).ewm(alpha=1/p, adjust=False).mean()
    avg_l = (-delta).clip(lower=0).ewm(alpha=1/p, adjust=False).mean()
    rsi   = (100 - 100/(1 + avg_g/avg_l)).round(1)
    tail  = rsi.iloc[-n:]
    return list(zip([str(i.date()) for i in tail.index], tail.values))

def calc_macd(df, fast=12, slow=26, sig=9, n=5):
    c    = df["close"]
    line = c.ewm(span=fast, adjust=False).mean() - c.ewm(span=slow, adjust=False).mean()
    sl   = line.ewm(span=sig, adjust=False).mean()
    hist = line - sl
    return [(str(i.date()), round(float(line[i]),2), round(float(sl[i]),2), round(float(hist[i]),2))
            for i in line.iloc[-n:].index]

def calc_pivots(d1_df):
    gw = d1_df.resample("W").agg({"open":"first","high":"max","low":"min","close":"last"}).dropna()
    b  = gw.iloc[-2]
    pp = (b["high"] + b["low"] + b["close"]) / 3
    return {"PP": round(pp,2),
            "R1": round(2*pp-b["low"],2),    "R2": round(pp+b["high"]-b["low"],2),
            "R3": round(b["high"]+2*(pp-b["low"]),2),
            "S1": round(2*pp-b["high"],2),   "S2": round(pp-b["high"]+b["low"],2),
            "S3": round(b["low"]-2*(b["high"]-pp),2)}

def swing_points(df, n=5):
    highs, lows = [], []
    for i in range(n, len(df)-n):
        if df["high"].iloc[i] == df["high"].iloc[i-n:i+n+1].max():
            highs.append((str(df.index[i].date()), round(float(df["high"].iloc[i]),2)))
        if df["low"].iloc[i] == df["low"].iloc[i-n:i+n+1].min():
            lows.append((str(df.index[i].date()), round(float(df["low"].iloc[i]),2)))
    return highs[-5:], lows[-5:]

def fib_levels(lo, hi):
    d = hi - lo
    return {"swing_low": round(lo,2), "swing_high": round(hi,2),
            "78.6%": round(hi-0.786*d,2), "61.8%": round(hi-0.618*d,2),
            "50.0%": round(hi-0.500*d,2), "38.2%": round(hi-0.382*d,2),
            "ext_127.2%": round(lo+1.272*d,2), "ext_161.8%": round(lo+1.618*d,2)}

def weekend_gap(h4_full, h4_trade):
    fri = h4_trade[h4_trade.index.dayofweek == 4]
    if fri.empty:
        return None
    last_fri_ts = fri.index[-1]
    fri_close   = float(fri.iloc[-1]["close"])
    after = h4_full[h4_full.index > last_fri_ts]
    if after.empty:
        return None
    next_ts   = after.index[0]
    next_open = float(after.iloc[0]["open"])
    gap_d   = next_open - fri_close
    gap_pct = (gap_d / fri_close) * 100
    flag    = ("RE-FORECAST" if abs(gap_pct) > 1.00 else
               "WARNING"     if abs(gap_pct) > 0.50 else
               "NOTE"        if abs(gap_pct) > 0.20 else "NOISE")
    return {"fri_date": str(last_fri_ts), "fri_close": round(fri_close,2),
            "next_date": str(next_ts),     "next_open": round(next_open,2),
            "gap_$": round(gap_d,2),       "gap_pct": round(gap_pct,3), "flag": flag}

# ── STEP 5: EXTERNAL FETCHES (no API key) ────────────────────────────────────

def volume_profile(ticker="GC=F", period="3mo", bins=50):
    try:
        df = yf.download(ticker, period=period, interval="1d", progress=False, auto_adjust=True)
        if df.empty:
            return {"error": "empty"}
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        edges = np.linspace(float(df["Low"].min()), float(df["High"].max()), bins+1)
        vols  = np.zeros(bins)
        for _, row in df.iterrows():
            lo, hi, vol = float(row["Low"]), float(row["High"]), float(row["Volume"])
            br = hi - lo
            if br == 0 or vol == 0:
                continue
            for i in range(bins):
                ov = min(hi, edges[i+1]) - max(lo, edges[i])
                if ov > 0:
                    vols[i] += vol * (ov / br)
        poc_idx = int(np.argmax(vols))
        poc = round((edges[poc_idx]+edges[poc_idx+1])/2, 2)
        total = vols.sum(); target = total*0.70
        lo_i = hi_i = poc_idx; acc = vols[poc_idx]
        while acc < target and (lo_i > 0 or hi_i < bins-1):
            add_lo = vols[lo_i-1] if lo_i > 0 else 0
            add_hi = vols[hi_i+1] if hi_i < bins-1 else 0
            if add_lo >= add_hi and lo_i > 0: lo_i -= 1; acc += add_lo
            elif hi_i < bins-1:               hi_i += 1; acc += add_hi
            else:                             lo_i -= 1; acc += add_lo
        return {"POC": poc, "VAH": round(edges[hi_i+1],2), "VAL": round(edges[lo_i],2)}
    except Exception as e:
        return {"error": str(e)}

def fetch_cot():
    try:
        url = ("https://publicreporting.cftc.gov/resource/6dca-aqww.json"
               "?$where=cftc_commodity_code='088691'"
               "&$order=report_date_as_yyyy_mm_dd DESC&$limit=4")
        rows = requests.get(url, timeout=15).json()
        if not rows:
            return None
        latest = rows[0]; prev = rows[1] if len(rows) > 1 else None
        net_now  = int(latest.get("noncomm_positions_long_all",0)) - int(latest.get("noncomm_positions_short_all",0))
        net_prev = (int(prev.get("noncomm_positions_long_all",0)) - int(prev.get("noncomm_positions_short_all",0))) if prev else None
        return {"date": latest.get("report_date_as_yyyy_mm_dd","")[:10],
                "long": int(latest.get("noncomm_positions_long_all",0)),
                "short": int(latest.get("noncomm_positions_short_all",0)),
                "net": net_now, "net_prev": net_prev,
                "net_chg": (net_now-net_prev) if net_prev is not None else None}
    except Exception as e:
        return {"error": str(e)}

def fetch_gld_flows():
    try:
        r = requests.get("https://www.spdrgoldshares.com/assets/dynamic/GLD/GLD_US_archive_EN.csv",
                         timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        lines = r.text.splitlines()
        hidx = next((i for i, ln in enumerate(lines)
                     if "date" in ln.lower() and ("tonne" in ln.lower() or "ounce" in ln.lower())), None)
        if hidx is None:
            return {"error": "header not found"}
        df = pd.read_csv(StringIO("\n".join(lines[hidx:])))
        dcol = next(c for c in df.columns if "date"  in c.lower())
        tcol = next((c for c in df.columns if "tonne" in c.lower()), None)
        if tcol is None:
            return {"error": "tonnes column not found"}
        df[dcol] = pd.to_datetime(df[dcol], errors="coerce")
        df[tcol] = pd.to_numeric(df[tcol].astype(str).str.replace(",",""), errors="coerce")
        df = df.dropna(subset=[dcol,tcol]).sort_values(dcol).reset_index(drop=True)
        if df.empty:
            return {"error": "empty after parse"}
        lat = df.iloc[-1]
        wk  = df.iloc[-6]  if len(df) >= 6  else None
        mo  = df.iloc[-21] if len(df) >= 21 else None
        return {"date": lat[dcol].strftime("%Y-%m-%d"), "tonnes": round(float(lat[tcol]),2),
                "wk_chg": round(float(lat[tcol])-float(wk[tcol]),2) if wk is not None else None,
                "mo_chg": round(float(lat[tcol])-float(mo[tcol]),2) if mo is not None else None}
    except Exception as e:
        return {"error": str(e)}

# ── MAIN ──────────────────────────────────────────────────────────────────────

def fetch_and_update(force=False):
    """Fetch 15M bars, resample, update FRED CSVs. Returns brief status lines.
    Called by both run() and --fetch-only mode (used by /validate)."""
    if not TWELVE_KEY or not FRED_KEY:
        print("ERROR: TWELVE_DATA_KEY or FRED_KEY not set in .env"); sys.exit(1)

    print("Fetching 15M bars from Twelve Data (1 API call)...")
    new_15m  = fetch_15m(force=force)
    info_15m = upsert("twelvedata", SYMBOL, "15min", new_15m)
    print(f"  → {len(new_15m)} new 15M bars | last: {info_15m['last_dt']}")
    print("Resampling 15min → 1h / 4h / 1day...")
    resample_results = resample_all()
    for tf, rows, last in resample_results:
        print(f"  → {tf}: {rows} rows | last: {last}")
    print("Updating FRED CSVs...")
    fred_results = update_fred(force=force)
    for sid, n, last in fred_results:
        print(f"  → {sid}: {n} new | last: {last}")
    print("✅ CSVs ready.")
    return info_15m


def run(force=False):
    out_path = PULL_DIR / f"weekly_pull_{YEAR}_W{WEEK_NUM:02d}.txt"
    if out_path.exists() and not force:
        size  = out_path.stat().st_size
        mtime = datetime.fromtimestamp(out_path.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"✅ Cache hit: {out_path} ({size} bytes, generated {mtime})")
        print("   Skipping fetch. Use --force to refetch.")
        return str(out_path)

    # 1. Fetch + resample + FRED
    fetch_and_update(force=force)

    # 2. Load local data
    print("Computing indicators...")
    gold_d       = load_ohlc(TD_DIR / "1day.csv")
    gold_h4_full = load_ohlc(TD_DIR / "4h.csv")
    gold_h4      = gold_h4_full[gold_h4_full.index.dayofweek < 5]  # trading days only

    # 4. External fetches
    print("  → Volume Profile (yfinance GC=F)...")
    vp  = volume_profile()
    print("  → COT (CFTC)...")
    cot = fetch_cot()
    print("  → GLD ETF flows (SPDR)...")
    gld = fetch_gld_flows()

    # 5. Indicators
    atr_d  = calc_atr(gold_d)
    atr_h4 = calc_atr(gold_h4)

    d1_atr_s   = calc_atr_series(gold_d)
    atr_d_now  = round(float(d1_atr_s.iloc[-1]), 2)
    atr_d_med  = round(float(d1_atr_s.iloc[-21:-1].median()), 2)
    compressed = atr_d_now < atr_d_med

    adx_val   = calc_adx(gold_d)
    ema50     = calc_ema(gold_d["close"], 50)
    ema200    = calc_ema(gold_d["close"], 200)
    rsi_vals  = calc_rsi_series(gold_d)
    macd_rows = calc_macd(gold_d)
    gap       = weekend_gap(gold_h4_full, gold_h4)
    pvt       = calc_pivots(gold_d)
    sh, sl    = swing_points(gold_d)
    sh_h4, sl_h4 = swing_points(gold_h4)

    rec_hi = sh[-1][1] if sh else float(gold_d["high"].tail(30).max())
    rec_lo = sl[-1][1] if sl else float(gold_d["low"].tail(30).min())
    fibs   = fib_levels(rec_lo, rec_hi)

    # FRED derived
    ry  = load_fred_local("DFII10"); ny  = load_fred_local("DGS10")
    be  = load_fred_local("T5YIE");  ff  = load_fred_local("DFF")
    dxy = load_fred_local("DTWEXBGS"); vix = load_fred_local("VIXCLS")

    gc = float(gold_d["close"].iloc[-1]); gp = float(gold_d["close"].iloc[-6])
    dc = float(dxy["value"].iloc[-1]);    dp = float(dxy["value"].iloc[-6])
    ry_now  = float(ry["value"].iloc[-1]); ry_prev = float(ry["value"].iloc[-6])
    ry_20d  = ry["value"].iloc[-21:]
    ry_slope = float(np.polyfit(range(len(ry_20d)), ry_20d.values, 1)[0])
    ry_drift = ry_now - float(ry["value"].iloc[-2])

    risk_unit = round(min(atr_h4, 0.5*atr_d), 2)
    lots_raw  = round(2000 / (risk_unit*100), 3)
    lots_fl   = int(lots_raw*100) / 100

    adx_regime = ("TRENDING (favor continuation/breakout setups)"  if adx_val > 25  else
                  "TRANSITIONAL (require 6.5/10+ score minimum)"   if adx_val >= 20 else
                  "RANGING (favor reversal setups at zone edges)")

    rsi_now = rsi_vals[-1][1]; rsi_old = rsi_vals[0][1]

    # Format blocks
    if cot and "error" not in cot:
        net_str = f"{cot['net']:+,}"; chg_str = f"{cot['net_chg']:+,}" if cot["net_chg"] is not None else "N/A"
        cot_block = (f"━━━ COT — CFTC GOLD FUTURES (non-commercial, as of {cot['date']}) ━━━━━━\n"
                     f"Spec Long:      {cot['long']:,}\nSpec Short:     {cot['short']:,}\n"
                     f"Net Position:   {net_str}  ({'BULLISH (spec long)' if cot['net']>0 else 'BEARISH (spec short)'})\n"
                     f"W/W Change:     {chg_str}  ({'INCREASING' if (cot['net_chg'] or 0)>0 else 'DECREASING'})\n"
                     f"Note: extreme net longs (>200k) = crowded = reversal risk")
    else:
        cot_block = f"━━━ COT — CFTC GOLD FUTURES ━━━━━━━━━━━━━━━━━━━━━━━━━━\nFetch failed: {(cot or {}).get('error','no data')}"

    if gld and "error" not in gld:
        wk = f"{gld['wk_chg']:+}" if gld["wk_chg"] is not None else "N/A"
        mo = f"{gld['mo_chg']:+}" if gld["mo_chg"] is not None else "N/A"
        bias = "INFLOW (bullish)" if (gld["wk_chg"] or 0) > 0 else "OUTFLOW (bearish)" if (gld["wk_chg"] or 0) < 0 else "FLAT"
        gld_block = (f"━━━ ETF FLOWS — SPDR GLD (tonnes held, as of {gld['date']}) ━━━\n"
                     f"Tonnes:         {gld['tonnes']}\n1w Δ tonnes:    {wk}  ({bias})\n4w Δ tonnes:    {mo}\n"
                     f"Note: persistent outflows during macro BEARISH = confirmation. Inflows against bias = warning.")
    else:
        gld_block = f"━━━ ETF FLOWS — SPDR GLD ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nFetch failed: {(gld or {}).get('error','no data')}"

    if gap and "error" not in gap:
        gap_block = (f"━━━ WEEKEND GLOBEX GAP ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                     f"Fri close:   ${gap['fri_close']}  ({gap['fri_date']})\n"
                     f"Sun reopen:  ${gap['next_open']}  ({gap['next_date']})\n"
                     f"Gap:         ${gap['gap_$']}  ({gap['gap_pct']:+}%)  → {gap['flag']}\n"
                     f"Thresholds: <0.20% NOISE | 0.20–0.50% NOTE | 0.50–1.00% WARNING | >1.00% RE-FORECAST")
    else:
        gap_block = "━━━ WEEKEND GLOBEX GAP ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nNo Sunday reopen bar found"

    vp_block = (f"VAH: ${vp['VAH']}\nPOC: ${vp['POC']}  ← highest volume node\nVAL: ${vp['VAL']}"
                if "error" not in vp else f"VP fetch failed: {vp['error']}")

    out = f"""
╔══════════════════════════════════════════════════════╗
  XAUUSD WEEKLY DATA — {TODAY.strftime('%Y-%m-%d')} (W{WEEK_NUM})
╚══════════════════════════════════════════════════════╝

━━━ MACRO ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fed Funds:        {float(ff['value'].iloc[-1]):.2f}%
10Y Nominal:      {float(ny['value'].iloc[-1]):.2f}%
10Y Real (TIPS):  {ry_now}% (was {ry_prev}% ~1w ago, Δ {round(ry_now-ry_prev,3):+}%)
  → {"RISING ⚠  (bearish gold)" if ry_now > ry_prev else "FALLING ✅ (bullish gold)"}
  20d slope: {ry_slope:+.4f} %/day  {"(rising trend)" if ry_slope > 0 else "(falling trend)"}
  1d drift:  {ry_drift:+.3f}%
5Y Breakeven:     {float(be['value'].iloc[-1]):.2f}%
VIX:              {float(vix['value'].iloc[-1]):.2f}

━━━ PRICE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Gold:             ${gc:.2f} (was ${gp:.2f}, {round(((gc/gp)-1)*100,2):+.2f}% ~1w chg)
USD Index (FRED): {dc:.3f}  (was {dp:.3f},  {round(((dc/dp)-1)*100,2):+.2f}% ~1w chg)

━━━ INDICATORS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATR(14) Daily:    ${atr_d}
ATR(14) H4:       ${atr_h4}  (trading days only)
risk_unit:        ${risk_unit} = min(H4 ATR ${atr_h4}, 0.5× Daily ATR ${round(0.5*atr_d,2)})
D1 ATR now:       ${atr_d_now} | 20d median: ${atr_d_med} → {"COMPRESSED ✅" if compressed else "EXPANDING ⚠"}

Lot sizing ($2000 risk):
  Raw lots:  {lots_raw}
  Use lots:  {lots_fl}  (rounded DOWN)

ADX(14) D1:       {adx_val} → {adx_regime}
EMA 50 D1:        ${ema50} | Price {"ABOVE" if gc > ema50 else "BELOW"}
EMA 200 D1:       ${ema200} | Price {"ABOVE" if gc > ema200 else "BELOW"}
RSI(14) D1:       {rsi_now} (was {rsi_old} 10 bars ago, {"rising" if rsi_now > rsi_old else "falling"})

RSI D1 (last 10 bars):
{chr(10).join([f"  {v[0]}: {v[1]}" for v in rsi_vals])}

MACD(12,26,9) D1 — last 5 bars:
  {"Date":<12} {"MACD":>8} {"Signal":>8} {"Hist":>8}
{chr(10).join([f"  {r[0]:<12} {r[1]:>8} {r[2]:>8} {r[3]:>8}" for r in macd_rows])}
  Histogram {"POSITIVE (bullish momentum)" if macd_rows[-1][3] > 0 else "NEGATIVE (bearish momentum)"}
  Cross: {"MACD above signal (bullish)" if macd_rows[-1][1] > macd_rows[-1][2] else "MACD below signal (bearish)"}

━━━ VOLUME PROFILE (CME GC=F, 3mo daily) ━━━━━━━━━━━━
{vp_block}
Signal 7 check: zone within $8 of POC/VAH/VAL = confluent

{cot_block}

{gld_block}

{gap_block}

━━━ BASELINES (snapshot for forecast frontmatter) ━━━━
baseline_dfii10: {ry_now}
baseline_dxy:    {dc:.3f}
weekend_gap_pct: {gap['gap_pct'] if gap and 'gap_pct' in gap else 'N/A'}

━━━ WEEKLY PIVOTS (prior week OHLC) ━━━━━━━━━━━━━━━━━━
R3:{pvt['R3']}  R2:{pvt['R2']}  R1:{pvt['R1']}
PP:{pvt['PP']}
S1:{pvt['S1']}  S2:{pvt['S2']}  S3:{pvt['S3']}

━━━ SWING POINTS (Daily, N=5) ━━━━━━━━━━━━━━━━━━━━━━━━
Highs: {' | '.join([f"${h[1]}({h[0]})" for h in sh])}
Lows:  {' | '.join([f"${l[1]}({l[0]})" for l in sl])}

━━━ SWING POINTS (H4, N=5, trading days) ━━━━━━━━━━━━━
Highs: {' | '.join([f"${h[1]}({h[0]})" for h in sh_h4])}
Lows:  {' | '.join([f"${l[1]}({l[0]})" for l in sl_h4])}

━━━ FIBONACCI (anchored to last D1 swing high/low) ━━━
Swing: ${fibs['swing_low']} → ${fibs['swing_high']}
  78.6%:      ${fibs['78.6%']}
  61.8%:      ${fibs['61.8%']}  ← golden pocket
  50.0%:      ${fibs['50.0%']}
  38.2%:      ${fibs['38.2%']}
  Ext 127.2%: ${fibs['ext_127.2%']}
  Ext 161.8%: ${fibs['ext_161.8%']}  ← TP extension zone

━━━ DAILY OHLCV — last 15 bars ━━━━━━━━━━━━━━━━━━━━━━━
{gold_d[['open','high','low','close']].tail(15).round(2).to_string()}

━━━ H4 OHLCV — last 24 bars (trading days) ━━━━━━━━━━━
{gold_h4[['open','high','low','close']].tail(24).round(2).to_string()}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    PULL_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out)
    print(out)
    print(f"✅ Saved to {out_path}")
    return str(out_path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Re-fetch full history")
    args = ap.parse_args()
    run(force=args.force)
