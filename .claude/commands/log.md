Log a real order limit, fill, or exit to the `trade` table in `data/index.db` (via `trade_log.py`,
canonical store — no CSV) — the REAL-trade registry that feeds Entry-Confluence (R2) calibration.
Distinct from the shadow zone ledger (`zone_ledger.py`, every published zone). Link via `zone_id`.

Argument: `[action] [instrument]` where action ∈ {order, fill, close, cancel, list} (default: list).

All writes go through `scripts/trade_log.py` (never hand-edit the CSV). Run via the launcher:
`bash scripts/pyrun.sh scripts/trade_log.py <sub> ...`.

Lifecycle of one row (trade_id = `{instrument}-{week}-{setup}`):
```
order  → PENDING   order limit live, awaiting fill
fill   → OPEN      limit filled, real position on
close  → WIN_TP1 | WIN_TP2 | LOSS | BE | MANUAL | INVALIDATED
cancel → CANCELLED order expired / pulled, never filled
```

## order — record a placed order limit (PENDING)
Source the numbers from the latest `/validate` ORDER LIMIT output (entry/SL/TP1/TP2/lots) or
the `_HOT` "Live Order Limits" block. `stop_dist` and `r_planned` auto-derive if omitted.
```
bash scripts/pyrun.sh scripts/trade_log.py order \
  --instrument usdchf --week 2026-W24 --setup PRIMARY --direction LONG \
  --entry 0.79477 --sl 0.79234 --tp 0.80085 --tp2 0.80206 --lots 8.23 \
  --expiry 2026-06-12T21:00:00Z --zone-id usdchf-2026-W24-PRIMARY --notes "EC 6.5 floor, E0 1H pin"
```
`--setup` = zone label (PRIMARY/SECONDARY/COUNTER). `--zone-id` defaults to the trade_id.

## fill — limit filled → live position (PENDING → OPEN)
`--id` optional when one live row matches (filter with `--instrument`/`--setup`). `--fill-px`
overrides the limit if filled away from it (recorded in notes). `--fill-time` defaults to now UTC.
```
bash scripts/pyrun.sh scripts/trade_log.py fill --instrument usdchf [--fill-px 0.79477]
```

## close — position flat
`--status` required. Set `--r-actual` (and `--mfe`/`--mae` in R if known) so calibration counts it.
```
bash scripts/pyrun.sh scripts/trade_log.py close --id usdchf-2026-W24-PRIMARY \
  --status WIN_TP1 --exit-px 0.80085 --r-actual 2.5
```

## cancel — unfilled order pulled/expired (PENDING → CANCELLED)
```
bash scripts/pyrun.sh scripts/trade_log.py cancel --id usdchf-2026-W24-PRIMARY --reason "expired no fill"
```

## list — current rows
```
bash scripts/pyrun.sh scripts/trade_log.py list [--instrument usdchf] [--status PENDING]
```

## After any write
1. Update `_HOT.md`:
   - `order` → add/refresh the "Live Order Limits" line.
   - `fill` → move it to "Open Position"; clear from order limits.
   - `close`/`cancel` → remove from Open Position / Live Order Limits; note outcome.
2. Keep `_HOT` under the 120-line cap — outcome history lives in `forecasts/daily/*`, not `_HOT`.
3. `r_actual` on close is what `calibration.py` reads for real-trade edge stats; always set it.
