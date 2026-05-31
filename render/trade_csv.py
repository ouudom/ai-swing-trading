"""Export trades to CSV matching the existing trades_log.csv schema."""

from __future__ import annotations

import csv
from pathlib import Path

from db.schemas import Trade

COLUMNS = [
    "date",
    "week",
    "setup",
    "direction",
    "entry",
    "sl",
    "tp",
    "lots",
    "stop_dist",
    "r_planned",
    "fill_time",
    "exit_time",
    "exit_px",
    "exit_reason",
    "r_actual",
    "mfe",
    "mae",
    "notes",
]


def export_trades_to_csv(filepath: str | Path, trades: list[Trade]) -> Path:
    """Write trades to CSV. Matches existing trades_log.csv schema."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for t in trades:
            writer.writerow(_trade_to_row(t))

    return path


def _trade_to_row(t: Trade) -> dict[str, str]:
    return {
        "date": t.date.isoformat(),
        "week": t.week,
        "setup": t.setup.value,
        "direction": t.direction.value,
        "entry": str(t.entry),
        "sl": str(t.sl),
        "tp": str(t.tp),
        "lots": str(t.lots),
        "stop_dist": str(t.stop_dist),
        "r_planned": str(t.r_planned),
        "fill_time": t.fill_time.isoformat(),
        "exit_time": t.exit_time.isoformat() if t.exit_time else "",
        "exit_px": str(t.exit_px) if t.exit_px is not None else "",
        "exit_reason": t.exit_reason.value if t.exit_reason else "",
        "r_actual": str(t.r_actual) if t.r_actual is not None else "",
        "mfe": str(t.mfe) if t.mfe is not None else "",
        "mae": str(t.mae) if t.mae is not None else "",
        "notes": t.notes or "",
    }
