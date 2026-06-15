#!/usr/bin/env python3
"""Send a Telegram message via the Bot API.

Reads TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID from the environment or from the
project .env file (KEY=value lines). Message text comes from --text or stdin.

Usage:
    python scripts/notify_telegram.py --text "hello"
    echo "hello" | python scripts/notify_telegram.py

Exit codes: 0 = sent, 1 = missing keys, 2 = send failed. Non-fatal by design —
callers (scheduled /validate) should not crash if Telegram is down.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"


def load_env_keys():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHAT_ID")
    if (not token or not chat) and ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k == "TELEGRAM_BOT_TOKEN" and not token:
                token = v
            elif k == "TELEGRAM_CHAT_ID" and not chat:
                chat = v
    return token, chat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", help="message text; if omitted, read from stdin")
    ap.add_argument("--silent", action="store_true", help="disable Telegram notification sound")
    args = ap.parse_args()

    text = args.text if args.text is not None else sys.stdin.read()
    text = (text or "").strip()
    if not text:
        print("[notify_telegram] empty message — nothing to send", file=sys.stderr)
        return 0

    token, chat = load_env_keys()
    if not token or not chat:
        print("[notify_telegram] TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set "
              "(env or .env) — skipping send", file=sys.stderr)
        return 1

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": chat,
        "text": text[:4096],            # Telegram hard limit
        "disable_notification": args.silent,
        "disable_web_page_preview": True,
    }).encode()
    try:
        with urllib.request.urlopen(url, data=data, timeout=15) as r:
            resp = json.loads(r.read().decode())
        if resp.get("ok"):
            print("[notify_telegram] sent")
            return 0
        print(f"[notify_telegram] API error: {resp}", file=sys.stderr)
        return 2
    except Exception as e:  # noqa: BLE001 — never crash the caller
        print(f"[notify_telegram] send failed: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
