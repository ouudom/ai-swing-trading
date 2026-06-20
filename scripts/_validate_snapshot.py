import sys, pandas as pd
sys.path.insert(0, "scripts"); import db

PARAMS = {
 "xauusd": dict(mbr=1.0, tick=100, dp=2, macro="DFII10"),
 "eurusd": dict(mbr=0.0003, tick=100000, dp=5, macro="DGS2"),
 "audusd": dict(mbr=0.0003, tick=100000, dp=5, macro="DGS2"),
 "nzdusd": dict(mbr=0.0003, tick=100000, dp=5, macro="DGS2"),
 "usdcad": dict(mbr=0.0003, tick=100000, dp=5, macro="DGS2"),
}
ZONES = {
 "xauusd": [("PRIMARY","SHORT",4360.0,4390.0),("SECONDARY","SHORT",4450.0,4485.0)],
 "eurusd": [("PRIMARY","LONG",1.15,1.152),("SECONDARY","SHORT",1.1618,1.164)],
 "audusd": [("PRIMARY","SHORT",0.7065,0.711),("COUNTER","LONG",0.698,0.700)],
 "nzdusd": [("PRIMARY","SHORT",0.5855,0.589),("COUNTER","LONG",0.575,0.579)],
 "usdcad": [("PRIMARY","LONG",1.383,1.3875)],
}

def _ohlc(inst, tf):
    df = db.read_ohlc(inst, tf); df["datetime"]=pd.to_datetime(df["datetime"])
    for c in ("open","high","low","close"): df[c]=pd.to_numeric(df[c],errors="coerce")
    return df.sort_values("datetime").reset_index(drop=True)
def _fred(sid):
    s=db.read_slice("macro_series",{"series_id":sid},["date","value"]); s["value"]=pd.to_numeric(s["value"],errors="coerce"); return s.dropna()
def _mkt(src,sym):
    s=db.read_slice("market_series",{"source":src,"symbol":sym},["date","value"]); s["value"]=pd.to_numeric(s["value"],errors="coerce"); return s.dropna()
def atr(df,p=14):
    tr=pd.concat([(df.high-df.low),(df.high-df.close.shift()).abs(),(df.low-df.close.shift()).abs()],axis=1).max(axis=1)
    return tr.rolling(p).mean()
def adx(df,p=14):
    up=df.high.diff(); dn=-df.low.diff()
    plus=((up>dn)&(up>0))*up; minus=((dn>up)&(dn>0))*dn
    tr=pd.concat([(df.high-df.low),(df.high-df.close.shift()).abs(),(df.low-df.close.shift()).abs()],axis=1).max(axis=1)
    atr_=tr.ewm(alpha=1/p,adjust=False).mean()
    pdi=100*(plus.ewm(alpha=1/p,adjust=False).mean()/atr_); mdi=100*(minus.ewm(alpha=1/p,adjust=False).mean()/atr_)
    dx=100*(pdi-mdi).abs()/(pdi+mdi); return dx.ewm(alpha=1/p,adjust=False).mean()
def drop_open(df,hrs):
    now=pd.Timestamp.now(tz="UTC").tz_localize(None); last=pd.Timestamp(df["datetime"].iloc[-1])
    return df.iloc[:-1] if now < last+pd.Timedelta(hours=hrs) else df
def e0_1h(df):
    b=drop_open(df,1).iloc[-1]; p=drop_open(df,1).iloc[-2]
    o,h,l,c=b.open,b.high,b.low,b.close; body=abs(c-o)
    upw=h-max(o,c); dnw=min(o,c)-l
    bull_eng = c>o and p.close<p.open and c>=p.open and o<=p.close
    bear_eng = c<o and p.close>p.open and c<=p.open and o>=p.close
    bull_pin = dnw>=2.5*body and body>0
    bear_pin = upw>=2.5*body and body>0
    return (bull_eng or bull_pin), (bear_eng or bear_pin), f"O{o} C{c} body{body:.5f} upw{upw:.5f} dnw{dnw:.5f} eng(bu{bull_eng}/be{bear_eng}) pin(bu{bull_pin}/be{bear_pin})"

vix=_fred("VIXCLS"); vix_now=float(vix.value.iloc[-1]); vix_spike=vix_now-float(vix.value.iloc[-2]); vix_date=str(vix.date.iloc[-1])
dxy=_mkt("yahoo","DXY"); dxy_jump=round(float(dxy.value.iloc[-1])-float(dxy.value.iloc[-2]),3)
print(f"GLOBAL: VIX {vix_now} (spike {vix_spike:+.2f}, date {vix_date}) | DXY 1d jump {dxy_jump:+.3f}")
print("="*70)
for inst in ["xauusd","eurusd","audusd","nzdusd","usdcad"]:
    P=PARAMS[inst]; dp=P["dp"]
    h4=_ohlc(inst,"4h"); d1=_ohlc(inst,"1day"); h1=_ohlc(inst,"1h")
    h4t=h4[(h4.high-h4.low)>=P["mbr"]].reset_index(drop=True)
    h4c=drop_open(h4t,4); d1c=drop_open(d1,24)
    h4_atr=round(atr(h4c).iloc[-1],dp)
    da=atr(d1c); d1_atr=round(da.iloc[-1],dp); d1_med=round(da.iloc[-20:].median(),dp); comp=d1_atr<d1_med
    spot=round(float(h4.close.iloc[-1]),dp)
    d1_adx=round(adx(d1c).iloc[-1],1)
    d1_last_close=round(float(d1c.close.iloc[-1]),dp); d1_last_dt=str(d1c.datetime.iloc[-1])
    s=_fred(P["macro"]); mnow=round(float(s.value.iloc[-1]),3); mslope=round(float(s.value.iloc[-1])-float(s.value.iloc[-20]),3)
    bull,bear,e0desc=e0_1h(h1)
    print(f"\n### {inst.upper()}  spot={spot}  D1_ATR={d1_atr} (med {d1_med}, compressed={comp})  H4_ATR={h4_atr}")
    print(f"  D1_ADX={d1_adx} {'>30 TREND' if d1_adx>30 else '<25 calm' if d1_adx<25 else 'transitional'} | macro({P['macro']})={mnow} slope20={mslope:+.3f}")
    print(f"  last CLOSED D1: {d1_last_dt} close={d1_last_close}")
    print(f"  E0 1H: bull={bull} bear={bear} | {e0desc}")
    for lab,dirn,bot,top in ZONES[inst]:
        if spot>top: dist=f"ABOVE by {round(spot-top,dp)}"
        elif spot<bot: dist=f"BELOW by {round(bot-spot,dp)}"
        else: dist="INSIDE"
        if dirn=="SHORT": v1 = "INVALID(D1 close>top)" if d1_last_close>top else "ok"
        else: v1 = "INVALID(D1 close<bot)" if d1_last_close<bot else "ok"
        need = bull if dirn=="LONG" else bear
        print(f"   [{lab} {dirn} {bot}-{top}] spot {dist} | V1 {v1} | E0-needed({'bull' if dirn=='LONG' else 'bear'})={need}")
