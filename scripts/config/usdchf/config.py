"""USDCHF instrument config — USD vs Swiss franc. Inherits USD-base defaults from config._fx_usd_base.

D024 pair #4 — second USD-base pair (clone of the usdcad class, no oil leg). Long USDCHF =
long USD (USD_BETA_SIGN=+1). CHF-quoted pip value runs ~25% over the nominal $10/pip majors
convention (historical pip-economics note; system tracks risk in R-multiples only, no live
$/pip conversion).

CHF specifics:
  - No daily FRED series for the SNB policy rate → RATE_FOREIGN=None.
  - CHF is a safe-haven currency: risk-off → CHF bid → USDCHF DOWN. VIX polarity is an open
    empirical question (both legs are havens) — decide from the scan, not by template.
  - SNB intervention regime: SNB historically intervenes against CHF strength (floor era
    2011-2015, ongoing smoothing). Mean-reversion near multi-year USDCHF lows can be
    SNB-assisted; SNB rate decisions are quarterly (thin calendar vs other pairs).
  - COT 6S INVERTED: spec long CHF futures = SHORT USDCHF.
  - Events: US tier-1 shared + SNB quarterly decision + CH CPI (monthly, low vol impact).
Signal character decided by scan, not assumed.
"""

from config._fx_usd_base import *  # noqa: F401,F403  (USD-base shared defaults)

SYMBOL       = "USD/CHF"
SYM_CLEAN    = "usdchf"
DISPLAY_NAME = "USDCHF"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/usdchf"
PULL_DIR = "data/weekly_pull/usdchf"

# Foreign carry leg: SNB policy rate has NO daily FRED series → carry leg disabled.
RATE_FOREIGN      = None
RATE_FOREIGN_NAME = "SNB policy rate"
FOREIGN_CCY       = "CH"

# Direction (DGS2, flipped) + US carry (DFF) + risk (VIXCLS). No commodity leg.
FRED_SERIES = FRED_SERIES_BASE

# V1b invalidation buffer: placeholder 4 pips — calibrate from ATR after backfill.
V1B_BUFFER = 0.0004

# COT — CME Swiss franc futures (6S). INVERTED (see _fx_usd_base).
COT_CONTRACT_NAME = "SWISS FRANC - CHICAGO MERCANTILE EXCHANGE"
