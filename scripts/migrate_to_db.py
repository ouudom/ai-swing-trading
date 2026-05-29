"""
One-time migration: existing markdown forecasts/validations + CSV trades → SQLite DB.

Usage:
    .venv/bin/python scripts/migrate_to_db.py
"""

from __future__ import annotations

import csv
import re
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

# Allow imports from project root
_project_root = Path(__file__).resolve().parents[1]
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from db import init_db
from db.crud import (
    create_daily_validation,
    create_trade,
    create_weekly_forecast,
    upsert_active_setup,
)
from schemas import (
    ActiveSetup,
    Bias,
    Confidence,
    DailyValidation,
    Direction,
    ExitReason,
    HardBlock,
    MacroDriver,
    Setup,
    SetupLetter,
    SetupLifecycle,
    Trade,
    ValidationGate,
    WeeklyForecast,
)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def _to_float(value):
    if value is None or value == "N/A" or value == "":
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _to_int(value):
    if value is None or value == "N/A" or value == "":
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text.strip())
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group(1))
    body = m.group(2)
    return fm if isinstance(fm, dict) else {}, body


def migrate_weekly_forecasts() -> int:
    count = 0
    for inst_dir in sorted(Path("forecasts/weekly").glob("*")):
        instrument = inst_dir.name
        for md_path in sorted(inst_dir.glob("*.md")):
            fm, body = parse_frontmatter(md_path.read_text())
            if not fm or fm.get("type") != "weekly_forecast":
                continue

            # Extract setups from frontmatter + body
            setups = []
            for letter in ["A", "B", "C"]:
                s = _parse_setup_from_body(body, letter)
                if s:
                    setups.append(s)

            generated = fm.get("generated", "2000-01-01")
            if isinstance(generated, str):
                generated = date.fromisoformat(generated)
            wf = WeeklyForecast(
                week=fm.get("week", ""),
                generated=generated,
                instrument=instrument,
                macro_bias=fm.get("macro_bias", "NEUTRAL"),
                macro_confidence=fm.get("macro_confidence", "MEDIUM"),
                mtf_alignment=fm.get("mtf_alignment", "MIXED"),
                best_setup=fm.get("best_setup"),
                conviction=fm.get("conviction", "MEDIUM"),
                baseline_dfii10=_to_float(fm.get("baseline_dfii10")),
                baseline_dxy=_to_float(fm.get("baseline_dxy")),
                baseline_ratediff=_to_float(fm.get("baseline_ratediff")),
                weekend_gap_pct=_to_float(fm.get("weekend_gap_pct")),
                cot_mm_net=_to_int(fm.get("cot_mm_net")),
                cot_mm_net_chg=_to_int(fm.get("cot_mm_net_chg")),
                etf_gld_tonnes=_to_float(fm.get("etf_gld_tonnes")),
                etf_gld_wk_chg=_to_float(fm.get("etf_gld_wk_chg")),
                macro_drivers=[],
                setups=setups,
                adx_regime=fm.get("adx_regime", "RANGING"),
                d1_atr=fm.get("d1_atr", 0.0),
                h4_atr=fm.get("h4_atr", 0.0),
                d1_atr_compressed=bool(fm.get("d1_atr_compressed", False)),
            )
            try:
                create_weekly_forecast(wf)
                count += 1
                print(f"  ✅ Migrated weekly forecast: {instrument} {wf.week}")
            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    print(f"  ⏭️  Skipped existing weekly forecast: {instrument} {wf.week}")
                else:
                    print(f"  ⚠️  Failed weekly forecast {md_path}: {e}")
    return count


