import sys, pandas as pd, numpy as np
sys.path.insert(0,"scripts"); import db
def _o(tf):
    d=db.read_ohlc("nzdusd",tf); d["datetime"]=pd.to_datetime(d["datetime"])
    for c in("open","high","low","close"): d[c]=pd.to_numeric(d[c],errors="coerce")
    return d.sort_values("datetime").reset_index(drop=True)
def stoch(df,k=14,d=3):
    ll=df.low.rolling(k).min(); hh=df.high.rolling(k).max()
    kk=100*(df.close-ll)/(hh-ll); return kk.iloc[-1], kk.rolling(d).mean().iloc[-1]
def wpr(df,p=14):
    hh=df.high.rolling(p).max(); ll=df.low.rolling(p).min()
    return (-100*(hh-df.close)/(hh-ll)).iloc[-1]
def cci(df,p=20):
    tp=(df.high+df.low+df.close)/3; ma=tp.rolling(p).mean(); md=(tp-ma).abs().rolling(p).mean()
    return ((tp-ma)/(0.015*md)).iloc[-1]
def rsi(df,p=14):
    dl=df.close.diff(); up=dl.clip(lower=0).ewm(alpha=1/p,adjust=False).mean(); dn=(-dl.clip(upper=0)).ewm(alpha=1/p,adjust=False).mean()
    return (100-100/(1+up/dn)).iloc[-1]
def keltner(df,p=20,m=1.5):
    ma=df.close.ewm(span=p,adjust=False).mean()
    tr=pd.concat([(df.high-df.low),(df.high-df.close.shift()).abs(),(df.low-df.close.shift()).abs()],axis=1).max(axis=1)
    atr=tr.rolling(p).mean(); return ma.iloc[-1]-m*atr.iloc[-1], ma.iloc[-1], ma.iloc[-1]+m*atr.iloc[-1]
def donchian(df,p=20):
    return df.low.rolling(p).min().iloc[-1], df.high.rolling(p).max().iloc[-1]
def adx(df,p=14):
    up=df.high.diff(); dn=-df.low.diff(); plus=((up>dn)&(up>0))*up; minus=((dn>up)&(dn>0))*dn
    tr=pd.concat([(df.high-df.low),(df.high-df.close.shift()).abs(),(df.low-df.close.shift()).abs()],axis=1).max(axis=1)
    a=tr.ewm(alpha=1/p,adjust=False).mean(); pdi=100*(plus.ewm(alpha=1/p,adjust=False).mean()/a); mdi=100*(minus.ewm(alpha=1/p,adjust=False).mean()/a)
    dx=100*(pdi-mdi).abs()/(pdi+mdi); return dx.ewm(alpha=1/p,adjust=False).mean().iloc[-1], pdi.iloc[-1], mdi.iloc[-1]
def drop_open(df,hrs):
    now=pd.Timestamp.now(tz="UTC").tz_localize(None); last=pd.Timestamp(df["datetime"].iloc[-1])
    return df.iloc[:-1] if now<last+pd.Timedelta(hours=hrs) else df
h4=drop_open(_o("4h"),4); h1=drop_open(_o("1h"),1); d1=drop_open(_o("1day"),24)
print("ZONE COUNTER LONG 0.575-0.579 | spot(last h1 close)", round(h1.close.iloc[-1],5))
sk,sd=stoch(h4); kl,km,ku=keltner(h4); dl,dh=donchian(h4); ax,pd_,md_=adx(h4)
print(f"H4: Stoch%K {sk:.1f}/%D {sd:.1f} | W%R {wpr(h4):.1f} | CCI {cci(h4):.1f} | RSI {rsi(h4):.1f}")
print(f"H4 Keltner l{kl:.5f}/m{km:.5f}/u{ku:.5f} | Donchian l{dl:.5f}/h{dh:.5f} | ADX {ax:.1f} (+DI{pd_:.1f}/-DI{md_:.1f})")
sk1,sd1=stoch(h1)
print(f"H1: Stoch%K {sk1:.1f}/%D {sd1:.1f} | W%R {wpr(h1):.1f} | CCI {cci(h1):.1f} | RSI {rsi(h1):.1f}")
print("\nLast 6 closed H1 bars (O/H/L/C):")
for _,r in h1.tail(6).iterrows():
    body=r.close-r.open; print(f"  {r.datetime} O{r.open:.5f} H{r.high:.5f} L{r.low:.5f} C{r.close:.5f} {'UP' if body>0 else 'DN' if body<0 else 'doji'} body{body:+.5f}")
print("\nLast 4 closed H4 bars:")
for _,r in h4.tail(4).iterrows():
    print(f"  {r.datetime} O{r.open:.5f} H{r.high:.5f} L{r.low:.5f} C{r.close:.5f}")
