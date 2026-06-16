"""
OHLC storage helper. Source-segregated, atomic upsert, manifest-tracked.

Layout:
  data/{source}/{symbol}/{tf}.csv
  data/{source}/{symbol}/_manifest.json
"""
import os
import sys
import json
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # scripts/ for `db`

OHLC_COLS = ["datetime", "open", "high", "low", "close", "volume"]

# FX session (UTC): Sun 22:00 reopen → Fri 22:00 close. Sat closed.
# Daily TF: collapse to Mon-Fri only.
INTRADAY_TFS = {"15min", "15m", "1h", "60min", "1hour", "4h", "240min"}
DAILY_TFS    = {"1d", "1day", "daily", "D"}


def filter_trading_session(df: pd.DataFrame, tf: str, dt_col: str = "datetime") -> pd.DataFrame:
    """
    Drop bars outside the FX trading session. The time window is authoritative —
    provider-reported volume on weekend bars does NOT rescue them.

    Intraday: Mon-Thu all, Fri < 22:00 UTC, Sun >= 22:00 UTC (Globex reopen). No Sat.
    Daily: Mon-Fri only.
    Unknown TF: no filter (passthrough).
    """
    if df.empty:
        return df
    out = df.copy()
    ts  = pd.to_datetime(out[dt_col])
    dow = ts.dt.dayofweek
    hr  = ts.dt.hour

    if tf in DAILY_TFS:
        keep = dow < 5
    elif tf in INTRADAY_TFS:
        keep = (
            (dow < 4)
            | ((dow == 4) & (hr < 22))
            | ((dow == 6) & (hr >= 22))
        )
    else:
        return out

    return out[keep].reset_index(drop=True)

# Known source timezones. All TD data pulled with timezone=UTC → stored as UTC.
SOURCE_TZ = {
    "twelvedata": "UTC",
}

# ── Bad-tick guard ────────────────────────────────────────────────────────────
# Provider errors are order-of-magnitude (e.g. nzdusd D1 high 1.71632 on a 0.588
# pair, 2026-04-29 — falsely drove ADX 18.5 → 79.6). Real single-bar moves never
# approach these bounds: gold's worst daily swings are ~5%, FX majors ~3%.
BAD_TICK_MAX_DEV = {"daily": 0.10, "intraday": 0.05}
BAD_TICK_WINDOW  = 11   # centered rolling-median window for the local reference price


