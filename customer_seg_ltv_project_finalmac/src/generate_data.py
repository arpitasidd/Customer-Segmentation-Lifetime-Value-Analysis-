from __future__ import annotations
import argparse, numpy as np, pandas as pd
from pathlib import Path

SEGMENTS=[("VIP_Loyal",3.5,140.0,0.4),("Regulars",1.8,90.0,0.8),("Bargain_Hunters",1.2,60.0,1.0),("Occasional",0.5,120.0,1.4)]
def poisson_overdisp(mean,k=1.3,size=1,rng=None):
    rng=rng or np.random.default_rng(0); lam=rng.gamma(k,mean/k,size=size); return rng.poisson(lam)
def gen_customers(n_customers:int,seed:int=42):
    rng=np.random.default_rng(seed); seg_idx=rng.choice(len(SEGMENTS),size=n_customers,p=[0.15,0.45,0.25,0.15])
    ids=[f"C{str(i).zfill(6)}" for i in range(1,n_customers+1)]; ages=np.clip(rng.normal(38,10,n_customers).round().astype(int),18,80)
    regions=rng.choice(["NE","MW","S","W"],size=n_customers,p=[0.25,0.23,0.30,0.22]); seg=[SEGMENTS[i][0] for i in seg_idx]
    return pd.DataFrame({"customer_id":ids,"segment_true":seg,"age":ages,"region":regions})
def gen_orders(customers:pd.DataFrame,start:str,end:str,seed:int=42):
    rng=np.random.default_rng(seed+1); start_dt=pd.to_datetime(start); end_dt=pd.to_datetime(end); months=pd.period_range(start_dt,end_dt,freq="M")
    recs=[]; 
    for _,r in customers.iterrows():
        name,m_orders,aov,skew=next(s for s in SEGMENTS if s[0]==r.segment_true)
        monthly=poisson_overdisp(m_orders,size=len(months),rng=rng)
        for p,m in enumerate(months):
            n=monthly[p]; 
            if n<=0: continue
            days=pd.date_range(m.start_time,m.end_time,freq="D"); 
            if len(days)==0: continue
            w=np.linspace(1.0,skew,len(days)); w=w/w.sum(); chosen=rng.choice(days,size=n,replace=True,p=w)
            for d in chosen:
                amt=max(10.0,float(rng.normal(aov,aov*0.2))); ts=d+pd.Timedelta(hours=int(rng.integers(0,24)))
                recs.append((r.customer_id,ts,round(amt,2)))
    orders=pd.DataFrame(recs,columns=["customer_id","order_ts","amount"]).sort_values("order_ts"); return orders
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--n_customers",type=int,default=15000); ap.add_argument("--seed",type=int,default=42)
    ap.add_argument("--start",type=str,default="2024-01-01"); ap.add_argument("--end",type=str,default="2025-06-30"); ap.add_argument("--outdir",type=str,default="data/raw"); a=ap.parse_args()
    od=Path(a.outdir); od.mkdir(parents=True,exist_ok=True); customers=gen_customers(a.n_customers,seed=a.seed); orders=gen_orders(customers,a.start,a.end,seed=a.seed)
    customers.to_csv(od/"customers.csv",index=False); orders.to_csv(od/"orders.csv",index=False); print(f"Wrote {len(customers)} customers and {len(orders)} orders to {od}")
if __name__=="__main__": main()
