"""
XAUUSD Weekly Data Pull
Run every Sunday before market open.
Output: data/weekly_pull/weekly_pull_{YEAR}_W{WEEK_NUM}.txt

Requirements: pip install requests pandas yfinance python-dotenv
"""

import os
import sys
import argparse
import requests
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

TWELVE_KEY = os.getenv("TWELVE_DATA_KEY")
FRED_KEY   = os.getenv("FRED_KEY")

TODAY     = datetime.today()
MONTH_AGO = (TODAY - timedelta(days=35)).strftime("%Y-%m-%d")
WEEK_NUM  = TODAY.isocalendar()[1]
YEAR      = TODAY.year

# ── HELPERS ────────────────────────────────────────────────────────────────────

def twelve(endpoint, params):
    params["apikey"] = TWELVE_KEY
    r = requests.get(f"https://api.twelvedata.com/{endpoint}", params=params, timeout=10)
    data = r.json()
    if "code" in data and data["code"] != 200:
        raise ValueError(f"Twelve Data [{endpoint}]: {data.get('message', data)}")
    return data

def fred(series_id):
    r = requests.get(
        "https://api.stlouisfed.org/fred/series/observations",
        params={"series_id": series_id, "observation_start": MONTH_AGO,
                "api_key": FRED_KEY, "file_type": "json"},
        timeout=10
    )
    obs = r.json().get("observations", [])
    df = pd.DataFrame(obs)[["date", "value"]]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df.dropna().reset_index(drop=True)

def ohlcv(data):
    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.set_index("datetime").sort_index()
    for col in ["open", "high", "low", "close"]:
        df[col] = pd.to_numeric(df[col])
    return df

def calc_atr(df, p=14):
    h, l, c = df["high"], df["low"], df["close"]
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    return round(tr.rolling(p).mean().iloc[-1], 2)

def calc_pivots(weekly_df):
    """Use prior week OHLC — pass resampled weekly dataframe."""
    b = weekly_df.iloc[-2]
    pp = (b["high"] + b["low"] + b["close"]) / 3
    return {
        "PP": round(pp, 2),
        "R1": round(2 * pp - b["low"], 2),
        "R2": round(pp + b["high"] - b["low"], 2),
        "R3": round(b["high"] + 2 * (pp - b["low"]), 2),
        "S1": round(2 * pp - b["high"], 2),
        "S2": round(pp - b["high"] + b["low"], 2),
        "S3": round(b["low"] - 2 * (b["high"] - pp), 2),
    }

def swing_points(df, n=5):
    highs, lows = [], []
    for i in range(n, len(df) - n):
        if df["high"].iloc[i] == df["high"].iloc[i - n:i + n + 1].max():
            highs.append((df.index[i].strftime("%Y-%m-%d"), round(df["high"].iloc[i], 2)))
        if df["low"].iloc[i] == df["low"].iloc[i - n:i + n + 1].min():
            lows.append((df.index[i].strftime("%Y-%m-%d"), round(df["low"].iloc[i], 2)))
    return highs[-5:], lows[-5:]

def fib_levels(lo, hi):
    d = hi - lo
    return {
        "swing_low": round(lo, 2), "swing_high": round(hi, 2),
        "78.6%":      round(hi - 0.786 * d, 2),
        "61.8%":      round(hi - 0.618 * d, 2),
        "50.0%":      round(hi - 0.500 * d, 2),
        "38.2%":      round(hi - 0.382 * d, 2),
        "ext_127.2%": round(lo + 1.272 * d, 2),
        "ext_161.8%": round(lo + 1.618 * d, 2),
    }