def quarantine_bad_ticks(df: pd.DataFrame, tf: str, quarantine_csv=None,
                         dt_col: str = "datetime") -> pd.DataFrame:
    """
    Detect and repair provider bad ticks against a local rolling-median reference.

    Reference = centered rolling median of close (window BAD_TICK_WINDOW). A bar is
    flagged when an extreme deviates more than BAD_TICK_MAX_DEV from the reference:
      - wick-only error (open+close sane): clamp high/low to the open/close body
      - body error (open or close insane): drop the bar entirely
    Every action is appended to `quarantine_csv` (deduped on tf+datetime+action)
    and printed. Unknown TF or <5 bars: passthrough.
    """
    if df.empty or len(df) < 5:
        return df
    if tf in DAILY_TFS:
        max_dev = BAD_TICK_MAX_DEV["daily"]
    elif tf in INTRADAY_TFS:
        max_dev = BAD_TICK_MAX_DEV["intraday"]
    else:
        return df

    out = df.reset_index(drop=True).copy()
    ref = out["close"].rolling(BAD_TICK_WINDOW, center=True, min_periods=3).median()
    upper, lower = ref * (1 + max_dev), ref * (1 - max_dev)

    hi_bad   = out["high"] > upper
    lo_bad   = out["low"]  < lower
    body_bad = (out["open"] > upper) | (out["open"] < lower) \
             | (out["close"] > upper) | (out["close"] < lower)
    wick_bad = (hi_bad | lo_bad) & ~body_bad

    if not (wick_bad.any() or body_bad.any()):
        return out

    records = []
    for i in out.index[wick_bad]:
        o, c = out.at[i, "open"], out.at[i, "close"]
        old_hi, old_lo = out.at[i, "high"], out.at[i, "low"]
        out.at[i, "high"] = max(o, c)
        out.at[i, "low"]  = min(o, c)
        records.append({"tf": tf, "datetime": str(out.at[i, dt_col]), "action": "clamp_wick",
                        "open": o, "high": old_hi, "low": old_lo, "close": c,
                        "ref_close": round(float(ref.iloc[i]), 6)})
    for i in out.index[body_bad]:
        records.append({"tf": tf, "datetime": str(out.at[i, dt_col]), "action": "drop_bar",
                        "open": out.at[i, "open"], "high": out.at[i, "high"],
                        "low": out.at[i, "low"], "close": out.at[i, "close"],
                        "ref_close": round(float(ref.iloc[i]), 6)})
    out = out[~body_bad].reset_index(drop=True)

    if quarantine_csv and records:
        rec_df = pd.DataFrame(records)
        rec_df["flagged_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        if os.path.exists(quarantine_csv):
            old_log = pd.read_csv(quarantine_csv, dtype=str)
            seen = set(zip(old_log["tf"], old_log["datetime"], old_log["action"]))
            rec_df = rec_df[~rec_df.apply(
                lambda r: (r["tf"], r["datetime"], r["action"]) in seen, axis=1)]
            if not rec_df.empty:
                rec_df.to_csv(quarantine_csv, mode="a", header=False, index=False)
        else:
            rec_df.to_csv(quarantine_csv, index=False)

    for r in records:
        print(f"  🚨 BAD TICK [{tf} {r['datetime']}] {r['action']}: "
              f"O={r['open']} H={r['high']} L={r['low']} C={r['close']} "
              f"(ref close {r['ref_close']}, max dev {max_dev:.0%}) → {quarantine_csv}")
    return out


def to_utc(df: pd.DataFrame, source_tz: str, dt_col: str = "datetime") -> pd.DataFrame:
    """
    Normalize a naive (tz-unaware) wall-clock datetime column to UTC.

    Pass `source_tz` as IANA name (e.g. "America/New_York", "UTC", "Europe/London").
    DST transitions handled: ambiguous/nonexistent bars dropped.
    Returns new df; original untouched.
    """
    out = df.copy()
    out[dt_col] = pd.to_datetime(out[dt_col])
    if source_tz.upper() == "UTC":
        # already UTC wall-clock; just strip any tz info
        if out[dt_col].dt.tz is not None:
            out[dt_col] = out[dt_col].dt.tz_convert("UTC").dt.tz_localize(None)
        return out
    # naive → localize as source tz → convert to UTC → strip
    out[dt_col] = (
        out[dt_col]
        .dt.tz_localize(source_tz, ambiguous="NaT", nonexistent="NaT")
        .dt.tz_convert("UTC")
        .dt.tz_localize(None)
    )
    dropped = out[dt_col].isna().sum()
    if dropped:
        print(f"  ⚠ to_utc({source_tz}): dropped {dropped} bars at DST transition")
    return out.dropna(subset=[dt_col]).reset_index(drop=True)


def read_csv_utc(path: str, source_tz: str) -> pd.DataFrame:
    """Read OHLC bars and normalize datetime to UTC. DB (`ohlc` table) is canonical; the
    legacy data/{source}/{symbol}/{tf}.csv path is parsed for symbol/tf and used as fallback."""
    df = None
    try:
        import db
        p = Path(path)
        df = db.read_ohlc(p.parent.name, p.stem, source=p.parent.parent.name)
        if df is not None and not df.empty:
            df = df.copy()
            df["datetime"] = pd.to_datetime(df["datetime"])
            for c in ["open", "high", "low", "close", "volume"]:
                if c in df.columns:
                    df[c] = pd.to_numeric(df[c], errors="coerce")
    except Exception:
        df = None
    if df is None or df.empty:
        df = pd.read_csv(path, parse_dates=["datetime"])
    return to_utc(df, source_tz)


def _paths(source: str, symbol: str, tf: str):
    base = os.path.join("data", source, symbol.lower().replace("/", ""))
    os.makedirs(base, exist_ok=True)
    return {
        "dir": base,
        "csv": os.path.join(base, f"{tf}.csv"),
        "manifest": os.path.join(base, "_manifest.json"),
    }


def load_manifest(source: str, symbol: str) -> dict:
    p = _paths(source, symbol, "x")["manifest"]
    if not os.path.exists(p):
        return {}
    with open(p) as f:
        return json.load(f)


def _save_manifest(source: str, symbol: str, manifest: dict):
    p = _paths(source, symbol, "x")["manifest"]
    tmp = p + ".tmp"
    with open(tmp, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)
    os.replace(tmp, p)


def last_dt(source: str, symbol: str, tf: str):
    """Last stored datetime (pd.Timestamp) for this source/symbol/tf, or None.
    Reads MAX(datetime) from the DB `ohlc` table (no more _manifest.json bookmark)."""
    try:
        import db
        s = db.last_ohlc_dt(symbol, tf, source)
        if s:
            return pd.Timestamp(s)
    except Exception:
        pass
    m = load_manifest(source, symbol).get(tf, {})   # legacy fallback (manifests removed)
    s = m.get("last_dt")
    return pd.Timestamp(s) if s else None


def upsert(source: str, symbol: str, tf: str, df: pd.DataFrame) -> dict:
    """Merge new bars into existing CSV. Dedupe on datetime (keep last). Atomic write."""
    if df.empty:
        return load_manifest(source, symbol).get(tf, {})

    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True).dt.tz_convert(None)
    for c in ["open", "high", "low", "close", "volume"]:
        if c not in df.columns:
            df[c] = 0.0
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df[OHLC_COLS].dropna(subset=["datetime", "close"])
    df = filter_trading_session(df, tf)

    p = _paths(source, symbol, tf)
    # Merge against prior bars from the DB (canonical) — CSV fallback keeps cold starts working.
    try:
        import db
        old = db.read_ohlc(symbol, tf, source=source)
    except Exception:
        old = None
    if (old is None or old.empty) and os.path.exists(p["csv"]):
        old = pd.read_csv(p["csv"])
    if old is not None and not old.empty:
        old = old.copy()
        old["datetime"] = pd.to_datetime(old["datetime"])
        for c in ["open", "high", "low", "close", "volume"]:
            if c in old.columns:
                old[c] = pd.to_numeric(old[c], errors="coerce")
        merged = pd.concat([old[OHLC_COLS], df], ignore_index=True)
    else:
        merged = df
    merged = (
        merged.drop_duplicates("datetime", keep="last")
              .sort_values("datetime")
              .reset_index(drop=True)
    )
    merged = filter_trading_session(merged, tf)
    merged = quarantine_bad_ticks(merged, tf,
                                  quarantine_csv=os.path.join(p["dir"], "_quarantine.csv"))

    # Persist the merged slice to the DB `ohlc` table (canonical store). On DB failure, write the
    # CSV as an emergency fallback so a pull never loses freshly-fetched bars (re-ingest manually
    # via db.replace_ohlc_slice). Normal path: DB only — no CSV mirror.
    try:
        import db
        db.replace_ohlc_slice(source, symbol, tf, merged[OHLC_COLS])
    except Exception as e:  # noqa: BLE001
        print(f"  ⚠ ohlc DB write failed ({source}/{symbol}/{tf}) — writing CSV fallback: {e}")
        tmp = p["csv"] + ".tmp"
        merged.to_csv(tmp, index=False)
        os.replace(tmp, p["csv"])

    # Coverage stats returned for the caller's print only — no longer persisted to _manifest.json
    # (last_dt is now read straight from the DB via db.last_ohlc_dt).
    return {
        "first_dt": merged["datetime"].iloc[0].isoformat(),
        "last_dt": merged["datetime"].iloc[-1].isoformat(),
        "rows": int(len(merged)),
        "last_pull_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