def _parse_setup_from_body(body: str, letter: str) -> Setup | None:
    """Best-effort parse of a setup table from markdown body."""
    # Look for section header like "## Setup A — ..."
    header_pat = re.compile(rf"## Setup {letter}\s*[-–—]\s*(.+?)\s*\[([\d.]+)/10\]\s*(\w+)", re.IGNORECASE)
    m = header_pat.search(body)
    if not m:
        return None

    label, score_str, conviction = m.group(1), m.group(2), m.group(3)
    score = float(score_str)

    # Extract direction from body table
    dir_pat = re.compile(rf"## Setup {letter}.*?(BUY|SELL)", re.IGNORECASE | re.DOTALL)
    dir_m = dir_pat.search(body[m.start():m.start()+800])
    raw_dir = dir_m.group(1).upper() if dir_m else "BUY"
    direction = "LONG" if raw_dir == "BUY" else "SHORT"

    # Extract zone
    zone_pat = re.compile(r"Zone\s*\|\s*\$?([\d,.]+)\s*[–-]\s*\$?([\d,.]+)")
    zone_m = zone_pat.search(body[m.start():m.start()+800])
    if zone_m:
        bottom = float(zone_m.group(1).replace(",", ""))
        top = float(zone_m.group(2).replace(",", ""))
    else:
        bottom, top = 0.0, 0.0

    # Extract limit, stop, tp, lots
    def _extract(pattern: str, text: str, default: float = 0.0) -> float:
        mm = re.search(pattern, text)
        if mm:
            return float(mm.group(1).replace(",", ""))
        return default

    segment = body[m.start():m.start()+1200]
    limit = _extract(r"Limit\s*\|\s*\$?([\d,.]+)", segment)
    stop = _extract(r"Stop\s*\|\s*\$?([\d,.]+)", segment)
    tp = _extract(r"TP\s*\|\s*\$?([\d,.]+)", segment)
    lots = _extract(r"Lots\s*\|\s*\$?([\d,.]+)", segment)
    stop_dist = _extract(r"Stop distance\s*\|\s*\$?([\d,.]+)", segment)
    offset = _extract(r"Offset\s*\|\s*\$?([\d,.]+)", segment)
    r_mult = _extract(r"[=\(]\s*([\d.]+)R", segment)

    return Setup(
        letter=SetupLetter(letter),
        label=label.strip(),
        direction=Direction(direction),
        zone_top=top,
        zone_bottom=bottom,
        score=score,
        conviction=conviction,
        stop_distance=stop_dist,
        entry_offset=offset,
        limit_price=limit,
        stop_price=stop,
        tp_price=tp,
        lots=lots,
        r_multiple=r_mult,
        invalidation_rule="",
        tp_anchor_name="",
    )


