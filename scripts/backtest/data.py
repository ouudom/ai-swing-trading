"""Data loading + indicators. Source: Twelve Data (UTC)."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2] / "data/twelvedata/xauusd"

# TF label → filename (resampled from M15, all UTC)
TF_FILE = {
    "D1":  "1day.csv",
    "H4":  "4h.csv",
    "H1":  "1h.csv",
    "M15": "15min.csv",
}

BPY = {"D1": 252, "H4": 252 * 6, "H1": 252 * 24, "M15": 252 * 96}


def load(tf: str) -> pd.DataFrame:
    """Load OHLC for given TF. Returns DataFrame indexed by UTC datetime."""
    fname = TF_FILE.get(tf)
    if fname is None:
        raise ValueError(f"Unknown TF '{tf}'. Valid: {list(TF_FILE)}")
    path = ROOT / fname
    if not path.exists():
        raise FileNotFoundError(f"{path} not found. Run backfill_twelvedata.py first.")
    df = (
        pd.read_csv(path, parse_dates=["datetime"])
          .set_index("datetime")
          .sort_index()
    )
    return df[["open", "high", "low", "close"]].astype(float)


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    h, l, c = df["high"], df["low"], df["close"]
    tr = pd.concat(
        [(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1
    ).max(axis=1)
    return tr.rolling(n).mean()


def rsi(s: pd.Series, n: int = 14) -> pd.Series:
    d  = s.diff()
    up = d.clip(lower=0).rolling(n).mean()
    dn = (-d.clip(upper=0)).rolling(n).mean()
    rs = up / dn.replace(0, np.nan)
    return 100 - 100 / (1 + rs)
