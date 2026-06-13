"""
JPY intervention / jawboning watch — mechanical gate for /weekly + /validate (#4).

Reads scripts/config/intervention_watch.json and, given the current spot, returns the
intervention regime for a JPY pair (usdjpy/eurjpy/gbpjpy): how close spot is to the MoF
intervention level, and any recent jawboning. This is the structured replacement for the
manual web-search MoF read — modeled on check_cb_calendar.py.

Spot rises toward the level = JPY weakening = MoF intervention risk against further pair
upside, so the gate blocks/caps NEW LONGS of the pair (= shorts of JPY):
  spot >= intervention_level             → HARD_BLOCK new longs (active intervention zone)
  spot >= intervention_level − band      → CAUTION  (cap conviction MEDIUM)
  recent jawboning within --days         → CAUTION at minimum, regardless of level

Claude maintains the JSON's jawboning[] from web search during /weekly JPY runs and pushes
verified_through forward (same discipline as cb_calendar).

Usage:
    bash scripts/pyrun.sh scripts/check_intervention_watch.py --instrument usdjpy --spot 160.5
    bash scripts/pyrun.sh scripts/check_intervention_watch.py --instrument eurjpy --spot 185.2 --days 14

Exit codes: 0 = ran. 1 = JSON missing/unreadable, pair absent, or verified_through is
before the query date (watch is stale → refresh from web search before trusting it).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WATCH_JSON = Path(__file__).resolve().parent / "config" / "intervention_watch.json"
JPY_PAIRS = ["usdjpy", "eurjpy", "gbpjpy"]


def main() -> int:
    ap = argparse.ArgumentParser(description="JPY intervention / jawboning watch")
    ap.add_argument("--instrument", required=True, choices=JPY_PAIRS)
    ap.add_argument("--spot", type=float, required=True, help="current spot price of the pair")
    ap.add_argument("--date", help="YYYY-MM-DD (default: today UTC)")
    ap.add_argument("--days", type=int, default=10, help="jawboning lookback window (default 10)")
    args = ap.parse_args()

    if not WATCH_JSON.exists():
        print(f"❌ Missing {WATCH_JSON} — build the intervention watch before trading JPY.")
        return 1
    cfg = json.loads(WATCH_JSON.read_text())
    pair = cfg.get("pairs", {}).get(args.instrument)
    if not pair:
        print(f"❌ {args.instrument} not in {WATCH_JSON}")
        return 1

    today = (datetime.strptime(args.date, "%Y-%m-%d").date() if args.date
             else datetime.now(timezone.utc).date())
    level = float(pair["intervention_level"])
    band = float(pair["caution_band"])
    spot = args.spot

    # regime by distance to level
    if spot >= level:
        verdict = "🛑 HARD_BLOCK new longs — spot in active MoF intervention zone"
    elif spot >= level - band:
        verdict = "⚠ CAUTION — spot in intervention band; cap LONG conviction MEDIUM"
    else:
        verdict = "✅ clear of intervention band"

    # recent jawboning
    cutoff = today - timedelta(days=args.days)
    recent = [j for j in pair.get("jawboning", [])
              if j.get("date", "") and datetime.strptime(j["date"], "%Y-%m-%d").date() >= cutoff]

    print(f"Intervention watch — {args.instrument} @ {spot} (as of {today})")
    print(f"   level {level} | caution band {level - band}–{level} | regime {pair.get('regime','?')}")
    print(f"   {verdict}")
    if recent:
        print(f"   jawboning (last {args.days}d) → CAUTION at minimum:")
        for j in recent:
            print(f"     {j['date']} {j.get('official','?')}: \"{j.get('quote','')}\"")
    else:
        print(f"   no jawboning in last {args.days}d")

    vt = datetime.strptime(pair["verified_through"], "%Y-%m-%d").date()
    if today > vt:
        print(f"\n❌ watch verified only through {vt} — refresh {args.instrument} jawboning[] from "
              f"web search and push verified_through forward before trusting this.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
