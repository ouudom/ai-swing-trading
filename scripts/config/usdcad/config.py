"""USDCAD instrument config — USD vs loonie. Inherits USD-base defaults from config._fx_usd_base.

D024 pair #3 — FIRST USD-base pair. Long USDCAD = long USD (USD_BETA_SIGN=+1; DXY/US-rate
polarity flipped vs the USD-quote majors). CAD-quoted pip value runs ~28% under the nominal
$10/pip majors convention (historical pip-economics note; system tracks risk in R-multiples
only, no live $/pip conversion).

CAD specifics:
  - No daily FRED series for the BoC overnight rate (monthly OECD only) → RATE_FOREIGN=None.
  - 🛢 CAD is an oil currency: WTI (FRED DCOILWTICO, daily) added to FRED_SERIES and scanned
    via the W-rows in backtest_signals (oil up → CAD up → USDCAD DOWN).
  - COT 6C INVERTED: spec long CAD futures = SHORT USDCAD.
  - Events: US tier-1 shared + BoC rate decision + CAD CPI/jobs (often 12:30/13:30 UTC, same
    slot as US data → double-event days) + OPEC/oil shocks (caution).
Signal character decided by scan, not assumed.
"""

from config._fx_usd_base import *  # noqa: F401,F403  (USD-base shared defaults)

SYMBOL       = "USD/CAD"
SYM_CLEAN    = "usdcad"
DISPLAY_NAME = "USDCAD"

# Data paths (relative to project root)
TD_DIR   = "data/twelvedata/usdcad"
PULL_DIR = "data/weekly_pull/usdcad"

# Foreign carry leg: BoC overnight rate has NO daily FRED series → carry leg disabled.
RATE_FOREIGN      = None
RATE_FOREIGN_NAME = "BoC overnight rate"
FOREIGN_CCY       = "CA"

# Direction (DGS2, flipped) + US carry (DFF) + risk (VIXCLS) + 🛢 WTI oil leg.
OIL_SERIES  = "DCOILWTICO"
FRED_SERIES = FRED_SERIES_BASE + [OIL_SERIES]

# V1b invalidation buffer: placeholder 5 pips — calibrate from ATR after backfill.
V1B_BUFFER = 0.0005

# COT — CME Canadian dollar futures (6C). INVERTED (see _fx_usd_base).
COT_CONTRACT_NAME = "CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"