def volume_profile(ticker="GC=F", period="3mo", bins=50):
    df = yf.download(ticker, period=period, interval="1d", progress=False, auto_adjust=True)
    if df.empty:
        return {"POC": "N/A", "VAH": "N/A", "VAL": "N/A"}
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    price_min = float(df["Low"].min().item() if hasattr(df["Low"].min(), "item") else df["Low"].min())
    price_max = float(df["High"].max().item() if hasattr(df["High"].max(), "item") else df["High"].max())
    bucket_edges = np.linspace(price_min, price_max, bins + 1)
    vol_per_bucket = np.zeros(bins)
    for _, row in df.iterrows():
        lo  = float(row["Low"].item()    if hasattr(row["Low"],    "item") else row["Low"])
        hi  = float(row["High"].item()   if hasattr(row["High"],   "item") else row["High"])
        vol = float(row["Volume"].item() if hasattr(row["Volume"], "item") else row["Volume"])
        bar_range = hi - lo
        if bar_range == 0 or vol == 0:
            continue
        for i in range(bins):
            overlap = min(hi, bucket_edges[i + 1]) - max(lo, bucket_edges[i])
            if overlap > 0:
                vol_per_bucket[i] += vol * (overlap / bar_range)
    poc_idx = int(np.argmax(vol_per_bucket))
    poc = round((bucket_edges[poc_idx] + bucket_edges[poc_idx + 1]) / 2, 2)
    total_vol = vol_per_bucket.sum()
    target = total_vol * 0.70
    lo_i = hi_i = poc_idx
    accumulated = vol_per_bucket[poc_idx]
    while accumulated < target and (lo_i > 0 or hi_i < bins - 1):
        add_lo = vol_per_bucket[lo_i - 1] if lo_i > 0 else 0
        add_hi = vol_per_bucket[hi_i + 1] if hi_i < bins - 1 else 0
        if add_lo >= add_hi and lo_i > 0:
            lo_i -= 1; accumulated += add_lo
        elif hi_i < bins - 1:
            hi_i += 1; accumulated += add_hi
        else:
            lo_i -= 1; accumulated += add_lo
    return {"POC": poc, "VAH": round(bucket_edges[hi_i + 1], 2), "VAL": round(bucket_edges[lo_i], 2)}

def fetch_gld_flows():
    """SPDR GLD daily holdings CSV. Auto-fetch. Compute Δtonnes 1w / 4w."""
    try:
        url = "https://www.spdrgoldshares.com/assets/dynamic/GLD/GLD_US_archive_EN.csv"
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        text = r.text
        lines = text.splitlines()
        header_idx = next((i for i, line in enumerate(lines)
                           if "date" in line.lower() and ("tonne" in line.lower() or "ounce" in line.lower())), None)
        if header_idx is None:
            return {"error": "header row not found"}
        df = pd.read_csv(StringIO("\n".join(lines[header_idx:])))
        date_col  = next(c for c in df.columns if "date"  in c.lower())
        tonne_col = next((c for c in df.columns if "tonne" in c.lower()), None)
        if tonne_col is None:
            return {"error": "tonnes column not found"}
        df[date_col]  = pd.to_datetime(df[date_col], errors="coerce")
        df[tonne_col] = pd.to_numeric(df[tonne_col].astype(str).str.replace(",", ""), errors="coerce")
        df = df.dropna(subset=[date_col, tonne_col]).sort_values(date_col).reset_index(drop=True)
        if df.empty:
            return {"error": "empty after parse"}
        latest = df.iloc[-1]
        wk = df.iloc[-6]  if len(df) >= 6  else None
        mo = df.iloc[-21] if len(df) >= 21 else None
        return {
            "date":    latest[date_col].strftime("%Y-%m-%d"),
            "tonnes":  round(float(latest[tonne_col]), 2),
            "wk_chg":  round(float(latest[tonne_col]) - float(wk[tonne_col]), 2) if wk is not None else None,
            "mo_chg":  round(float(latest[tonne_col]) - float(mo[tonne_col]), 2) if mo is not None else None,
        }
    except Exception as e:
        return {"error": str(e)}

