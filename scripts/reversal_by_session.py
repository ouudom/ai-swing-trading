"""Count trend reversals (swing pivots) by UTC hour on H1 XAUUSD."""
import pandas as pd

df = pd.read_csv("data/twelvedata/xauusd/1h.csv", parse_dates=["datetime"])
df = df.sort_values("datetime").reset_index(drop=True)
df["hour"] = df["datetime"].dt.hour

# Pivot definition: local high/low within k-bar window each side
K = 3
hi = df["high"]
lo = df["low"]
is_pivot_high = pd.Series(False, index=df.index)
is_pivot_low = pd.Series(False, index=df.index)
for i in range(K, len(df) - K):
    h_win = hi.iloc[i-K:i+K+1]
    l_win = lo.iloc[i-K:i+K+1]
    if hi.iloc[i] == h_win.max() and (h_win == hi.iloc[i]).sum() == 1:
        is_pivot_high.iloc[i] = True
    if lo.iloc[i] == l_win.min() and (l_win == lo.iloc[i]).sum() == 1:
        is_pivot_low.iloc[i] = True

df["pivot"] = is_pivot_high | is_pivot_low

def session(h):
    if 0 <= h < 8: return "Asia (00-07)"
    if 8 <= h < 13: return "London (08-12)"
    if 13 <= h < 17: return "LDN/NY overlap (13-16)"
    if 17 <= h < 21: return "NY late (17-20)"
    return "Late (21-23)"

df["session"] = df["hour"].apply(session)

bars_per_hr = df.groupby("hour").size()
pivots_per_hr = df.groupby("hour")["pivot"].sum()
rate_per_hr = (pivots_per_hr / bars_per_hr * 100).round(2)

print("=== Pivots per UTC hour (H1, k=3) ===")
print(pd.DataFrame({"bars": bars_per_hr, "pivots": pivots_per_hr, "rate_%": rate_per_hr}))

print("\n=== Pivots per session ===")
sess = df.groupby("session").agg(bars=("pivot", "size"), pivots=("pivot", "sum"))
sess["rate_%"] = (sess["pivots"] / sess["bars"] * 100).round(2)
sess = sess.sort_values("rate_%", ascending=False)
print(sess)
