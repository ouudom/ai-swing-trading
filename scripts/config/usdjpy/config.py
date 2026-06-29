"""USDJPY instrument config — USD vs Japanese yen. Inherits USD-base defaults from config._fx_usd_base.

D024 pair #5 — third USD-base pair and FIRST JPY-quoted pair. Long USDJPY = long USD
(USD_BETA_SIGN=+1). JPY pip plumbing differs from every prior pair:
  - PIP_SIZE = 0.01 (price ~155, quoted to 3dp; 1 big figure = 1.00 = 100 pips).
  - TICK_MULTIPLIER = 650, STATIC (D024 operator ruling, historical — no longer used for
    lot sizing, system is R-multiple only): ≈ 100,000/USDJPY ≈ 100,000/154. The non-JPY
    value (TICK=100000) would be wrong by ~155× here, not a tolerable drift. Retained only
    as a PRICE_DP display-precision heuristic.
  - PRICE_DP = 3 — weekly_pull display/rounding (TICK heuristic would give 5dp).

JPY specifics:
  - No daily FRED series for the BoJ policy rate → RATE_FOREIGN=None.
  - JPY is a safe-haven / funding currency: risk-off → carry unwind → JPY bid → USDJPY DOWN.
    VIX polarity is an open empirical question (both legs haven-adjacent; CHF scanned as
    washout) — decide from the scan, not by template.
  - Carry-trade regime: US-JP rate gap historically the dominant macro; BoJ
    intervention (MoF) against JPY weakness near multi-decade USDJPY highs (2022/2024
    150–162 zone) — violent 300-500 pip interventions, mean-reversion can be MoF-assisted.
  - BoJ decisions are ~8/yr, unscheduled-intervention risk is continuous near highs.
  - COT 6J INVERTED: spec long JPY futures = SHORT USDJPY.
  - Events: US tier-1 shared + BoJ decision + Tokyo CPI + MoF intervention watch.
Signal character decided by scan, not assumed.
"""

from config._fx_usd_base import *  # noqa: F401,F403  (USD-base shared defaults)

SYMBOL       = "USD/JPY"
SYM_CLEAN    = "usdjpy"
DISPLAY_NAME = "USDJPY"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/usdjpy"
PULL_DIR = "data/weekly_pull/usdjpy"

# ── JPY pip plumbing (see module docstring) ──
PIP_SIZE        = 0.01     # 1 pip; big figure = 1.00
PRICE_DP        = 3        # display/rounding precision
TICK_MULTIPLIER = 650      # static ≈ 100000/154; legacy price-scale constant, no longer
                           # used for lot sizing — retained for PRICE_DP heuristic
MIN_BAR_RANGE   = 0.03     # 3 pips, JPY scale (vestigial — session filter is time-based)

# Foreign carry leg: BoJ policy rate has NO daily FRED series → carry leg disabled.
RATE_FOREIGN      = None
RATE_FOREIGN_NAME = "BoJ policy rate"
FOREIGN_CCY       = "JP"

# Direction (DGS2, flipped) + US carry (DFF) + risk (VIXCLS). No commodity leg.
FRED_SERIES = FRED_SERIES_BASE

# V1b invalidation buffer: placeholder 4 pips JPY-scale — calibrate from ATR after backfill.
V1B_BUFFER = 0.04

# COT — CME Japanese yen futures (6J). INVERTED (see _fx_usd_base).
COT_CONTRACT_NAME = "JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE"
