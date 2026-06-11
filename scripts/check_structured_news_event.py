"""
T4-X — Structured news event checker (mid-week re-forecast trigger).

Reads data/news_events/[DATE]_t4x.json (written by operator/LLM during /validate step 3
when a qualifying unscheduled macro event is found via web search).

Returns True only when the JSON file exists AND every required field validates against
the constitution's closed category list. No file = no T4-X. Discretion is confined to
the act of writing the file — once written, validation is mechanical.

Schema enforced (all fields required):
    {
      "date":           "YYYY-MM-DD",                  # must equal --date arg
      "category":       one of CATEGORIES,
      "source":         one of SOURCES,
      "url":            "https://...",                 # must start with allowed source domain
      "utc_timestamp":  "YYYY-MM-DDTHH:MM:SSZ",
      "headline":       "verbatim headline"
    }

Usage:
    bash scripts/pyrun.sh scripts/check_structured_news_event.py --date 2026-05-27
    → exit 0 + prints "T4_X=TRUE | <category> | <headline>"  if fires
    → exit 0 + prints "T4_X=FALSE"                            if no file / invalid
    → exit 2 + prints error                                   if file exists but malformed

Import usage (from /validate workflow):
    from scripts.check_structured_news_event import check_structured_news_event
    fires, payload = check_structured_news_event("2026-05-27")
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

EVENTS_DIR = Path("data/news_events")

CATEGORIES = {
    "central_bank_emergency",   # off-cycle rate move, QE/QT shock
    "war_sanctions",            # declared war / G20 sanctions
    "fed_chair_removal",        # resignation or removal
    "sovereign_default",        # major economy default
    "political_shock",          # cancelled election, coup, impeachment vote
}

SOURCES = {
    "reuters.com",
    "bloomberg.com",
    "apnews.com",
}

REQUIRED_FIELDS = ("date", "category", "source", "url", "utc_timestamp", "headline")

ISO_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class T4XValidationError(Exception):
    pass


def _validate_payload(payload: dict, date_arg: str) -> None:
    missing = [f for f in REQUIRED_FIELDS if f not in payload or payload[f] in (None, "")]
    if missing:
        raise T4XValidationError(f"missing required fields: {missing}")

    if payload["date"] != date_arg:
        raise T4XValidationError(f"date mismatch: file says {payload['date']}, expected {date_arg}")

    if payload["category"] not in CATEGORIES:
        raise T4XValidationError(
            f"category {payload['category']!r} not in allowed set {sorted(CATEGORIES)}"
        )

    if payload["source"] not in SOURCES:
        raise T4XValidationError(
            f"source {payload['source']!r} not in allowed set {sorted(SOURCES)}"
        )

    url = payload["url"]
    if not url.startswith("https://"):
        raise T4XValidationError(f"url must be https://: {url!r}")
    if payload["source"] not in url:
        raise T4XValidationError(f"url {url!r} does not contain source domain {payload['source']!r}")

    if not ISO_TS_RE.match(payload["utc_timestamp"]):
        raise T4XValidationError(
            f"utc_timestamp {payload['utc_timestamp']!r} not in ISO format YYYY-MM-DDTHH:MM:SSZ"
        )

    try:
        ts = datetime.strptime(payload["utc_timestamp"], "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as e:
        raise T4XValidationError(f"utc_timestamp unparseable: {e}")

    if ts.strftime("%Y-%m-%d") != date_arg:
        raise T4XValidationError(
            f"utc_timestamp date {ts.strftime('%Y-%m-%d')} does not match --date {date_arg}"
        )

    headline = payload["headline"].strip()
    if len(headline) < 10:
        raise T4XValidationError(f"headline too short (<10 chars): {headline!r}")


def check_structured_news_event(date_arg: str):
    """
    Returns (fires: bool, payload: dict|None).
    fires=True only on file present + all validations pass.
    Raises T4XValidationError if file exists but is malformed (caller must surface).
    """
    path = EVENTS_DIR / f"{date_arg}_t4x.json"
    if not path.exists():
        return False, None

    try:
        with path.open() as f:
            payload = json.load(f)
    except json.JSONDecodeError as e:
        raise T4XValidationError(f"{path}: invalid JSON — {e}")

    _validate_payload(payload, date_arg)
    return True, payload


def main(argv=None):
    parser = argparse.ArgumentParser(description="T4-X structured news event check")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    args = parser.parse_args(argv)

    try:
        fires, payload = check_structured_news_event(args.date)
    except T4XValidationError as e:
        print(f"T4_X=ERROR | {e}", file=sys.stderr)
        return 2

    if fires:
        print(f"T4_X=TRUE | {payload['category']} | {payload['headline']}")
    else:
        print("T4_X=FALSE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
