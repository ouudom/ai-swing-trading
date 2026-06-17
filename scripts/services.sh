#!/usr/bin/env bash
# Manage trading launchd services: start | stop | restart | status | logs
# Usage: bash scripts/services.sh [start|stop|restart|status|logs]
set -euo pipefail

API_LABEL="trading.api"
FE_LABEL="trading.frontend"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cmd="${1:-status}"

_load() {
    launchctl list "$API_LABEL" &>/dev/null \
        && echo "  $API_LABEL already running" \
        || launchctl load -w ~/Library/LaunchAgents/trading.api.plist
    launchctl list "$FE_LABEL" &>/dev/null \
        && echo "  $FE_LABEL already running" \
        || launchctl load -w ~/Library/LaunchAgents/trading.frontend.plist
    echo "Services loaded."
}

_unload() {
    launchctl unload ~/Library/LaunchAgents/trading.api.plist 2>/dev/null || true
    launchctl unload ~/Library/LaunchAgents/trading.frontend.plist 2>/dev/null || true
    echo "Services unloaded."
}

_status() {
    echo "--- API ($API_LABEL) ---"
    launchctl list | grep "$API_LABEL" || echo "  not running"
    echo "--- Frontend ($FE_LABEL) ---"
    launchctl list | grep "$FE_LABEL" || echo "  not running"
}

case "$cmd" in
    start)
        _load
        ;;
    stop)
        _unload
        ;;
    restart)
        _unload
        # If update triggered restart, reinstall frontend deps if package-lock changed
        if [[ "${2:-}" == "--update" ]]; then
            echo "Running npm install..."
            cd "$ROOT/frontend" && npm install
            cd "$ROOT"
        fi
        _load
        echo "Restarted. API :8008 | Frontend :3008"
        ;;
    status)
        _status
        ;;
    logs)
        service="${2:-all}"
        if [[ "$service" == "api" ]]; then
            tail -f "$ROOT/data/logs/api.log" "$ROOT/data/logs/api.err"
        elif [[ "$service" == "frontend" ]]; then
            tail -f "$ROOT/data/logs/frontend.log" "$ROOT/data/logs/frontend.err"
        else
            tail -f "$ROOT/data/logs/api.log" "$ROOT/data/logs/frontend.log"
        fi
        ;;
    *)
        echo "Usage: $0 [start|stop|restart|status|logs [api|frontend]]"
        exit 1
        ;;
esac