def weekend_gap(h4_df):
    """Friday last bar close vs first bar after Sunday reopen. Uses H4 dataframe."""
    try:
        df = h4_df.copy()
        df["dow"] = df.index.dayofweek  # Mon=0 … Fri=4, Sat=5, Sun=6
        fri = df[df["dow"] == 4]
        if fri.empty:
            return None
        last_fri_bar = fri.iloc[-1]
        last_fri_ts  = fri.index[-1]
        fri_close    = float(last_fri_bar["close"])
        after = df[df.index > last_fri_ts]
        if after.empty:
            return None
        next_bar  = after.iloc[0]
        next_ts   = after.index[0]
        next_open = float(next_bar["open"])
        gap_d   = next_open - fri_close
        gap_pct = (gap_d / fri_close) * 100
        if   abs(gap_pct) > 1.00: flag = "RE-FORECAST"
        elif abs(gap_pct) > 0.50: flag = "WARNING"
        elif abs(gap_pct) > 0.20: flag = "NOTE"
        else:                     flag = "NOISE"
        return {
            "fri_date":  last_fri_ts.strftime("%Y-%m-%d %H:%M"),
            "fri_close": round(fri_close, 2),
            "next_date": next_ts.strftime("%Y-%m-%d %H:%M"),
            "next_open": round(next_open, 2),
            "gap_$":     round(gap_d, 2),
            "gap_pct":   round(gap_pct, 3),
            "flag":      flag,
        }
    except Exception as e:
        return {"error": str(e)}

def fetch_cot():
    """CFTC Commitments of Traders — gold futures (COMEX, code 088691). Returns latest 4 weeks."""
    try:
        url = (
            "https://publicreporting.cftc.gov/resource/6dca-aqww.json"
            "?$where=cftc_commodity_code='088691'"
            "&$order=report_date_as_yyyy_mm_dd DESC"
            "&$limit=4"
        )
        r = requests.get(url, timeout=15)
        rows = r.json()
        if not rows:
            return None
        latest = rows[0]
        prev   = rows[1] if len(rows) > 1 else None
        net_now  = int(latest.get("noncomm_positions_long_all", 0)) - int(latest.get("noncomm_positions_short_all", 0))
        net_prev = (int(prev.get("noncomm_positions_long_all", 0)) - int(prev.get("noncomm_positions_short_all", 0))) if prev else None
        return {
            "date":      latest.get("report_date_as_yyyy_mm_dd", "")[:10],
            "long":      int(latest.get("noncomm_positions_long_all", 0)),
            "short":     int(latest.get("noncomm_positions_short_all", 0)),
            "net":       net_now,
            "net_prev":  net_prev,
            "net_chg":   (net_now - net_prev) if net_prev is not None else None,
        }
    except Exception as e:
        return {"error": str(e)}

# ── MAIN ──────────────────────────────────────────────────────────────────────

