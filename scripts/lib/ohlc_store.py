"""
OHLC storage helper. Source-segregated, atomic upsert, manifest-tracked.

Layout:
  data/{source}/{symbol}/{tf}.csv
  data/{source}/{symbol}/_manifest.json
"""
import os
import json
import pandas as pd
from datetime import datetime, timezone

OHLC_COLS = ["datetime", "open", "high", "low", "close", "volume"]

# Known source timezones. All TD data pulled with timezone=UTC → stored as UTC.
SOURCE_TZ = {
    "twelvedata": "UTC",
}


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
    """Read an OHLC CSV and normalize its datetime column to UTC."""
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
    """Return last stored datetime (pd.Timestamp) for this source/symbol/tf, or None."""
    m = load_manifest(source, symbol).get(tf, {})
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

    p = _paths(source, symbol, tf)
    if os.path.exists(p["csv"]):
        old = pd.read_csv(p["csv"], parse_dates=["datetime"])
        merged = pd.concat([old, df], ignore_index=True)
    else:
        merged = df
    merged = (
        merged.drop_duplicates("datetime", keep="last")
              .sort_values("datetime")
              .reset_index(drop=True)
    )

    tmp = p["csv"] + ".tmp"
    merged.to_csv(tmp, index=False)
    os.replace(tmp, p["csv"])

    manifest = load_manifest(source, symbol)
    manifest[tf] = {
        "first_dt": merged["datetime"].iloc[0].isoformat(),
        "last_dt": merged["datetime"].iloc[-1].isoformat(),
        "rows": int(len(merged)),
        "last_pull_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    _save_manifest(source, symbol, manifest)
    return manifest[tf]
