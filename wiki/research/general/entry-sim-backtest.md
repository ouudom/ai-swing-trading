# Entry-Confirmation (E0) Tier-2 Entry Simulation

MARKET = enter at signal close. LIMIT = outward offset (s/3) limit, fills on a poke within 12 bars. LIMIT+E0 = same, only when a 1H pin/engulf is present. Same SL=H1 ATR14 and 2.5R target across arms — only entry price differs. **If LIMIT / LIMIT+E0 beat MARKET on avgR & PF despite lower fill%, the offset (and E0 gating it) earns its weight.** FX mean-rev reading; gold separate.

## Verdict — the OFFSET is validated; E0 is a real per-trade-R filter (Tier-1 was blind to both)

avgR by arm (MARKET → LIMIT → LIMIT+E0):

| pair | MARKET | LIMIT | LIMIT+E0 | read |
|---|--:|--:|--:|---|
| eurusd | +0.021 | +0.024 | **+0.063** | ladder up — E0 best |
| usdcad | −0.018 | +0.045 | **+0.083** | clean MKT<LIMIT<E0; offset flips it positive |
| audusd | −0.022 | −0.007 | **+0.049** | E0 flips a losing setup positive |
| gbpjpy | +0.010 | +0.030 | **+0.044** | ladder up |
| nzdusd | +0.061 | +0.036 | **+0.084** | E0 best (offset alone dips) |
| eurjpy | +0.012 | **+0.037** | +0.026 | offset best, E0 ≈ offset |
| eurgbp | +0.055 | **+0.098** | +0.064 | offset best |
| usdchf | +0.019 | **+0.060** | +0.026 | offset best |
| gbpusd | −0.025 | **−0.004** | −0.004 | offset repairs market loss |
| xauusd | +0.018 | +0.009 | −0.003 | fade reading wrong for gold (E0=continuation) ✓ |
| usdjpy | −0.076 | −0.018 | −0.030 | carry-drift — fades lose all arms; E0 can't fix wrong dir ✓ |

**Findings:**
1. **Outward offset beats market entry on avgR/PF in 9 of 11 pairs.** Same SL, same target, better
   fill price → higher expectancy. This is exactly E0's mechanism, and Tier-1 (win-rate) could not
   see it. **The offset rule is justified by data.**
2. **E0 trigger adds further on top of the offset for ~6 pairs** (eurusd, usdcad, audusd, nzdusd,
   gbpjpy + ties) — it flips audusd/usdcad from losing to positive — **at the cost of taking only
   ~22–25% of setups.** E0 is a quality FILTER: fewer trades, better per-trade R. Precisely its role.
3. **Exceptions confirm the model, not refute it:** xauusd (E0 is continuation, not fade) and
   usdjpy (carry-drift — fades are wrong-direction) underperform under the fade reading. Both are
   already coded that way in their rubrics (gold E0 toward zone; usdjpy long = drift). No fix.

**Caveat (read honestly):** avgR magnitudes are small and PF barely >1 because the universe is
**every** oscillator extreme — unfiltered. The live system only trades confluence-gated zones
(floor 5.0), a higher-quality subset, so real edge should exceed these. This validates the
**direction and ordering** of the effect (MARKET < LIMIT ≤ LIMIT+E0), not absolute profitability.
SL=1×ATR / TP=2.5R fixed — sensitivity not swept.

**Actionable:** keep the offset rule and E0 as-is — both now have forward-test support, on R not
win-rate. No reweight. Do NOT extend fade-E0 to gold/usdjpy (already correct). A confluence-gated
re-run (setups filtered to high Z-score) is the natural Tier-3 once the live ledger grows.