def run(force: bool = False):
    out_path = f"data/weekly_pull/weekly_pull_{YEAR}_W{WEEK_NUM:02d}.txt"
    if os.path.exists(out_path) and not force:
        size = os.path.getsize(out_path)
        mtime = datetime.fromtimestamp(os.path.getmtime(out_path)).strftime("%Y-%m-%d %H:%M")
        print(f"✅ Cache hit: {out_path} ({size} bytes, generated {mtime})")
        print("   Skipping fetch. Use --force to refetch.")
        return out_path

    print("Fetching data...")

    print("  → Volume Profile (CME GC)...")
    vp = volume_profile()

    print("  → COT (CFTC gold futures)...")
    cot = fetch_cot()

    print("  → GLD ETF flows (SPDR)...")
    gld = fetch_gld_flows()

    print("  → Price + indicators (Twelve Data)...")
    gold_d  = ohlcv(twelve("time_series", {"symbol": "XAU/USD", "interval": "1day", "outputsize": 60}))
    gold_h4 = ohlcv(twelve("time_series", {"symbol": "XAU/USD", "interval": "4h",   "outputsize": 120}))

    print("  → Weekend Globex gap...")
    gap = weekend_gap(gold_h4)

    atr_d   = float(twelve("atr",  {"symbol": "XAU/USD", "interval": "1day", "time_period": 14, "outputsize": 1})["values"][0]["atr"])
    atr_h4  = float(twelve("atr",  {"symbol": "XAU/USD", "interval": "4h",   "time_period": 14, "outputsize": 1})["values"][0]["atr"])
    adx_val = float(twelve("adx",  {"symbol": "XAU/USD", "interval": "1day", "time_period": 14, "outputsize": 1})["values"][0]["adx"])

    rsi_raw  = twelve("rsi",  {"symbol": "XAU/USD", "interval": "1day", "time_period": 14, "outputsize": 10})["values"]
    rsi_vals = [(v["datetime"][:10], round(float(v["rsi"]), 1)) for v in rsi_raw]

    macd_raw = twelve("macd", {"symbol": "XAU/USD", "interval": "1day",
                               "fast_period": 12, "slow_period": 26, "signal_period": 9,
                               "outputsize": 5})["values"]
    macd_rows = [(v["datetime"][:10],
                  round(float(v["macd"]), 2),
                  round(float(v["macd_signal"]), 2),
                  round(float(v["macd_hist"]), 2)) for v in macd_raw]

    ema50  = float(twelve("ema", {"symbol": "XAU/USD", "interval": "1day", "time_period": 50,  "outputsize": 1})["values"][0]["ema"])
    ema200 = float(twelve("ema", {"symbol": "XAU/USD", "interval": "1day", "time_period": 200, "outputsize": 1})["values"][0]["ema"])

    print("  → FRED macro series...")
    ry  = fred("DFII10")
    ny  = fred("DGS10")
    be  = fred("T5YIE")
    ff  = fred("DFF")
    dxy = fred("DTWEXBGS")

    # ── DERIVED ──────────────────────────────────────────────────────────────
    gc = gold_d["close"].iloc[-1]
    gp = gold_d["close"].iloc[-5]
    dc = dxy["value"].iloc[-1]
    dp = dxy["value"].iloc[-5]
    ry_now, ry_prev = ry["value"].iloc[-1], ry["value"].iloc[-5]

    atr_d   = round(atr_d, 2)
    atr_h4  = round(atr_h4, 2)
    adx_val = round(adx_val, 1)
    stop_distance = round(min(atr_h4, 0.5 * atr_d), 2)

    # Weekly pivot from prior week OHLC
    gold_w = gold_d.resample("W").agg({"open": "first", "high": "max", "low": "min", "close": "last"})
    pvt = calc_pivots(gold_w)

    # Swing points
    sh, sl = swing_points(gold_d)

    # Fib anchored to most recent identified swing high/low
    if sh and sl:
        recent_high = sh[-1][1]
        recent_low  = sl[-1][1]
        fibs = fib_levels(recent_low, recent_high)
    else:
        fibs = fib_levels(gold_d["low"].tail(30).min(), gold_d["high"].tail(30).max())

    rsi_now, rsi_old = rsi_vals[0][1], rsi_vals[-1][1]

    # ADX regime label
    if adx_val > 25:
        adx_regime = "TRENDING (favor continuation/breakout setups)"
    elif adx_val >= 20:
        adx_regime = "TRANSITIONAL (require 4+ signals minimum)"
    else:
        adx_regime = "RANGING (favor reversal setups at zone edges)"

    # Stop sizing — unified: risk_unit = min(H4 ATR, 0.5 × Daily ATR), no widening
    # Upper cap only: if H4 ATR > 1.5 × Daily ATR → skip trade (vol regime broken)
    risk_unit = stop_distance
    buffer_per_signal = round(0.25 * risk_unit, 2)
    if atr_h4 > 1.5 * atr_d:
        stop_note = f"SKIP — H4 ATR ${atr_h4} > 1.5× Daily ATR ${round(1.5*atr_d,2)} (vol regime broken)"
    else:
        stop_note = f"OK — risk_unit ${risk_unit}, buffer ${buffer_per_signal}/signal"

    # Lot sizing at $2000 risk
    lots_raw     = round(2000 / (stop_distance * 100), 3)
    lots_rounded = round(int(lots_raw * 100) / 100, 2)

    # COT formatting
    if cot and "error" not in cot:
        cot_net_str  = f"{cot['net']:+,}"
        cot_chg_str  = f"{cot['net_chg']:+,}" if cot["net_chg"] is not None else "N/A"
        cot_bias = "BULLISH (spec long)" if cot["net"] > 0 else "BEARISH (spec short)"
        if cot["net_chg"] is not None:
            cot_trend = "INCREASING" if cot["net_chg"] > 0 else "DECREASING"
        else:
            cot_trend = "N/A"
        cot_block = f"""━━━ COT — CFTC GOLD FUTURES (non-commercial, as of {cot['date']}) ━━━━━━
Spec Long:      {cot['long']:,}
Spec Short:     {cot['short']:,}
Net Position:   {cot_net_str}  ({cot_bias})
W/W Change:     {cot_chg_str}  ({cot_trend})
Note: extreme net longs (>200k) = crowded = reversal risk"""
    else:
        err = cot.get("error", "no data") if cot else "no data"
        cot_block = f"━━━ COT — CFTC GOLD FUTURES ━━━━━━━━━━━━━━━━━━━━━━━━━━\nFetch failed: {err}"

    # GLD block
    if gld and "error" not in gld:
        gld_wk = f"{gld['wk_chg']:+}" if gld["wk_chg"] is not None else "N/A"
        gld_mo = f"{gld['mo_chg']:+}" if gld["mo_chg"] is not None else "N/A"
        gld_bias = "INFLOW (bullish)" if (gld["wk_chg"] or 0) > 0 else "OUTFLOW (bearish)" if (gld["wk_chg"] or 0) < 0 else "FLAT"
        gld_block = f"""━━━ ETF FLOWS — SPDR GLD (tonnes held, as of {gld['date']}) ━━━
Tonnes:         {gld['tonnes']}
1w Δ tonnes:    {gld_wk}  ({gld_bias})
4w Δ tonnes:    {gld_mo}
Note: persistent outflows during macro BEARISH = confirmation. Inflows against bias = warning."""
    else:
        err = gld.get("error", "no data") if gld else "no data"
        gld_block = f"━━━ ETF FLOWS — SPDR GLD ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\nFetch failed: {err}"

    # Weekend gap block
    if gap and "error" not in gap and gap is not None:
        gap_block = f"""━━━ WEEKEND GLOBEX GAP ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fri close:   ${gap['fri_close']}  ({gap['fri_date']})
Sun reopen:  ${gap['next_open']}  ({gap['next_date']})
Gap:         ${gap['gap_$']}  ({gap['gap_pct']:+}%)  → {gap['flag']}
Thresholds: <0.20% NOISE | 0.20–0.50% NOTE | 0.50–1.00% WARNING | >1.00% RE-FORECAST"""
    else:
        err = gap.get("error", "no gap (no Friday bar)") if isinstance(gap, dict) else "no data"
        gap_block = f"━━━ WEEKEND GLOBEX GAP ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n{err}"

    out = f"""
╔══════════════════════════════════════════════════════╗
  XAUUSD WEEKLY DATA — {TODAY.strftime('%Y-%m-%d')} (W{WEEK_NUM})
╚══════════════════════════════════════════════════════╝

━━━ MACRO ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Fed Funds:        {ff["value"].iloc[-1]}%
10Y Nominal:      {ny["value"].iloc[-1]}%
10Y Real (TIPS):  {ry_now}% (was {ry_prev}% ~1w ago, Δ {round(ry_now-ry_prev,3)}%)
  → {"RISING ⚠️  (bearish gold)" if ry_now > ry_prev else "FALLING ✅ (bullish gold)"}
5Y Breakeven:     {be["value"].iloc[-1]}%

━━━ PRICE ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Gold:             ${gc:.2f} (was ${gp:.2f}, {round(((gc/gp)-1)*100,2)}% 1w chg)
USD Index (FRED): {dc:.3f}  (was {dp:.3f},  {round(((dc/dp)-1)*100,2)}% 1w chg)

━━━ INDICATORS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATR(14) Daily:    ${atr_d}
ATR(14) H4:       ${atr_h4}
risk_unit:        ${risk_unit} = min(H4 ATR ${atr_h4}, 0.5× Daily ATR ${round(0.5*atr_d,2)}) → {stop_note}
Stop distance:    ${risk_unit} (= risk_unit, no widening)
Offset buffer:    ${buffer_per_signal} per missing signal (0.25 × risk_unit)
Vol regime cap:   H4 ATR must be ≤ 1.5× Daily ATR (${round(1.5*atr_d,2)}) — else skip trade

Lot sizing ($2000 risk):
  Raw lots:  {lots_raw}
  Use lots:  {lots_rounded}  (rounded DOWN)

ADX(14):          {adx_val} → {adx_regime}

EMA 50:           ${round(ema50,2)} | Price {"ABOVE" if gc > ema50 else "BELOW"}
EMA 200:          ${round(ema200,2)} | Price {"ABOVE" if gc > ema200 else "BELOW"}
RSI(14):          {rsi_now} (was {rsi_old} 10 bars ago, {"rising" if rsi_now > rsi_old else "falling"})

RSI recent:
{chr(10).join([f"  {v[0]}: {v[1]}" for v in rsi_vals])}

MACD(12,26,9) Daily — last 5 bars:
  {'Date':<12} {'MACD':>8} {'Signal':>8} {'Hist':>8}
{chr(10).join([f"  {r[0]:<12} {r[1]:>8} {r[2]:>8} {r[3]:>8}" for r in macd_rows])}
  Histogram {"POSITIVE (bullish momentum)" if macd_rows[0][3] > 0 else "NEGATIVE (bearish momentum)"}
  Cross: {"MACD above signal (bullish)" if macd_rows[0][1] > macd_rows[0][2] else "MACD below signal (bearish)"}

━━━ VOLUME PROFILE (CME GC, 3mo daily approx) ━━━━━━━
VAH: ${vp['VAH']}
POC: ${vp['POC']}  ← highest volume node
VAL: ${vp['VAL']}
Signal 7 check: zone within $8 of POC/VAH/VAL = confluent

{cot_block}

{gld_block}

{gap_block}

━━━ BASELINES (snapshot for forecast frontmatter) ━━━━━
baseline_dfii10: {ry_now}
baseline_dxy:    {dc:.3f}
weekend_gap_pct: {gap['gap_pct'] if (gap and 'gap_pct' in gap) else 'N/A'}

━━━ WEEKLY PIVOTS (prior week OHLC) ━━━━━━━━━━━━━━━━━━
R3:{pvt['R3']}  R2:{pvt['R2']}  R1:{pvt['R1']}
PP:{pvt['PP']}
S1:{pvt['S1']}  S2:{pvt['S2']}  S3:{pvt['S3']}

━━━ SWING POINTS (Daily, N=5) ━━━━━━━━━━━━━━━━━━━━━━━━
Highs: {' | '.join([f"${h[1]}({h[0]})" for h in reversed(sh)])}
Lows:  {' | '.join([f"${l[1]}({l[0]})" for l in reversed(sl)])}

━━━ FIBONACCI (anchored to last swing high/low) ━━━━━━
Swing: ${fibs['swing_low']} → ${fibs['swing_high']}
  78.6%:      ${fibs['78.6%']}
  61.8%:      ${fibs['61.8%']}  ← golden pocket
  50.0%:      ${fibs['50.0%']}
  38.2%:      ${fibs['38.2%']}
  Ext 127.2%: ${fibs['ext_127.2%']}
  Ext 161.8%: ${fibs['ext_161.8%']}  ← TP zone (3R structural target)

━━━ DAILY OHLCV — last 15 bars ━━━━━━━━━━━━━━━━━━━━━━━
{gold_d[['open','high','low','close']].tail(15).round(2).to_string()}

━━━ H4 OHLCV — last 24 bars ━━━━━━━━━━━━━━━━━━━━━━━━━
{gold_h4[['open','high','low','close']].tail(24).round(2).to_string()}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    os.makedirs("data/weekly_pull", exist_ok=True)
    with open(out_path, "w") as f:
        f.write(out)
    print(out)
    print(f"✅ Saved to {out_path}")
    print("   Open Claude Code and run: /weekly")
    return out_path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Refetch even if this week's cache file exists")
    args = ap.parse_args()
    run(force=args.force)
