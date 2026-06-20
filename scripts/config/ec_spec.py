"""
ec_spec.py — per-instrument Entry Confluence (R2) component table.

One entry per pair: list of (code, weight, predicate_key, params), summing to 10.0,
transcribed from each `wiki/system/{inst}/confluence_criteria.md` R2 table. Consumed
by `entry_confluence.score()`; predicate_key resolves to a function in that module.

REVIEW BEFORE TRUSTING R2 (fidelity gate, plan/D031): this maps prose rows to the
nearest deterministic predicate. Bespoke per-pair oscillator/threshold/session picks
are approximated to the generic fade thresholds. Verify each row against the markdown.

Predicate keys: e0 · structure_intact · h4_osc_extreme · h1_osc_extreme ·
d1_osc_extreme · band_touch_h4 · band_touch_h1 · h1osc_or_h4band · squeeze_or_h4osc ·
adx_below{thr} · atr_compression · squeeze · h4_structure_aligned · dxy_slope ·
realyield_slope · macro_drift_ok · macro_regime · session_window{long,short}.
"""

EC_SPEC = {
    # xauusd — MOMENTUM/continuation: E1 is structure-aligned, macro legs live (DFII10/DXY).
    "xauusd": [
        ("E0", 3.0, "e0", None),
        ("E1", 2.5, "h4_structure_aligned", None),
        ("E2", 2.0, "realyield_slope", None),
        ("E3", 1.0, "macro_drift_ok", None),
        ("E4", 1.0, "atr_compression", None),
        ("E5", 0.5, "dxy_slope", None),
    ],
    # eurusd — mean-reversion fade, fully price-based.
    "eurusd": [
        ("E0", 3.0, "e0", None),
        ("E1", 2.5, "h4_osc_extreme", None),
        ("E2", 1.5, "band_touch_h4", None),
        ("E3", 1.0, "adx_below", {"thr": 25}),
        ("E4", 1.0, "atr_compression", None),
        ("E5", 1.0, "structure_intact", None),
    ],
    # gbpusd — D1 osc primary, H1 osc secondary.
    "gbpusd": [
        ("E0", 3.0, "e0", None),
        ("E1", 2.5, "d1_osc_extreme", None),
        ("E2", 1.5, "h1_osc_extreme", None),
        ("E3", 1.0, "adx_below", {"thr": 25}),
        ("E4", 1.0, "structure_intact", None),
        ("E5", 1.0, "atr_compression", None),
    ],
    # eurgbp — cross, D1 osc primary, H1 osc secondary, no USD leg.
    "eurgbp": [
        ("E0", 3.0, "e0", None),
        ("E1", 2.5, "d1_osc_extreme", None),
        ("E2", 1.5, "h1_osc_extreme", None),
        ("E3", 1.0, "adx_below", {"thr": 25}),
        ("E4", 1.0, "structure_intact", None),
        ("E5", 1.0, "atr_compression", None),
    ],
    # audusd — H4 osc primary; E2 short=H1 osc / long=H4 band; E4 macro regime (VIX/US2Y).
    "audusd": [
        ("E0", 3.0, "e0", None),
        ("E1", 2.5, "h4_osc_extreme", None),
        ("E2", 1.5, "h1osc_or_h4band", None),
        ("E3", 1.0, "adx_below", {"thr": 25}),
        ("E4", 1.0, "macro_regime", None),
        ("E5", 1.0, "structure_intact", None),
    ],
    # nzdusd — like aud but E4 = squeeze (NZD's strongest signal).
    "nzdusd": [
        ("E0", 3.0, "e0", None),
        ("E1", 2.5, "h4_osc_extreme", None),
        ("E2", 1.5, "h1osc_or_h4band", None),
        ("E3", 1.0, "adx_below", {"thr": 25}),
        ("E4", 1.0, "squeeze", None),
        ("E5", 1.0, "structure_intact", None),
    ],
    # usdcad — H4 osc primary, H1 osc secondary, E4 macro regime (VIX fade-USD).
    "usdcad": [
        ("E0", 3.0, "e0", None),
        ("E1", 2.5, "h4_osc_extreme", None),
        ("E2", 1.5, "h1_osc_extreme", None),
        ("E3", 1.0, "adx_below", {"thr": 25}),
        ("E4", 1.0, "macro_regime", None),
        ("E5", 1.0, "structure_intact", None),
    ],
    # usdchf — H1 osc primary (2.5), DXY slope live leg (1.5), squeeze.
    "usdchf": [
        ("E0", 3.0, "e0", None),
        ("E1", 2.5, "h1_osc_extreme", None),
        ("E2", 1.5, "dxy_slope", None),
        ("E3", 1.0, "squeeze", None),
        ("E4", 1.0, "adx_below", {"thr": 25}),
        ("E5", 1.0, "structure_intact", None),
    ],
    # usdjpy — asymmetric: E1 long=squeeze/calm, short=H4 osc; E2 DXY; E3 NY session (long).
    "usdjpy": [
        ("E0", 3.0, "e0", None),
        ("E1", 2.5, "squeeze_or_h4osc", None),
        ("E2", 1.5, "dxy_slope", None),
        ("E3", 1.0, "session_window", {"long": (12, 16)}),
        ("E4", 1.0, "structure_intact", None),
        ("E5", 1.0, "adx_below", {"thr": 25}),
    ],
    # eurjpy — cross fade, osc both sides; E2 session (long NY overlap / short London open).
    "eurjpy": [
        ("E0", 3.0, "e0", None),
        ("E1", 2.5, "h4_osc_extreme", None),
        ("E2", 1.5, "session_window", {"long": (12, 16), "short": (7, 9)}),
        ("E3", 1.0, "squeeze", None),
        ("E4", 1.0, "structure_intact", None),
        ("E5", 1.0, "adx_below", {"thr": 25}),
    ],
    # gbpjpy — cross fade; E2 long NY overlap session; E3 H1 timing structure (osc proxy).
    "gbpjpy": [
        ("E0", 3.0, "e0", None),
        ("E1", 2.5, "h4_osc_extreme", None),
        ("E2", 1.5, "session_window", {"long": (12, 16)}),
        ("E3", 1.0, "h1_osc_extreme", None),
        ("E4", 1.0, "structure_intact", None),
        ("E5", 1.0, "adx_below", {"thr": 25}),
    ],
}

# Generic fallback (eurusd-shaped) for any instrument missing a spec.
DEFAULT_SPEC = EC_SPEC["eurusd"]