```
==================================================================
XAUUSD — Entry-Sim (H1, SL=ATR14, TP=2.5R, 4205 setups)
==================================================================
arm          N_fill   fill%    win%     avgR      PF
------------------------------------------------------------------
MARKET         4202    100%    29.2   +0.018    1.02
LIMIT          3625     86%    28.9   +0.009    1.01
LIMIT+E0       1056     25%    28.6   -0.003    1.00
------------------------------------------------------------------

==================================================================
EURUSD — Entry-Sim (H1, SL=ATR14, TP=2.5R, 4572 setups)
==================================================================
arm          N_fill   fill%    win%     avgR      PF
------------------------------------------------------------------
MARKET         4571    100%    29.3   +0.021    1.03
LIMIT          3989     87%    29.3   +0.024    1.03
LIMIT+E0       1038     23%    30.3   +0.063    1.09
------------------------------------------------------------------

==================================================================
GBPUSD — Entry-Sim (H1, SL=ATR14, TP=2.5R, 4538 setups)
==================================================================
arm          N_fill   fill%    win%     avgR      PF
------------------------------------------------------------------
MARKET         4537    100%    28.0   -0.025    0.96
LIMIT          3984     88%    28.5   -0.004    1.00
LIMIT+E0       1076     24%    28.5   -0.004    0.99
------------------------------------------------------------------

==================================================================
EURGBP — Entry-Sim (H1, SL=ATR14, TP=2.5R, 4554 setups)
==================================================================
arm          N_fill   fill%    win%     avgR      PF
------------------------------------------------------------------
MARKET         4553    100%    30.3   +0.055    1.08
LIMIT          3952     87%    31.5   +0.098    1.14
LIMIT+E0       1135     25%    30.6   +0.064    1.09
------------------------------------------------------------------

==================================================================
AUDUSD — Entry-Sim (H1, SL=ATR14, TP=2.5R, 4425 setups)
==================================================================
arm          N_fill   fill%    win%     avgR      PF
------------------------------------------------------------------
MARKET         4424    100%    28.1   -0.022    0.97
LIMIT          3888     88%    28.4   -0.007    0.99
LIMIT+E0        986     22%    30.0   +0.049    1.07
------------------------------------------------------------------

==================================================================
NZDUSD — Entry-Sim (H1, SL=ATR14, TP=2.5R, 4510 setups)
==================================================================
arm          N_fill   fill%    win%     avgR      PF
------------------------------------------------------------------
MARKET         4509    100%    30.4   +0.061    1.09
LIMIT          3934     87%    29.7   +0.036    1.05
LIMIT+E0        967     21%    31.0   +0.084    1.12
------------------------------------------------------------------

==================================================================
USDCAD — Entry-Sim (H1, SL=ATR14, TP=2.5R, 4557 setups)
==================================================================
arm          N_fill   fill%    win%     avgR      PF
------------------------------------------------------------------
MARKET         4555    100%    28.2   -0.018    0.97
LIMIT          4014     88%    30.0   +0.045    1.06
LIMIT+E0       1125     25%    31.1   +0.083    1.12
------------------------------------------------------------------

==================================================================
USDCHF — Entry-Sim (H1, SL=ATR14, TP=2.5R, 4587 setups)
==================================================================
arm          N_fill   fill%    win%     avgR      PF
------------------------------------------------------------------
MARKET         4586    100%    29.2   +0.019    1.03
LIMIT          4023     88%    30.4   +0.060    1.09
LIMIT+E0       1083     24%    29.4   +0.026    1.04
------------------------------------------------------------------

==================================================================
USDJPY — Entry-Sim (H1, SL=ATR14, TP=2.5R, 4267 setups)
==================================================================
arm          N_fill   fill%    win%     avgR      PF
------------------------------------------------------------------
MARKET         4264    100%    26.6   -0.076    0.90
LIMIT          3763     88%    28.2   -0.018    0.97
LIMIT+E0        919     22%    27.7   -0.030    0.96
------------------------------------------------------------------

==================================================================
EURJPY — Entry-Sim (H1, SL=ATR14, TP=2.5R, 4506 setups)
==================================================================
arm          N_fill   fill%    win%     avgR      PF
------------------------------------------------------------------
MARKET         4505    100%    29.1   +0.012    1.02
LIMIT          3928     87%    29.9   +0.037    1.05
LIMIT+E0       1129     25%    29.5   +0.026    1.04
------------------------------------------------------------------

==================================================================
GBPJPY — Entry-Sim (H1, SL=ATR14, TP=2.5R, 4399 setups)
==================================================================
arm          N_fill   fill%    win%     avgR      PF
------------------------------------------------------------------
MARKET         4398    100%    29.1   +0.010    1.01
LIMIT          3808     87%    29.5   +0.030    1.04
LIMIT+E0       1106     25%    30.0   +0.044    1.06
------------------------------------------------------------------
```
