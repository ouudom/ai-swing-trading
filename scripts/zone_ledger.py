"""
Zone ledger — shadow-trade registry for every published Trading Zone.

Every zone from /weekly gets one row here at publish time, whether or not a real
trade ever fires. `zone_outcomes.py` later replays OHLC against these rows to
measure zone hit-rates, confluence-score calibration, and would-be R outcomes.
Without this, confluence scores are never validated against reality.

Store: `zone_ledger` table in data/database/index.db (DB-canonical; resolver flips
status OPEN→RESOLVED). zone_id = {instrument}-{week}-{label}, e.g. gbpusd-2026-W24-PRIMARY.

Usage:
    bash scripts/pyrun.sh scripts/zone_ledger.py add \
        --instrument gbpusd --week 2026-W24 --label PRIMARY --direction SHORT \
        --zone-bottom 1.3400 --zone-top 1.3447 --score 8.0 --conviction MEDIUM \
        [--invalidation-level 1.3460] [--tp-anchor 1.32866] [--notes "..."]
    bash scripts/pyrun.sh scripts/zone_ledger.py validate \
        --zone-id gbpusd-2026-W24-PRIMARY --verdict ORDER_LIMIT \
        [--entry-confluence 7.5] [--limit-price 1.3452] [--date 2026-06-16] \
        [--e0]                # confirmation candle present → anchor may lock (D032)
        [--hard-block]        # on a hard-gate NO_TRADE/INVALIDATED → clears the anchor lock
        [--lock-hours 4]      # anchor-lock window (default 4h, clamped to 21:00 UTC)
    bash scripts/pyrun.sh scripts/zone_ledger.py list [--week 2026-W24] [--status OPEN]

Anchor lock (D030 follow-up; D032): an ORDER_LIMIT confirmed off a 1H/15M E0 (--e0) freezes its
anchor for --lock-hours so the hourly /validate re-run stops whipsawing the limit. A no-E0 (50%
zone-midpoint) ORDER_LIMIT writes the verdict but NEVER locks — it keeps re-deriving hourly. While
locked: a strictly higher-EC *E0* ORDER_LIMIT re-anchors and resets the clock (UPGRADE); an
equal/lower EC, a no-E0 midpoint ORDER_LIMIT, or a soft NO_TRADE (E0 lapse / EC dip) is ignored
(HOLD); INVALIDATED or NO_TRADE --hard-block always cancels and clears the lock (CANCEL).

`--invalidation-level` optional: when omitted, the resolver applies the default
rule (D1 close beyond the zone's far edge — top for SHORT, bottom for LONG).
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))  # for `db` import
import db  # noqa: E402

LEDGER_CSV = Path("data/zone_ledger.csv")
TABLE = "zone_ledger"

COLUMNS = [
    "zone_id", "instrument", "week", "label", "direction",
    "zone_bottom", "zone_top", "zone_confluence", "conviction",
    "invalidation_level", "tp_anchor", "published_utc", "source_file",
    "status", "notes",
    # daily-validation write-back (latest /validate verdict per zone) — frontend reads these
    "entry_confluence", "daily_verdict", "limit_price", "validated_date",
    # asymmetric anchor lock (D030 follow-up; D032): freeze an E0-confirmed ORDER_LIMIT anchor for
    # a window so the hourly /validate re-derivation stops whipsawing the limit. Only --e0 (anchor
    # = confirmation close) locks; a no-E0 50%-midpoint ORDER_LIMIT re-derives hourly. The lock
    # holds the limit/EC against soft downgrades (E0 lapse, EC dip) but yields to upgrades (a
    # stronger E0 re-anchors + resets the clock) and to hard blocks (V1/V1b/V3/intervention → cleared).
    "anchor_set_utc", "anchor_locked_until",
]

LABELS = ["PRIMARY", "SECONDARY", "COUNTER"]
VERDICTS = ["PENDING", "ORDER_LIMIT", "NO_TRADE", "INVALIDATED"]


def load_ledger() -> pd.DataFrame:
    # Canonical store = data/index.db (table `zone_ledger`); CSV is a mirror.
    df = db.read_table(TABLE, columns=COLUMNS)
    if not df.empty:
        return df
    if LEDGER_CSV.exists():            # cold-start fallback
        return pd.read_csv(LEDGER_CSV, dtype={"week": str})
    return pd.DataFrame(columns=COLUMNS)


def save_ledger(df: pd.DataFrame):
    db.write_table(TABLE, df, columns=COLUMNS)   # DB-canonical; no CSV mirror


def cmd_add(args):
    if args.zone_bottom >= args.zone_top:
        sys.exit(f"❌ zone_bottom {args.zone_bottom} must be < zone_top {args.zone_top}")
    zone_id = f"{args.instrument}-{args.week}-{args.label}"
    df = load_ledger()
    if (df["zone_id"] == zone_id).any():
        if not args.force:
            sys.exit(f"❌ {zone_id} already in ledger — use --force to overwrite")
        df = df[df["zone_id"] != zone_id]

    row = {
        "zone_id": zone_id,
        "instrument": args.instrument,
        "week": args.week,
        "label": args.label,
        "direction": args.direction,
        "zone_bottom": args.zone_bottom,
        "zone_top": args.zone_top,
        "zone_confluence": args.score,
        "conviction": args.conviction or "",
        "invalidation_level": args.invalidation_level if args.invalidation_level is not None else "",
        "tp_anchor": args.tp_anchor if args.tp_anchor is not None else "",
        "published_utc": args.published or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source_file": args.source_file or f"forecasts/weekly/{args.instrument}/{args.week}.md",
        "status": "OPEN",
        "notes": args.notes or "",
        "entry_confluence": "",
        "daily_verdict": "PENDING",      # set by `zone_ledger.py validate` at /validate
        "limit_price": "",
        "validated_date": "",
        "anchor_set_utc": "",
        "anchor_locked_until": "",
    }
    new = pd.DataFrame([row])
    df = new if df.empty else pd.concat([df, new], ignore_index=True)
    save_ledger(df)
    print(f"✅ ledger += {zone_id}  {args.direction} {args.zone_bottom}–{args.zone_top} "
          f"(R1 {args.score}) → {TABLE} (DB)")


TS_FMT = "%Y-%m-%dT%H:%M:%SZ"


def _parse_ts(s: str):
    """Parse an ISO-UTC stamp ('...Z' or naive) → tz-aware UTC datetime, or None."""
    if not s:
        return None
    s = str(s).strip()
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _fmt_ts(dt) -> str:
    return dt.astimezone(timezone.utc).strftime(TS_FMT)


def _to_float(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def cmd_validate(args):
    """Write the latest daily-validation verdict back onto a published zone row.

    Called once per validated zone at the end of /validate so the frontend can show
    per-zone status (ORDER_LIMIT / NO_TRADE / INVALIDATED) + R2 + limit without
    scraping the daily markdown body.

    Asymmetric anchor lock (D030 follow-up; D032). Only an E0-confirmed ORDER_LIMIT (--e0,
    anchor = confirmation candle CLOSE) locks its anchor (limit/EC) for --lock-hours
    (default 4), so the hourly re-run stops whipsawing the resting limit. A no-E0
    ORDER_LIMIT (anchor = 50% zone midpoint) writes the verdict but does NOT lock — it
    keeps re-deriving every hour. While a lock is live:
      • UPGRADE  — a strictly higher-EC *E0* ORDER_LIMIT re-anchors (new limit/EC) AND
                   resets the clock.
      • HOLD     — an equal/lower EC E0 ORDER_LIMIT, a no-E0 (midpoint) ORDER_LIMIT, or a
                   *soft* NO_TRADE (E0 lapse / EC below floor), is ignored: the locked
                   limit/EC/verdict stay put.
      • CANCEL   — INVALIDATED, or NO_TRADE with --hard-block (V1/V1b/V3/intervention/
                   macro-flip), always wins: it writes the verdict and clears the lock.
    The lock never extends past the daily 21:00 UTC expiry (clamped).
    """
    df = load_ledger()
    mask = df["zone_id"] == args.zone_id
    if not mask.any():
        sys.exit(f"❌ {args.zone_id} not in ledger — publish it first (zone_ledger.py add)")
    i = df.index[mask][0]

    now = _parse_ts(args.now) or datetime.now(timezone.utc)
    val_date = args.date or now.strftime("%Y-%m-%d")
    lock_hours = args.lock_hours

    prev_verdict = str(df.at[i, "daily_verdict"] or "")
    prev_ec = _to_float(df.at[i, "entry_confluence"])
    locked_until = _parse_ts(df.at[i, "anchor_locked_until"])
    lock_live = prev_verdict == "ORDER_LIMIT" and locked_until is not None and now < locked_until
    new_ec = args.entry_confluence
    hard = args.hard_block or args.verdict == "INVALIDATED"

    def _write(verdict, ec, limit, set_lock):
        df.at[i, "daily_verdict"] = verdict
        df.at[i, "entry_confluence"] = "" if ec is None else str(ec)
        df.at[i, "limit_price"] = "" if limit is None else str(limit)
        df.at[i, "validated_date"] = val_date
        if set_lock:
            until = now + pd.Timedelta(hours=lock_hours)
            cap = _parse_ts(f"{val_date}T21:00:00Z")          # daily order expiry
            if cap is not None and until > cap:
                until = cap
            df.at[i, "anchor_set_utc"] = _fmt_ts(now)
            df.at[i, "anchor_locked_until"] = _fmt_ts(until) if until > now else ""
        else:
            df.at[i, "anchor_set_utc"] = ""
            df.at[i, "anchor_locked_until"] = ""

    # ── decide ────────────────────────────────────────────────────────────────
    if hard:                                                  # CANCEL — always wins
        _write(args.verdict, new_ec, args.limit_price, set_lock=False)
        action = f"CANCEL ({'hard-block' if args.hard_block else 'invalidated'}) — lock cleared"
    elif args.verdict == "ORDER_LIMIT" and lock_live:
        if args.e0 and new_ec is not None and prev_ec is not None and new_ec > prev_ec:
            _write("ORDER_LIMIT", new_ec, args.limit_price, set_lock=True)   # UPGRADE (E0 only)
            action = f"UPGRADE EC {prev_ec}→{new_ec} — re-anchored, lock reset"
        elif not args.e0:
            action = (f"HOLD — no-E0 (midpoint) ORDER_LIMIT cannot re-anchor a locked E0 entry; "
                      f"locked until {df.at[i,'anchor_locked_until']}; limit {df.at[i,'limit_price']} unchanged")
        else:
            action = (f"HOLD — locked until {df.at[i,'anchor_locked_until']} "
                      f"(EC {prev_ec} ≥ {new_ec}); limit {df.at[i,'limit_price']} unchanged")
    elif args.verdict == "NO_TRADE" and lock_live:
        action = (f"HOLD — soft NO_TRADE ignored under lock until "
                  f"{df.at[i,'anchor_locked_until']}; limit {df.at[i,'limit_price']} unchanged")
    elif args.verdict == "ORDER_LIMIT":
        _write("ORDER_LIMIT", new_ec, args.limit_price, set_lock=args.e0)    # fresh ACCEPT
        if args.e0:
            action = f"ACCEPT — E0 confirmed, anchor locked until {df.at[i,'anchor_locked_until']}"
        else:
            action = "ACCEPT — no-E0 (50% midpoint) anchor, NOT locked (D032; re-derives hourly)"
    else:                                                     # NO_TRADE / PENDING, no live lock
        _write(args.verdict, new_ec, args.limit_price, set_lock=False)
        action = args.verdict

    save_ledger(df)
    print(f"✅ {args.zone_id} validated {val_date}: {action}")
    print(f"   effective: verdict={df.at[i,'daily_verdict']} "
          f"EC={df.at[i,'entry_confluence'] or '—'} limit={df.at[i,'limit_price'] or '—'} "
          f"lock={df.at[i,'anchor_locked_until'] or 'none'}")


def cmd_list(args):
    df = load_ledger()
    if df.empty:
        print("ledger empty")
        return
    for col, val in [("instrument", args.instrument), ("week", args.week), ("status", args.status)]:
        if val:
            df = df[df[col] == val]
    if df.empty:
        print("no matching rows")
        return
    cols = ["zone_id", "direction", "zone_bottom", "zone_top", "zone_confluence",
            "conviction", "status", "daily_verdict"]
    print(df[cols].to_string(index=False))
    print(f"\n{len(df)} rows | status: {df['status'].value_counts().to_dict()}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="register a published zone")
    a.add_argument("--instrument", required=True)
    a.add_argument("--week", required=True, help="ISO trade week, e.g. 2026-W24")
    a.add_argument("--label", required=True, choices=LABELS)
    a.add_argument("--direction", required=True, choices=["LONG", "SHORT"])
    a.add_argument("--zone-bottom", type=float, required=True)
    a.add_argument("--zone-top", type=float, required=True)
    a.add_argument("--score", type=float, required=True, help="Zone Confluence R1 (0–10)")
    a.add_argument("--conviction", default="",
                   choices=["", "HIGH", "MEDIUM-HIGH", "MEDIUM", "MEDIUM-LOW", "LOW"])
    a.add_argument("--invalidation-level", type=float, default=None,
                   help="D1-close kill level (default: zone far edge)")
    a.add_argument("--tp-anchor", type=float, default=None)
    a.add_argument("--published", default="", help="ISO UTC timestamp (default: now)")
    a.add_argument("--source-file", default="")
    a.add_argument("--notes", default="")
    a.add_argument("--force", action="store_true", help="overwrite existing zone_id")
    a.set_defaults(func=cmd_add)

    v = sub.add_parser("validate", help="write a daily-validation verdict back onto a zone")
    v.add_argument("--zone-id", required=True, help="e.g. eurusd-2026-W25-PRIMARY")
    v.add_argument("--verdict", required=True, choices=VERDICTS)
    v.add_argument("--entry-confluence", type=float, default=None, help="Entry Confluence R2 (0–10)")
    v.add_argument("--limit-price", type=float, default=None, help="order-limit price on ORDER_LIMIT")
    v.add_argument("--date", default="", help="validation date YYYY-MM-DD (default: today UTC)")
    v.add_argument("--hard-block", action="store_true",
                   help="cancel + clear any anchor lock (V1/V1b/V3/intervention/macro-flip). "
                        "Use on a NO_TRADE that is a hard gate, not a soft EC/E0 downgrade.")
    v.add_argument("--e0", action="store_true",
                   help="confirmation candle (E0) present — the anchor is a confirmation CLOSE, not a "
                        "50%% zone midpoint. Only an E0-confirmed ORDER_LIMIT sets/keeps the anchor "
                        "lock (D032); a no-E0 midpoint ORDER_LIMIT writes the verdict but never locks.")
    v.add_argument("--lock-hours", type=float, default=4.0,
                   help="anchor-lock window in hours (default 4; clamped to 21:00 UTC expiry)")
    v.add_argument("--now", default="",
                   help="override 'now' as ISO-UTC (testing only; default: system UTC now)")
    v.set_defaults(func=cmd_validate)

    l = sub.add_parser("list", help="show ledger rows")
    l.add_argument("--instrument", default="")
    l.add_argument("--week", default="")
    l.add_argument("--status", default="", choices=["", "OPEN", "RESOLVED"])
    l.set_defaults(func=cmd_list)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
