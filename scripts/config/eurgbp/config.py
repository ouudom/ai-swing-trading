"""EURGBP instrument config — euro vs sterling CROSS. Inherits FX defaults from config._fx_base.

⚠️ EURGBP is a CROSS, not a USD-major. It has NO USD leg — its driver is ECB-vs-BoE
(EUR vs GBP rate/policy differential), not DGS2/DXY/VIX-risk-off. The macro block below is a
PLACEHOLDER inherited from _fx_base so the pipeline runs; the real EUR-GBP macro model
(ECB−BoE policy diff, German–UK yield spread) is EG2 of the onboarding plan and must be
rebuilt + backtested before EURGBP trades live. See wiki/system/core/currency_exposure.md
(Architecture B / EURGBP onboarding) and decisions.md D022.

Status: EG1 (config + data) for the EG3 go/no-go backtest. NOT yet a live tradable instrument.
"""

from config._fx_base import *  # noqa: F401,F403  (FX shared defaults)

SYMBOL       = "EUR/GBP"
SYM_CLEAN    = "eurgbp"
DISPLAY_NAME = "EURGBP"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/eurgbp"
PULL_DIR = "data/weekly_pull/eurgbp"

# ── No USD leg: EURGBP is EUR/GBP. The USD correlation guard does not apply. ──
USD_BETA_SIGN = 0

# ── Low-volatility cross: ATR runs ~half a USD-major (16yr D1 median 60 pips vs GBP 112).
#    Tighten the flatline filter + invalidation buffer accordingly. ──
MIN_BAR_RANGE = 0.0002      # 2 pips (vs 3 for majors) — H4 trading-day ATR filter
V1B_BUFFER    = 0.0004      # 4 pips past zone, 2 consecutive H4 closes (vs 5/6 for majors)

# ── PIP ECONOMICS — EURGBP is nominally GBP-quoted (historical note). ──────────
# OPERATOR DECISION (historical): treat the same as the majors — NO GBP→USD conversion.
# System tracks risk in R-multiples only now; no live $/pip or quote→USD conversion is
# performed anywhere in the pipeline.
QUOTE_CCY            = "GBP"
SIZING_FX_CONVERT    = False       # operator: no quote→USD conversion (legacy flag, unused by sizing — R-multiple only)

# ── Macro: EG2 cross model — ECB vs BoE (NOT US/DXY) ───────────────────────────
# EURGBP has no USD leg. Direction driver = EUR-vs-GBP rate differential.
#   EUR leg = ECB Deposit Facility Rate (ECBDFR, daily — but a near-flat policy step)
#   GBP leg = SONIA (IUDSOIA, daily — moves with BoE expectations)
#   diff = ECBDFR − SONIA; diff rising (EUR rates up rel to GBP) → EURGBP UP.
# DATA LIMIT: no free daily German/UK *market* yield (2Y/10Y) on FRED — only the policy/
# overnight legs are daily. So the differential is GBP-side-driven (ECBDFR flat). German–UK
# sovereign spread (richer two-sided signal) needs ECB SDW / a paid daily source = EG2b follow-on.
#
# EG2 RESULT (wiki/research/eurgbp/signal-results.md): cross macro is THIN/DEAD on free daily data —
# all 20d rate slopes are noise; only X3 (diff widening, t=1.50) + E16 (VIX-spike, t=1.68) hint,
# both sub-significant. ⇒ EURGBP confluence is PRICE/structure mean-reversion; macro = LOW-weight
# tilt only, NOT a gate. 🔑 VIX risk-off polarity is INVERTED vs USD-majors (risk-off → EURGBP UP),
# so the FX VIX-veto-LONGS rule does NOT apply to this cross (EG4).
MACRO_MODE        = "cross_rate_diff"
RATE_EUR          = "ECBDFR"    # EUR policy leg
RATE_GBP          = "IUDSOIA"   # GBP rate leg (SONIA)
RATE_FOREIGN      = "IUDSOIA"   # kept for pipeline compat (snapshot foreign-leg field)
RATE_FOREIGN_NAME = "UK SONIA"
FOREIGN_CCY       = "UK"
FRED_SERIES = FRED_SERIES_BASE + ["ECBDFR", "IUDSOIA"]

# ── COT: no single CFTC EURGBP contract. Cross positioning must be DERIVED from 6E vs 6B
#    (EG4 work) — disabled for now rather than mislabel. ──
COT_ENABLED       = False
COT_CONTRACT_NAME = None

# ── No clean EURGBP futures continuous for a volume-profile proxy. ──
VP_TICKER = None
