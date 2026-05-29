"""Render DailyValidation → markdown with YAML frontmatter."""

from __future__ import annotations

import yaml

from schemas import DailyValidation


def render_daily_validation(dv: DailyValidation) -> str:
    """Generate a markdown document matching the existing daily validation format."""
    frontmatter = _build_frontmatter(dv)
    body = _build_body(dv)
    return f"---\n{yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True)}---\n\n{body}"


def _build_frontmatter(dv: DailyValidation) -> dict:
    fm: dict = {
        "type": "daily_validation",
        "date": dv.date.isoformat(),
        "week": dv.week,
        "active_setup": dv.active_setup.value if dv.active_setup else None,
        "v1_structure_intact": dv.hard_blocks[0].passed if dv.hard_blocks and dv.hard_blocks[0].name == "V1" else True,
        "v3_news_clear": next((hb.passed for hb in dv.hard_blocks if hb.name == "V3"), True),
        "validation_score": dv.validation_score,
        "h1_trigger_present": dv.h1_trigger_present,
        "weekly_confluence_score": dv.weekly_confluence_score,
        "stop_distance": dv.stop_distance,
        "entry_offset": dv.entry_offset,
        "order_limit": dv.order_result.value,
        "h4_atr": dv.h4_atr,
        "d1_atr": dv.d1_atr,
        "d1_atr_compressed": dv.d1_atr_compressed,
        "dfii10_slope": dv.dfii10_slope,
        "dfii10_drift": dv.dfii10_drift,
    }
    if dv.limit_price is not None:
        fm["limit_price"] = dv.limit_price
    if dv.limit_direction is not None:
        fm["limit_direction"] = dv.limit_direction.value
    if dv.limit_expires is not None:
        fm["limit_expires"] = dv.limit_expires.strftime("%Y-%m-%d %H:%M UTC")
    if dv.vix is not None:
        fm["vix"] = dv.vix
    if dv.asia_range is not None:
        fm["asia_range"] = dv.asia_range
    return fm


def _build_body(dv: DailyValidation) -> str:
    lines: list[str] = []
    active = dv.active_setup.value if dv.active_setup else "NONE"
    lines.append(f"# Validation — {dv.date} (Setup {active} from [[{dv.week}]])")
    lines.append("")

    # Hard Blocks
    lines.append("## Hard Blocks")
    lines.append("")
    lines.append("| | Block | Result | Note |")
    lines.append("|---|---|---|---|")
    for hb in dv.hard_blocks:
        icon = "✅" if hb.passed else "❌"
        lines.append(f"| {hb.name} | {hb.name} | {icon} | {hb.note} |")
    lines.append("")

    # Validation Score
    lines.append(f"## Validation Score (max 10.0)")
    lines.append("")
    lines.append("| | Condition | Pts | Result | Note |")
    lines.append("|---|---|---|---|---|")
    for vg in dv.validation_gates:
        icon = "✅" if vg.passed else "❌"
        lines.append(f"| {vg.code} | {vg.name} | {vg.weight} | {icon} | {vg.note} |")
    lines.append(f"| | **Total** | **{dv.validation_score} / 10.0** | | ≥ {dv.floor_used} {'✅' if dv.validation_score >= dv.floor_used else '❌'} |")
    lines.append("")

    # H1 Trigger
    lines.append("## H1 Trigger")
    lines.append("")
    if dv.h1_trigger_present:
        lines.append(f"**YES** — {dv.h1_trigger_description or 'trigger present'}")
    else:
        lines.append("**NO** — no valid H1 trigger")
    lines.append("")

    # Order Limit Calc
    if dv.order_result.value in ("PLACED", "WATCH"):
        lines.append("## Order Limit Calc")
        lines.append("")
        lines.append("```")
        lines.append(f"stop_distance   = {dv.stop_distance}")
        lines.append(f"entry_offset    = {dv.entry_offset}")
        if dv.limit_price is not None:
            lines.append(f"limit_price     = {dv.limit_price}")
        lines.append("```")
        lines.append("")

    # Result
    lines.append("## Result")
    lines.append("")
    if dv.order_result.value == "PLACED":
        dir_str = dv.limit_direction.value if dv.limit_direction else ""
        lines.append(f"✅ ORDER LIMIT: {dir_str} {dv.limit_price} | expires {dv.limit_expires.strftime('%Y-%m-%d %H:%M UTC') if dv.limit_expires else '—'}")
    elif dv.order_result.value == "WATCH":
        lines.append("👁 WATCH — validation passed, no H1 trigger or zone unreachable")
    elif dv.order_result.value == "NO_TRADE":
        lines.append("❌ NO TRADE — score below floor or hard block")
    elif dv.order_result.value == "INVALIDATED":
        lines.append("❌ INVALIDATED — structure broken or news block")
    lines.append("")

    # Intraday updates
    for upd in dv.intraday_updates:
        lines.append(f"## Intraday Update")
        lines.append("")
        lines.append(upd)
        lines.append("")

    return "\n".join(lines)
