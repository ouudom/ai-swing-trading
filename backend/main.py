"""
Trading Brain — local backend.
Serves OHLC candles from data/twelvedata/xauusd/*.csv.

Run:
    .venv/bin/uvicorn backend.main:app --reload --port 8000
"""
from pathlib import Path
from functools import lru_cache
from time import time

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "twelvedata" / "xauusd"

TF_FILES = {
    "15m": "15min.csv",
    "1h": "1h.csv",
    "4h": "4h.csv",
    "1d": "1day.csv",
}

app = FastAPI(title="Trading Brain API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


_cache: dict[str, tuple[float, list]] = {}
CACHE_TTL = 60.0


def _load_candles(tf: str, limit: int) -> list[dict]:
    fname = TF_FILES.get(tf)
    if not fname:
        raise HTTPException(400, f"unknown tf '{tf}'. allowed: {list(TF_FILES)}")
    path = DATA_DIR / fname
    if not path.exists():
        raise HTTPException(500, f"missing data file: {path}")

    key = f"{tf}:{limit}"
    now = time()
    cached = _cache.get(key)
    if cached and now - cached[0] < CACHE_TTL:
        return cached[1]

    df = pd.read_csv(path, parse_dates=["datetime"])
    df = df.sort_values("datetime").tail(limit)
    out = [
        {
            "time": int(ts.timestamp()),
            "open": float(o),
            "high": float(h),
            "low": float(l),
            "close": float(c),
        }
        for ts, o, h, l, c in zip(
            df["datetime"], df["open"], df["high"], df["low"], df["close"]
        )
    ]
    _cache[key] = (now, out)
    return out


@app.get("/api/candles")
def candles(
    tf: str = Query("4h"),
    limit: int = Query(300, ge=10, le=5000),
):
    data = _load_candles(tf, limit)
    return {"symbol": "XAUUSD", "tf": tf, "count": len(data), "candles": data}


@app.get("/api/health")
def health():
    return {"ok": True, "tfs": list(TF_FILES.keys())}
