"""EURJPY instrument config — euro vs Japanese yen CROSS, JPY-quoted. Inherits config._fx_base.

D024 pair #6 — FIRST cross-JPY pair: combines the eurgbp cross pattern (USD_BETA_SIGN=0,
no USD leg, no DXY rows) with the usdjpy JPY pip plumbing (PIP_SIZE 0.01, PRICE_DP 3,
TICK_MULTIPLIER 650 static).

Character expectations (verify by scan, never assume):
  - EURJPY = EURUSD × USDJPY — the classic risk-on/risk-off carry barometer.
    Risk-off → carry unwind → JPY bid → EURJPY DOWN. VIX polarity likely matters MORE
    here than on either leg alone; read it empirically.
  - Macro legs: EUR = ECBDFR (daily, near-flat policy step); JPY = NO daily FRED series
    (BoJ). So the cross rate-diff cannot be computed — macro mode runs ONE-LEG (EUR only),
    expected thin/dead like eurgbp (EG2 result). Confluence likely price/structure driven.
  - MoF/BoJ intervention: interventions target USDJPY but slam ALL JPY crosses
    simultaneously — the 2022/2024 300-500 pip USDJPY slams moved EURJPY comparably.
    Same hard-block regime as usdjpy (BoJ decision + active MoF jawboning).
  - Events: ECB decision + BoJ decision + Tokyo CPI + MoF intervention watch
    (NOT US tier-1 first-order, but USD legs transmit — treat US CPI/FOMC as volatility risk).

COT: direct CME cross contract EXISTS ("EURO FX/JAPANESE YEN XRATE") — long contract =
long EURJPY, DIRECT read (not inverted). Thin: OI ~21k vs 6J ~250k — treat extremes
with caution, W/W swings are small-number noise.
"""

from config._fx_base import *  # noqa: F401,F403  (FX shared defaults)

SYMBOL       = "EUR/JPY"
SYM_CLEAN    = "eurjpy"
DISPLAY_NAME = "EURJPY"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/eurjpy"
PULL_DIR = "data/weekly_pull/eurjpy"

# ── No USD leg: EURJPY is EUR vs JPY. USD correlation guard does not apply. ──
USD_BETA_SIGN = 0

# ── JPY pip plumbing (same as usdjpy — quote ccy is JPY) ──
PIP_SIZE        = 0.01     # 1 pip; big figure = 1.00
PRICE_DP        = 3        # display/rounding precision
TICK_MULTIPLIER = 650      # static ≈ 100000/USDJPY(154); legacy price-scale constant, no
                           # longer used for lot sizing — retained for PRICE_DP heuristic
                           # (quote ccy = JPY, so pip value depends on USDJPY, NOT EURJPY)
MIN_BAR_RANGE   = 0.03     # 3 JPY pips (vestigial — session filter is time-based)

# V1b invalidation buffer: ~10% median H4 ATR (median 42 JPY pips, 2020-2026 trading-day
# bars) → 4 pips. Same value as usdjpy despite 1.37× D1 ATR — H4 medians land close.
V1B_BUFFER = 0.04

# ── Macro: one-leg cross — EUR (ECBDFR) only; JPY has NO daily FRED series ──
# MACRO_MODE="cross_rate_diff" with RATE_GBP=None → pipeline runs the EUR-leg-only branch
# (X9/X10 in backtest; diff/X1-X8 skipped). Expected thin (ECBDFR is a flat policy step).
MACRO_MODE        = "cross_rate_diff"
RATE_EUR          = "ECBDFR"    # EUR policy leg (daily, step function)
RATE_GBP          = None        # ← no second daily leg (BoJ has no daily FRED series)
RATE_FOREIGN      = None        # pipeline compat (snapshot foreign-leg field)
RATE_FOREIGN_NAME = "BoJ policy rate"
FOREIGN_CCY       = "JP"
FRED_SERIES = FRED_SERIES_BASE + ["ECBDFR"]

# ── COT — direct CME EUR/JPY cross-rate futures. DIRECT read (long = long EURJPY).
#    Thin contract (OI ~21k): extremes are noisy, low weight. ──
COT_ENABLED       = True
COT_CONTRACT_NAME = "EURO FX/JAPANESE YEN XRATE - CHICAGO MERCANTILE EXCHANGE"

# ── No clean EURJPY futures continuous for a volume-profile proxy. ──
VP_TICKER = None