def migrate_daily_validations() -> int:
    count = 0
    for inst_dir in sorted(Path("forecasts/daily").glob("*")):
        instrument = inst_dir.name
        for md_path in sorted(inst_dir.glob("*.md")):
            fm, body = parse_frontmatter(md_path.read_text())
            if not fm or fm.get("type") != "daily_validation":
                continue

            hard_blocks = []
            validation_gates = []

            # Best-effort parse hard blocks and gates from body tables
            # (frontmatter carries the structured data; body is prose)
            v1 = bool(fm.get("v1_structure_intact", True))
            v3 = bool(fm.get("v3_news_clear", True))
            hard_blocks.append(HardBlock(name="V1", passed=v1, note=""))
            hard_blocks.append(HardBlock(name="V3", passed=v3, note=""))

            g1 = bool(fm.get("g1_mtf_structure", False))
            g3 = bool(fm.get("g3_dfii10_slope", False))
            g2 = bool(fm.get("g2_atr_compressed", False))
            v2 = bool(fm.get("v2_macro_drift", False))
            validation_gates.append(ValidationGate(code="G1", name="H4+H1 structure aligned", weight=4.0, passed=g1, note=""))
            validation_gates.append(ValidationGate(code="G3", name="DFII10 slope supports", weight=3.5, passed=g3, note=""))
            validation_gates.append(ValidationGate(code="G2", name="D1 ATR compressed", weight=1.5, passed=g2, note=""))
            validation_gates.append(ValidationGate(code="V2", name="Macro drift OK", weight=1.0, passed=v2, note=""))

            dv_date = fm.get("date", "2000-01-01")
            if isinstance(dv_date, str):
                dv_date = date.fromisoformat(dv_date)
            dv = DailyValidation(
                date=dv_date,
                week=fm.get("week", ""),
                instrument=instrument,
                active_setup=fm.get("active_setup"),
                hard_blocks=hard_blocks,
                validation_gates=validation_gates,
                validation_score=float(fm.get("validation_score", 0.0)),
                floor_used=6.5 if fm.get("adx_regime") == "TRANSITIONAL" else 6.0,
                h1_trigger_present=bool(fm.get("h1_trigger_present", False)),
                weekly_confluence_score=float(fm.get("weekly_confluence_score", 0.0)),
                stop_distance=float(fm.get("stop_distance", 0.0)),
                structural_dist=float(fm.get("structural_dist", 0.0)),
                entry_offset=float(fm.get("entry_offset", 0.0)),
                order_result=fm.get("order_limit", "NO_TRADE"),
                limit_price=_to_float(fm.get("limit_price")),
                limit_direction=("LONG" if fm.get("limit_direction") == "BUY" else
                                 "SHORT" if fm.get("limit_direction") == "SELL" else
                                 None),
                limit_expires=_parse_datetime(fm.get("limit_expires")),
                h4_atr=float(fm.get("h4_atr", 0.0)),
                d1_atr=float(fm.get("d1_atr", 0.0)),
                d1_atr_compressed=bool(fm.get("d1_atr_compressed", False)),
                dfii10_slope=float(fm.get("dfii10_slope", 0.0)),
                dfii10_drift=float(fm.get("dfii10_drift", 0.0)),
                vix=fm.get("vix"),
                asia_range=fm.get("asia_range"),
            )
            try:
                create_daily_validation(dv)
                count += 1
                print(f"  ✅ Migrated daily validation: {instrument} {dv.date}")
            except Exception as e:
                print(f"  ⚠️  Failed daily validation {md_path}: {e}")
    return count


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    value = value.replace(" UTC", "")
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            return None


def migrate_trades() -> int:
    csv_path = Path("data/trades_log.csv")
    if not csv_path.exists():
        print("  ℹ️  No trades_log.csv found.")
        return 0

    count = 0
    with csv_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row.get("date"):
                continue
            try:
                t = Trade(
                    date=date.fromisoformat(row["date"]),
                    week=row["week"],
                    instrument=row.get("instrument", "xauusd"),
                    setup=row["setup"],
                    direction=row["direction"],
                    entry=float(row["entry"]),
                    sl=float(row["sl"]),
                    tp=float(row["tp"]),
                    lots=float(row["lots"]),
                    stop_dist=float(row["stop_dist"]),
                    r_planned=float(row["r_planned"]),
                    fill_time=datetime.fromisoformat(row["fill_time"]),
                    exit_time=datetime.fromisoformat(row["exit_time"]) if row.get("exit_time") else None,
                    exit_px=float(row["exit_px"]) if row.get("exit_px") else None,
                    exit_reason=row["exit_reason"] if row.get("exit_reason") else None,
                    r_actual=float(row["r_actual"]) if row.get("r_actual") else None,
                    mfe=float(row["mfe"]) if row.get("mfe") else None,
                    mae=float(row["mae"]) if row.get("mae") else None,
                    notes=row.get("notes"),
                )
                create_trade(t)
                count += 1
            except Exception as e:
                print(f"  ⚠️  Failed trade row: {e}")
    print(f"  ✅ Migrated {count} trades.")
    return count


def main():
    print("Initializing database...")
    init_db()
    print("Migrating weekly forecasts...")
    wf_count = migrate_weekly_forecasts()
    print(f"  → {wf_count} weekly forecasts migrated.\n")

    print("Migrating daily validations...")
    dv_count = migrate_daily_validations()
    print(f"  → {dv_count} daily validations migrated.\n")

    print("Migrating trades...")
    tr_count = migrate_trades()
    print(f"  → {tr_count} trades migrated.\n")

    print("Migration complete.")


if __name__ == "__main__":
    main()
