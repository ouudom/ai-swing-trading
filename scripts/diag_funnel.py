"""Phase 0 funnel diagnostic — where do weekly setups die?

Counts, per armed week, the furthest stage the setup reaches in the s_weekly_swing_v1
entry funnel. Identifies the biggest sample-killer before any redesign.

Run: .venv/bin/python -m scripts.diag_funnel
"""
import pandas as pd
from collections import Counter
from scripts.backtest.data import load, atr
from scripts.structure import structure_state, nearest_pivot_dist

STAGES = [
    "armed",            # week built a zone
    "score_ok",         # score >= 5.5 (passed G1+G2+G3)
    "reached_zone",     # price entered zone during a session bar
    "got_trigger",      # pin bar formed in zone
    "fresh_trigger",    # trigger within 8 bars (recency)
    "filled",           # price reached outward-offset limit
    "passed_R",         # R >= r_floor  → TRADE
]


def run(pivot_n, struct_win, g1_mode, r_floor, label):
    d1 = load("D1").copy()
    h4 = load("H4").copy()
    h1 = load("H1").copy()
    h4 = h4[(h4.high - h4.low) >= 1.0].copy()
    d1["atr14"] = atr(d1, 14)
    d1["atr_med20"] = d1["atr14"].rolling(20).median()
    d1["ema50"] = d1.close.ewm(span=50, adjust=False).mean()
    h4["atr14"] = atr(h4, 14)

    def g1ok(h4h, h1h, bias):
        want = "up" if bias > 0 else "down"
        s4 = structure_state(h4h, pivot_n); s1 = structure_state(h1h, pivot_n)
        if g1_mode == "h4_only": return s4 == want
        if g1_mode == "either":  return s4 == want or s1 == want
        return s4 == want and s1 == want

    # iterate weeks
    cnt = Counter()
    g1_fail = g2_state = 0
    weeks = []
    cur = None
    for ts in h1.index:
        y, w, wd = ts.isocalendar()
        if (y, w) != cur and wd == 1 and ts.hour == 0:
            cur = (y, w); weeks.append(ts)

    for arm_ts in weeks:
        dh = d1[d1.index < arm_ts]
        if len(dh) < 50: continue
        last = dh.iloc[-1]
        if pd.isna(last.atr14) or pd.isna(last.atr_med20): continue
        cnt["armed"] += 1
        bias = 1 if last.close > last.ema50 else -1
        d1_atr = last.atr14
        recent = dh.tail(5)
        if bias > 0:
            z_lo = recent.low.min(); z_hi = z_lo + 0.5 * d1_atr
        else:
            z_hi = recent.high.max(); z_lo = z_hi - 0.5 * d1_atr

        h4h = h4[h4.index < arm_ts].tail(struct_win)
        h1h = h1[h1.index < arm_ts].tail(struct_win)
        g1 = g1ok(h4h, h1h, bias)
        g2 = 2.0 if d1_atr < last.atr_med20 else 0.0
        score = (3.5 if g1 else 0.0) + g2 + 3.5
        if not g1: g1_fail += 1
        if score < 5.5:
            continue
        cnt["score_ok"] += 1

        # scan the week's H1 bars
        end_ts = arm_ts + pd.Timedelta(days=4, hours=17)
        wk = h1[(h1.index >= arm_ts) & (h1.index <= end_ts)]
        h4_hist_all = h4[h4.index < arm_ts]
        h4_atr_now = h4_hist_all.iloc[-1].atr14 if len(h4_hist_all) else d1_atr * 0.4
        ref_px = z_lo if bias > 0 else z_hi
        struct = nearest_pivot_dist(h4_hist_all, ref_px, bias, n=pivot_n)
        if struct is None or struct <= 0:
            stop = (0.5 * d1_atr + h4_atr_now) / 2.0; struct = 0.0
        else:
            stop = (0.5 * d1_atr + h4_atr_now + struct) / 3.0
        if struct > 3 * h4_atr_now or stop <= 0:
            continue  # capped — dies before zone scan effectively
        offset = (10 - score) * 0.3 * stop
        limit_px = (z_lo - offset) if bias > 0 else (z_hi + offset)
        tp_px = recent.high.max() if bias > 0 else recent.low.min()
        R = abs(tp_px - limit_px) / stop if stop else 0

        reached = trig = fresh = filled = False
        trig_idx = -999
        for j, (ts2, r2) in enumerate(wk.iterrows()):
            if ts2.hour < 8 or ts2.hour >= 17: continue
            if (r2.low <= z_hi) and (r2.high >= z_lo):
                reached = True
                body = abs(r2.close - r2.open)
                uw = r2.high - max(r2.close, r2.open); lw = min(r2.close, r2.open) - r2.low
                pin = (lw >= 2 * body and r2.close > r2.open and bias > 0) or \
                      (uw >= 2 * body and r2.close < r2.open and bias < 0)
                if pin: trig = True; trig_idx = j
                if trig and (j - trig_idx) <= 8 and trig_idx >= 0:
                    fresh = True
                    if r2.low <= limit_px <= r2.high:
                        filled = True
                        break
        if reached: cnt["reached_zone"] += 1
        if trig: cnt["got_trigger"] += 1
        if fresh: cnt["fresh_trigger"] += 1
        if filled: cnt["filled"] += 1
        if filled and R >= r_floor: cnt["passed_R"] += 1

    print(f"\n=== {label} (pivot_n={pivot_n}, win={struct_win}, mode={g1_mode}, rflr={r_floor}) ===")
    prev = None
    for s in STAGES:
        v = cnt[s]
        drop = f"  (−{prev - v})" if prev is not None else ""
        print(f"  {s:<14} {v:>5}{drop}")
        prev = v
    print(f"  [G1 fails: {g1_fail} of {cnt['armed']} armed weeks]")


if __name__ == "__main__":
    run(2, 60, "both", 1.8, "LIVE config")
    run(2, 60, "either", 1.8, "Best-PnL config")
    run(3, 60, "either", 1.8, "Most-trades config")
