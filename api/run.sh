#!/usr/bin/env bash
# Launch the read-only API. Reuses the project .venv (has pandas/numpy + fastapi/uvicorn).
# Localhost only — do not bind 0.0.0.0 without adding auth first.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec "$ROOT/.venv/bin/python" -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8008 --app-dir "$ROOT"
