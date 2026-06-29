"""GBPJPY instrument config — pound vs Japanese yen CROSS, JPY-quoted. Inherits config._fx_base.

D024 pair #7 (LAST) — second cross-JPY pair: same skeleton as eurjpy (USD_BETA_SIGN=0,
no USD leg, no DXY rows; JPY pip plumbing PIP_SIZE 0.01, PRICE_DP 3, TICK_MULTIPLIER 650
static — quote ccy is JPY, so $/pip depends on USDJPY, not GBPJPY).

Character expectations (verify by scan, never assume):
  - GBPJPY = "the Beast"/"Dragon" — historically 1.5-2× EURJPY ATR. Highest-vol pair in
    the book; V1B_BUFFER must be recalibrated from its own H4 ATR median, not copied.
  - Carry cross with the widest rate gap (BoE ~4% vs BoJ ~0.5%) → strong long-drift
    floor expected, possibly trendier than EURJPY (carry-trend vs mean-reversion —
    scan may come back NO-GO for the fade template).
  - Macro legs: GBP = SONIA (IUDSOIA, daily); JPY = NO daily FRED series (BoJ).
    → ONE-LEG macro branch (RATE_GBP=None), live leg = SONIA via RATE_EUR slot.
  - MoF/BoJ intervention: targets USDJPY but slams ALL JPY crosses; GBPJPY moves are
    the LARGEST of the crosses (vol-amplified). Same hard-block regime.
  - Events: BoE decision + BoJ decision + UK CPI + Tokyo CPI + MoF intervention watch.
    US tier-1 transmits through both legs — volatility caution, not first-order.

COT: NO direct CFTC cross contract (2026 disagg zip has only EUR/GBP + EUR/JPY XRATEs).
COT disabled — do not synthesize from 6B/6J (different question, noisy).
"""

from config._fx_base import *  # noqa: F401,F403  (FX shared defaults)

SYMBOL       = "GBP/JPY"
SYM_CLEAN    = "gbpjpy"
DISPLAY_NAME = "GBPJPY"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/gbpjpy"
PULL_DIR = "data/weekly_pull/gbpjpy"

# ── No USD leg: GBPJPY is GBP vs JPY. USD correlation guard does not apply. ──
USD_BETA_SIGN = 0

# ── JPY pip plumbing (same as usdjpy/eurjpy — quote ccy is JPY) ──
PIP_SIZE        = 0.01     # 1 pip; big figure = 1.00
PRICE_DP        = 3        # display/rounding precision
TICK_MULTIPLIER = 650      # static ≈ 100000/USDJPY(154); legacy price-scale constant, no
                           # longer used for lot sizing — retained for PRICE_DP heuristic
MIN_BAR_RANGE   = 0.05     # 5 JPY pips (vestigial — session filter is time-based; high-ATR pair)

# V1b invalidation buffer: ~10% median H4 ATR (median 54 JPY pips, 2020-2026 trading-day
# bars, range>=0.05 filter) → 5 pips. 1.28× eurjpy's 0.04 — highest in the book.
V1B_BUFFER = 0.05

# ── Macro: one-leg cross — GBP (SONIA) only; JPY has NO daily FRED series ──
# MACRO_MODE="cross_rate_diff" with RATE_GBP=None → one-leg branch. RATE_EUR slot
# carries the LIVE leg series (SONIA here — slot name is historical, see weekly_pull).
MACRO_MODE        = "cross_rate_diff"
RATE_EUR          = "IUDSOIA"   # live leg = GBP SONIA (slot name legacy from eurgbp)
RATE_GBP          = None        # ← no second daily leg (BoJ has no daily FRED series)
RATE_FOREIGN      = None        # pipeline compat (snapshot foreign-leg field)
RATE_FOREIGN_NAME = "BoJ policy rate"
FOREIGN_CCY       = "JP"
LIVE_LEG_LABEL    = "GBP SONIA (IUDSOIA)"
LIVE_LEG_CCY      = "GBP"
BASELINE_LABEL    = "baseline_sonia_rate"
FRED_SERIES = FRED_SERIES_BASE + ["IUDSOIA"]

# ── COT — no direct CFTC GBP/JPY cross contract exists. Disabled. ──
COT_ENABLED       = False
COT_CONTRACT_NAME = None

# ── No clean GBPJPY futures continuous for a volume-profile proxy. ──
VP_TICKER = None
