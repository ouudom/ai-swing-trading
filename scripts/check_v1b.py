"""
V1b — Intraday H4 invalidation checker.

Reads _HOT.md for active setup zones, checks last 2 H4 closes in data/twelvedata/xauusd/4h.csv.
Flags any setup with 2 consecutive H4 closes >$5 past zone extreme.

Run at each H4 boundary (00/04/08/12/16/20 UTC) — manually or via cron.

Usage:
    .venv/bin/python scripts/check_v1b.py
"""

import re
import sys
import pandas as pd
from pathlib import Path

HOT_PATH = Path("_HOT.md")
H4_CSV   = Path("data/twelvedata/xauusd/4h.csv")
BUFFER   = 5.0  # $ past zone extreme that counts as a real breach (not noise)


def parse_setups(hot_text):
    """Yield dicts: {label, direction, zone_top, zone_bottom} for each Setup line in _HOT.md."""
    # Matches lines like: "- **Setup A** [8.0/10]: SELL ... zone $4530–$4575 ..."
    pat = re.compile(
        r"\*\*Setup\s+([A-Z])\*\*.*?(BUY|SELL).*?zone\s+\$([\d,.]+)\s*[–-]\s*\$([\d,.]+)",
        re.IGNORECASE,
    )
    for m in pat.finditer(hot_text):
        label, direction, lo, hi = m.group(1), m.group(2).upper(), m.group(3), m.group(4)
        lo_f = float(lo.replace(",", ""))
        hi_f = float(hi.replace(",", ""))
        yield {
            "label": label,
            "direction": direction,
            "zone_bottom": min(lo_f, hi_f),
            "zone_top":    max(lo_f, hi_f),
        }


def main():
    if not HOT_PATH.exists() or not H4_CSV.exists():
        print(f"❌ Missing {HOT_PATH} or {H4_CSV}")
        sys.exit(1)

    setups = list(parse_setups(HOT_PATH.read_text()))
    if not setups:
        print("No active setups in _HOT.md.")
        return

    h4 = pd.read_csv(H4_CSV, parse_dates=["datetime"]).sort_values("datetime")
    last2 = h4.tail(2)
    if len(last2) < 2:
        print("Not enough H4 bars.")
        return

    print(f"V1b check — last 2 H4 closes: ${last2['close'].iloc[0]:.2f} @ {last2['datetime'].iloc[0]} | ${last2['close'].iloc[1]:.2f} @ {last2['datetime'].iloc[1]}")
    print()

    any_breach = False
    for s in setups:
        c1, c2 = float(last2["close"].iloc[0]), float(last2["close"].iloc[1])
        if s["direction"] == "SELL":
            # invalidation = both H4 closes ABOVE zone_top + buffer
            breach = (c1 > s["zone_top"] + BUFFER) and (c2 > s["zone_top"] + BUFFER)
            extreme = s["zone_top"] + BUFFER
        else:
            breach = (c1 < s["zone_bottom"] - BUFFER) and (c2 < s["zone_bottom"] - BUFFER)
            extreme = s["zone_bottom"] - BUFFER
        verdict = "❌ V1b BREACH — INVALIDATE" if breach else "✅ intact"
        print(f"Setup {s['label']} ({s['direction']}) zone ${s['zone_bottom']:.2f}–${s['zone_top']:.2f} | threshold ${extreme:.2f} | {verdict}")
        if breach:
            any_breach = True

    if any_breach:
        print("\n→ Cancel live limits for breached setups. Remove from _HOT.md Pending Setups.")
        sys.exit(2)


if __name__ == "__main__":
    main()
