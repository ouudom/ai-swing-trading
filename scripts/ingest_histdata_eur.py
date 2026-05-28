"""Ingest HistData.com EURUSD M1 (2020-2023), convert EST->UTC, merge with TD (2023->now).

HistData MT format: YYYY.MM.DD,HH:MM,O,H,L,C,V. Despite the "EST" label, the timestamps
empirically track US Eastern WITH DST (validated vs TD: summer needs +4h, winter +5h;
America/New_York→UTC gives 0.40 pip median diff vs fixed-offset 2.4+). Convert via
America/New_York tz, NOT a fixed offset. TD data is already UTC.

Writes research CSVs to data/research/eurusd/{15min,1h,4h,1day}.csv (full 2020->now).
Live TD CSVs in data/twelvedata/eurusd/ are LEFT UNTOUCHED (live pipeline appends those).

Run: .venv/bin/python -m scripts.ingest_histdata_eur
"""
import glob
import pandas as pd
from pathlib import Path

HIST_DIR = Path("/tmp/histdata_eur")
TD_DIR = Path("data/twelvedata/eurusd")
OUT_DIR = Path("data/research/eurusd")
TD_START = pd.Timestamp("2023-04-24")  # use TD from here; HistData before

RESAMPLE = {"15min": "15min", "1h": "1h", "4h": "4h", "1day": "1D"}


def load_histdata():
    frames = []
    for f in sorted(glob.glob(str(HIST_DIR / "*/*.csv"))):
        df = pd.read_csv(f, header=None,
                         names=["d", "t", "open", "high", "low", "close", "vol"])
        dt = pd.to_datetime(df["d"] + " " + df["t"], format="%Y.%m.%d %H:%M")
        # US Eastern WITH DST → UTC. DST-transition bars (rare) dropped via NaT.
        utc = (dt.dt.tz_localize("America/New_York", ambiguous="NaT", nonexistent="NaT")
                 .dt.tz_convert("UTC").dt.tz_localize(None))
        df["datetime"] = utc
        frames.append(df[["datetime", "open", "high", "low", "close"]].dropna(subset=["datetime"]))
    m1 = pd.concat(frames).drop_duplicates("datetime").sort_values("datetime").reset_index(drop=True)
    return m1


def resample(m1, rule):
    s = m1.set_index("datetime")
    o = s["open"].resample(rule).first()
    h = s["high"].resample(rule).max()
    l = s["low"].resample(rule).min()
    c = s["close"].resample(rule).last()
    out = pd.DataFrame({"open": o, "high": h, "low": l, "close": c}).dropna().reset_index()
    return out


def validate_overlap(hist_h1):
    """Compare HistData vs TD on overlapping H1 timestamps — confirms timezone alignment."""
    td = pd.read_csv(TD_DIR / "1h.csv", parse_dates=["datetime"])
    merged = pd.merge(hist_h1, td, on="datetime", suffixes=("_h", "_t"))
    if merged.empty:
        print("  ⚠ no overlapping timestamps — timezone likely misaligned!")
        return
    diff = (merged["close_h"] - merged["close_t"]).abs() * 10000  # pips
    print(f"  overlap N={len(merged)}  median |Δclose|={diff.median():.1f} pips  "
          f"p95={diff.quantile(0.95):.1f} pips  max={diff.max():.1f} pips")
    print(f"  (low diff = timezone aligned; high diff = offset error)")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    m1 = load_histdata()
    print(f"HistData M1: {len(m1)} bars {m1.datetime.iloc[0]} → {m1.datetime.iloc[-1]} (UTC)")

    hist_h1 = resample(m1, "1h")
    print("Timezone validation (HistData vs TD overlap, H1):")
    validate_overlap(hist_h1)

    for tf, rule in RESAMPLE.items():
        hist = resample(m1, rule)
        td = pd.read_csv(TD_DIR / f"{tf}.csv", parse_dates=["datetime"])[["datetime", "open", "high", "low", "close"]]
        hist_pre = hist[hist.datetime < TD_START]
        td_use = td[td.datetime >= TD_START]
        merged = pd.concat([hist_pre, td_use]).drop_duplicates("datetime").sort_values("datetime").reset_index(drop=True)
        merged.to_csv(OUT_DIR / f"{tf}.csv", index=False)
        print(f"  {tf}: {len(merged)} bars {merged.datetime.iloc[0].date()} → {merged.datetime.iloc[-1].date()} "
              f"(hist {len(hist_pre)} + td {len(td_use)})")


if __name__ == "__main__":
    main()
