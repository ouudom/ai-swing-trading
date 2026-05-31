"""Render WeeklyForecast → markdown with YAML frontmatter."""

from __future__ import annotations

import yaml

from db.schemas import WeeklyForecast


def render_weekly_forecast(wf: WeeklyForecast) -> str:
    """Generate a markdown document matching the existing weekly forecast format."""
    frontmatter = _build_frontmatter(wf)
    body = _build_body(wf)
    return f"---\n{yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=True)}---\n\n{body}"


def _build_frontmatter(wf: WeeklyForecast) -> dict:
    fm: dict = {
        "type": "weekly_forecast",
        "week": wf.week,
        "generated": wf.generated.isoformat(),
        "macro_bias": wf.macro_bias.value,
        "macro_confidence": wf.macro_confidence.value,
        "mtf_alignment": wf.mtf_alignment.value,
        "best_setup": wf.best_setup.value if wf.best_setup else None,
        "conviction": wf.conviction.value,
    }
    if wf.baseline_dfii10 is not None:
        fm["baseline_dfii10"] = wf.baseline_dfii10
    if wf.baseline_dxy is not None:
        fm["baseline_dxy"] = wf.baseline_dxy
    if wf.baseline_ratediff is not None:
        fm["baseline_ratediff"] = wf.baseline_ratediff
    if wf.weekend_gap_pct is not None:
        fm["weekend_gap_pct"] = wf.weekend_gap_pct
    if wf.cot_mm_net is not None:
        fm["cot_mm_net"] = wf.cot_mm_net
    if wf.cot_mm_net_chg is not None:
        fm["cot_mm_net_chg"] = wf.cot_mm_net_chg
    if wf.etf_gld_tonnes is not None:
        fm["etf_gld_tonnes"] = wf.etf_gld_tonnes
    if wf.etf_gld_wk_chg is not None:
        fm["etf_gld_wk_chg"] = wf.etf_gld_wk_chg
    return fm


def _build_body(wf: WeeklyForecast) -> str:
    lines: list[str] = []
    instrument_upper = wf.instrument.upper()
    lines.append(f"# {instrument_upper} Weekly Forecast — {wf.week[5:]} (Mon {wf.generated})")
    lines.append("")

    # Macro
    lines.append(f"## Macro — {wf.macro_bias.value} / {wf.macro_confidence.value}")
    lines.append("")
    lines.append("| Driver | Value | Δ1W | Signal |")
    lines.append("|---|---|---|---|")
    for d in wf.macro_drivers:
        delta_str = f"{d.delta_1w:+.2f}" if d.delta_1w != 0 else "—"
        lines.append(f"| {d.name} | {d.value} | {delta_str} | {d.signal} |")
    lines.append("")

    # Technical
    lines.append(f"## Technical — ADX {wf.adx_regime.value}")
    lines.append("")
    lines.append(f"| | Value | Note |")
    lines.append(f"|---|---|---|")
    lines.append(f"| D1 ATR(14) | {wf.d1_atr} | {'compressed' if wf.d1_atr_compressed else 'expanded'} |")
    lines.append(f"| H4 ATR(14) | {wf.h4_atr} | — |")
    lines.append("")

    # Positioning
    lines.append("## Positioning")
    lines.append("")
    if wf.cot_mm_net is not None:
        lines.append(f"| COT MM net | {wf.cot_mm_net} |")
    if wf.etf_gld_tonnes is not None:
        lines.append(f"| GLD tonnes | {wf.etf_gld_tonnes}t |")
    lines.append("")

    # Pre-Screen Gates
    lines.append("## Pre-Screen Gates")
    lines.append("")
    lines.append("| Gate | Status | Note |")
    lines.append("|---|---|---|")
    # gates are not directly modeled; agent fills this in body
    lines.append("| G1 | — | see setups |")
    lines.append("")

    # Setups
    for s in wf.setups:
        lines.append(f"## Setup {s.letter.value} — {s.label} [{s.score}/10] {s.conviction.value}")
        lines.append("")
        sig_str = " / ".join(
            f"{'✅' if v else '❌'} {k}" for k, v in s.signals.items()
        )
        lines.append(f"| Direction | {s.direction.value} |")
        lines.append(f"| Zone | {s.zone_bottom} – {s.zone_top} |")
        lines.append(f"| Signals | {sig_str} |")
        lines.append(f"| Score | {s.score} / 10.0 |")
        lines.append(f"| Stop distance | {s.stop_distance} |")
        lines.append(f"| Offset | {s.entry_offset} |")
        lines.append(f"| Limit | {s.limit_price} |")
        lines.append(f"| Stop | {s.stop_price} |")
        lines.append(f"| TP | {s.tp_price} @ {s.tp_anchor_name} (= {s.r_multiple}R) |")
        lines.append(f"| Lots | {s.lots} |")
        lines.append(f"| Invalidation | {s.invalidation_rule} |")
        lines.append("")

    # Bias Statement
    lines.append("## Bias Statement")
    lines.append("")
    lines.append(f"{wf.macro_bias.value} / {wf.macro_confidence.value} / {wf.mtf_alignment.value} MTF.")
    lines.append("")

    return "\n".join(lines)
