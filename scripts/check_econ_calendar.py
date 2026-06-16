"""
Economic-calendar check — scheduled data-release gate for /weekly + /validate (#1/#2).

Reads data/econ_calendar/calendar.csv (Forex Factory free JSON, fetched by weekly_pull.py)
and reports HIGH-impact scheduled releases for an instrument's two currency legs inside the
lookahead window, with no-trade windows. This is the data-release analogue of check_cb_calendar.py
(which covers central-bank DECISIONS): together they remove the manual-web-search blind
spot that caused the W24 ECB miss.

  --retro <ISO-week> mode: prints last week's releases with actual vs estimate → SURPRISE
  (#2), consumed by the /weekly Step 2b retrospective.

Country codes are ISO-2 (weekly_pull maps the Forex Factory currency field → ISO-2). The
pair→country map below may need a one-line tweak if the euro area shows as EU vs DE/FR —
verify against data/econ_calendar/calendar.csv.

Usage:
    bash scripts/pyrun.sh scripts/check_econ_calendar.py --instrument eurusd --days 10
    bash scripts/pyrun.sh scripts/check_econ_calendar.py --instrument eurusd --date 2026-06-15
    bash scripts/pyrun.sh scripts/check_econ_calendar.py --retro 2026-W23 --instrument eurusd

Exit codes: 0 = ran. 1 = calendar CSV missing or its coverage ends before the window end
(stale → re-run weekly_pull.py to refetch before trusting "no events").
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

ECON_CSV = Path("data/econ_calendar/calendar.csv")

INSTRUMENTS = ["xauusd", "eurusd", "gbpusd", "eurgbp", "audusd", "nzdusd",
               "usdcad", "usdchf", "usdjpy", "eurjpy", "gbpjpy"]

# Instrument → the country legs whose releases move it. US is in every USD pair; gold = US.
PAIR_COUNTRIES = {
    "xauusd": ["US"],
    "eurusd": ["US", "EU"], "gbpusd": ["US", "GB"], "eurgbp": ["EU", "GB"],
    "audusd": ["US", "AU"], "nzdusd": ["US", "NZ"], "usdcad": ["US", "CA"],
    "usdchf": ["US", "CH"], "usdjpy": ["US", "JP"], "eurjpy": ["EU", "JP"],
    "gbpjpy": ["GB", "JP"],
}

HIGH = {"high", "3", "h"}  # Forex Factory impact "High" (lowercased) = high-impact


def load_calendar() -> pd.DataFrame:
    df = None
    try:
        import db
        df = db.read_table("econ_calendar")             # canonical store
    except Exception:
        df = None
    if (df is None or df.empty) and ECON_CSV.exists():
        df = pd.read_csv(ECON_CSV, dtype=str).fillna("")
    if df is None or df.empty:
        print(f"❌ No econ calendar in data/index.db or {ECON_CSV} — run weekly_pull.py (Forex "
              f"Factory free JSON, no key) before trusting the no-trade calendar. Web-search fallback applies.")
        sys.exit(1)
    df = df.fillna("")
    df["country"] = df["country"].str.upper().str.strip()
    return df


def is_high(impact: str) -> bool:
    return str(impact).strip().lower() in HIGH


def iso_week_window(week: str):
    year, wnum = week.split("-W")
    mon = datetime.fromisocalendar(int(year), int(wnum), 1).date()
    return mon, mon + timedelta(days=6)


def cmd_retro(df: pd.DataFrame, week: str, countries: list[str]):
    start, end = iso_week_window(week)
    m = (df["date"] >= str(start)) & (df["date"] <= str(end)) & df["country"].isin(countries)
    sub = df[m & df["actual"].astype(str).str.strip().ne("")]
    print(f"Surprise retrospective — {week} ({start}→{end}), {'/'.join(countries)}")
    if sub.empty:
        print("  (no released high/med events with actuals in window)")
        return 0
    for _, r in sub[sub["impact"].map(is_high)].iterrows():
        est, act = str(r["estimate"]).strip(), str(r["actual"]).strip()
        surprise = ""
        try:
            if est and act:
                d = float(act) - float(est)
                surprise = f"  → {'BEAT' if d > 0 else 'MISS' if d < 0 else 'INLINE'} ({d:+.4g} vs est)"
        except ValueError:
            pass
        print(f"  {r['date']} [{r['country']}] {r['event']}: actual {act or '—'} / est {est or '—'} "
              f"/ prev {str(r['prev']).strip() or '—'}{surprise}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Economic-calendar / data-release gate")
    ap.add_argument("--instrument", required=True, choices=INSTRUMENTS)
    ap.add_argument("--date", help="YYYY-MM-DD window start (default: today UTC)")
    ap.add_argument("--days", type=int, default=7, help="lookahead window in days (default 7)")
    ap.add_argument("--retro", help="ISO week (e.g. 2026-W23) → surprise retrospective instead")
    ap.add_argument("--all-impact", action="store_true", help="include medium/low, not just high")
    args = ap.parse_args()

    df = load_calendar()
    countries = PAIR_COUNTRIES[args.instrument]

    if args.retro:
        return cmd_retro(df, args.retro, countries)

    start = (datetime.strptime(args.date, "%Y-%m-%d").date() if args.date
             else datetime.now(timezone.utc).date())
    end = start + timedelta(days=args.days)

    coverage_end = df["date"].max() if not df.empty else ""
    m = (df["date"] >= str(start)) & (df["date"] <= str(end)) & df["country"].isin(countries)
    hits = df[m] if args.all_impact else df[m & df["impact"].map(is_high)]
    hits = hits.sort_values(["date", "time_utc"])

    print(f"Econ-calendar check — {args.instrument} ({'/'.join(countries)}), "
          f"window {start} → {end} (UTC)")
    if hits.empty:
        print("✅ No high-impact scheduled releases in window.")
    for _, r in hits.iterrows():
        days_away = (datetime.strptime(r["date"], "%Y-%m-%d").date() - start).days
        when = "TODAY" if days_away == 0 else f"in {days_away}d"
        est = f" (est {str(r['estimate']).strip()})" if str(r["estimate"]).strip() else ""
        print(f"\n🔔 {r['date']} {r['time_utc'] or '??:??'} UTC ({when}) — "
              f"[{r['country']}] {r['event']}{est}")
        print(f"   no-trade window: release ±30min (high-impact)")

    if coverage_end and str(end) > coverage_end:
        print(f"\n❌ Calendar coverage ends {coverage_end} but window extends to {end} — "
              f"re-run weekly_pull.py to refetch before trusting a 'no events' result.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
