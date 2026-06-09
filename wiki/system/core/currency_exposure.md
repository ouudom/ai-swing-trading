---
type: system
updated: 2026-06-09
confidence: high
tags: [risk, fx, portfolio, netting, correlation]
related: [constitution, decisions, eurusd_profile, gbpusd_profile]
---

# Currency-Leg Netting — FX Portfolio Exposure (Architecture A)

## Why this exists
EURUSD, GBPUSD, EURGBP are **not independent**. They form a triangle:
`EURGBP = EURUSD / GBPUSD`. Three pairs, only **two degrees of freedom**. Trading two of
them at once does **not** diversify — it concentrates risk onto one underlying factor while
*looking* like two separate $2000 trades. The naive "both zones passed, take both" doubles
risk on a single bet.

**True triangular arbitrage is NOT tradeable for us** — the mispricing closes in microseconds
and lives at HFT colocation latency; by the time a retail feed shows it, crossing three spreads
makes the edge negative. This page is the opposite problem: not capturing the triangle, but
**not accidentally betting it twice.**

> We do NOT trade EURGBP. It is reference-only (price overlay for confluence). All netting below
> is pure leg algebra on EURUSD + GBPUSD positions — needs no EURGBP data.

## Leg decomposition
Every pair = a long leg + a short leg:

| Pair | Long side | = legs |
|---|---|---|
| EURUSD | buy EUR with USD | `+EUR −USD` |
| GBPUSD | buy GBP with USD | `+GBP −USD` |
| EURGBP | buy EUR with GBP | `+EUR −GBP` (reference only — never traded) |

A SHORT flips the signs.

## The four combinations — every one concentrates
Because both majors share the USD leg, **any two simultaneous EURUSD+GBPUSD orders concentrate.**
There is no "safe" pair. Only the *factor* differs:

| EURUSD | GBPUSD | Net legs | = Bet on | Factor |
|---|---|---|---|---|
| LONG  | SHORT | `+EUR −GBP` (USD cancels) | **long EURGBP cross** | CROSS |
| SHORT | LONG  | `−EUR +GBP` (USD cancels) | **short EURGBP cross** | CROSS |
| LONG  | LONG  | `+EUR +GBP −2·USD` | **short USD, doubled** | USD |
| SHORT | SHORT | `−EUR −GBP +2·USD` | **long USD, doubled** | USD |

Rule of thumb:
```
same direction      → USD stacks      → DOUBLED USD bet
opposite direction  → USD cancels     → EURGBP CROSS bet
either way          → one factor at 2× → NOT two independent trades
```

**Live example (2026-06-09):** both W24 forecasts are SHORT → `SHORT+SHORT` → **2× long USD**.
If both filled with no netting, that is a $4000 long-USD position dressed as two $2000 trades.

## Risk unit — per currency-factor, not per instrument
Replace "$2000 per instrument" with **"$2000 per currency-factor"** for FX.
```
across all open + pending FX orders:
  net_EUR, net_GBP, net_USD = Σ signed legs (each order = ±1 unit per leg)
  risk on any single currency factor ≤ $2000 (one unit)
```
Two FX orders that net to one factor = **one unit of risk**, not two.

## Netting gate — runs inside /validate (separate sequential runs)
EURUSD and GBPUSD validate in **separate invocations**, writing separate files. Shared state is
`_HOT.md`. The gate is a cross-file read at order-finalization time.

Trigger: this `/validate` run for instrument **X** has reached **✅ ORDER LIMIT**
(Entry Confluence ≥ 5.0, hard blocks passed). Before writing the order:

1. **Read `_HOT.md`** for the OTHER FX major's LIVE ORDER LIMIT or Open Position dated **today**
   (unexpired, this trading day). None → no concentration; place X normally.
2. **Decompose** both to legs; identify the factor (same dir → USD; opposite → CROSS).
   (For two USD-majors this always concentrates — confirm the factor, don't re-test independence.)
3. **Resolve — keep best, drop weaker** (operator decision D022):
   - Compare `entry_confluence_score` of X vs the recorded order Y.
   - `X > Y`  → **cancel Y's live limit** (note in `_HOT.md`: `CANCELLED [Y] — netting, superseded by [X] EC x.x>y.y`); place **X** at full $2000.
   - `X < Y`  → **X = ❌ SKIP (concentration)**; Y stays. Write X's daily file with the SKIP verdict + reason.
   - `X = Y`  → keep Y (already placed; avoid churn); X = ❌ SKIP.
4. **Emit the flag** in X's daily file regardless:
   `> [!warning] Concentration: EURUSD + GBPUSD net to <USD|EURGBP cross>. One unit risk — kept <winner> (EC x.x), skipped <loser> (EC y.y).`
5. Mirror to `_HOT.md`: which order is live, which is skipped, net factor, $2000 single-unit risk.

SKIP is a distinct verdict from NO TRADE — the zone was *tradeable* but lost the netting
tie-break. It stays PENDING; tomorrow it can win the limit if the other side weakens or closes.

## EURGBP reference overlay (optional, confluence-only)
When wired, pull EURGBP price/trend and read it as confirm/contradict on the *implied* cross:
- `EURUSD long + GBPUSD short` ⇒ implied **long EURGBP**. EURGBP rising = confirm; falling = contradict (lower conviction, flag conflict per Contradiction Protocol).
- Needs an EURGBP reference fetch (register via `_fx_base`, no zones, no orders). Not required for
  the netting gate above — netting is pure algebra. Defer until the gate is trusted.

## Scope boundaries (what A does NOT do)
- **Gold excluded.** XAUUSD is priced in USD but its driver is real yields, not a clean USD leg.
  Do not net gold into the FX factor budget. Note gold/USD co-movement as *context* only.
- **Within-instrument stacking not netted.** Two EURUSD shorts (PRIMARY+SECONDARY) literally
  double the EUR/USD bet — more concentrated than cross-pair. Current rule (constitution
  "Multi-Zone Handling") still allows each at $2000 as scale-in. Folding this into the factor
  budget is **Architecture B**, below.

---

## Architecture B — Portfolio exposure accounting (PLANNED, not built)
A is a pairwise tie-break between two majors. B is a full exposure layer.

**Goal:** one authoritative net-exposure ledger across ALL open + pending FX orders (every zone,
every instrument), enforcing a hard per-currency cap before any order is written.

**Adds over A:**
1. **Exposure ledger** — for every live/pending FX order, store signed legs + risk $. A computed
   view (script or `_HOT.md` table) sums `net_EUR / net_GBP / net_USD` continuously.
2. **Within-instrument netting** — count PRIMARY+SECONDARY same-pair same-dir as 2× one factor;
   cap or scale so total factor risk ≤ $2000 (e.g. two half-size scale-ins, not two full).
3. **EURGBP as a tradeable instrument** — its own weekly zones + validation, but orders pass
   through the same ledger so a direct EURGBP trade can't stack on an implied cross.
4. **Cross-factor budget** — optional global cap (e.g. total FX risk ≤ $4000 across ≤2 factors).
5. **Gold correlation note** — keep gold out of the FX ledger but surface a soft "all three lean
   same USD direction" advisory when XAU bias aligns with the net FX USD factor.

**Build sketch:** `scripts/fx_exposure.py` — reads `_HOT.md` live orders → emits the net-leg table
+ concentration verdict; `/validate` calls it at order-finalization instead of the manual pairwise
read. Decision gate stays "keep best, drop weaker" but generalized to N orders / N factors.

**Promote A→B when:** the pairwise gate has fired correctly in live use a few times AND there's
appetite to either (a) trade EURGBP directly or (b) run multi-zone scale-ins under one factor cap.

## Decisions trail
See `decisions.md` **D022** (this framework). Cross-links: [[constitution]] (Portfolio
Currency-Leg Netting section), [[eurusd_profile]], [[gbpusd_profile]].
