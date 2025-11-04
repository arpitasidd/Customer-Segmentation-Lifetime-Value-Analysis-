from __future__ import annotations
import argparse, sqlite3, numpy as np, pandas as pd
from pathlib import Path
def sigmoid(x): return 1/(1+np.exp(-x))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--db",type=str,default="db/app.db")
    ap.add_argument("--margin",type=float,default=0.60); ap.add_argument("--discount_rate",type=float,default=0.01); ap.add_argument("--out",type=str,default="data/processed/clv.csv"); a=ap.parse_args()
    con=sqlite3.connect(a.db)
    orders=pd.read_sql_query("SELECT customer_id, order_ts, amount FROM orders ORDER BY order_ts",con,parse_dates=["order_ts"])
    rfm=pd.read_sql_query("SELECT * FROM rfm",con); con.close()
    def _cust_stats(df):
        df=df.sort_values("order_ts")
        if len(df)<2:
            inter=np.nan; freq_m=len(df)/max(((df["order_ts"].max()-df["order_ts"].min()).days/30.0),1/30)
        else:
            inters=df["order_ts"].diff().dropna().dt.days.values; inter=float(np.nanmean(inters)) if len(inters)>0 else np.nan
            span=max(((df["order_ts"].max()-df["order_ts"].min()).days/30.0),1/30); freq_m=len(df)/span
        aov=df["amount"].mean(); return pd.Series({"avg_interpurchase_days":inter,"purchases_per_month":freq_m,"avg_order_value":aov})
    kpis=orders.groupby("customer_id").apply(_cust_stats).reset_index()
    as_of=orders["order_ts"].max().normalize()+pd.Timedelta(days=1)
    m=rfm.merge(kpis,on="customer_id",how="left")
    m["avg_interpurchase_days"]=m["avg_interpurchase_days"].fillna(60.0); m["purchases_per_month"]=m["purchases_per_month"].fillna(0.05); m["avg_order_value"]=m["avg_order_value"].fillna(50.0)
    x=(m["Recency"]-m["avg_interpurchase_days"])/(m["avg_interpurchase_days"]+1e-6); m["churn_prob"]=sigmoid(x)
    hazard=np.clip(m["churn_prob"],0.01,0.99); m["lifetime_months"]=np.clip(1.0/(hazard+1e-6),1,48)
    r=a.discount_rate; cf=m["avg_order_value"]*m["purchases_per_month"]*a.margin; m["CLV"]=cf*((1-(1+r)**(-m["lifetime_months"]))/r)
    out=m[["customer_id","Recency","Frequency","Monetary","cluster","purchases_per_month","avg_order_value","avg_interpurchase_days","churn_prob","lifetime_months","CLV"]]
    Path("data/processed").mkdir(parents=True,exist_ok=True); out.to_csv(a.out,index=False)
    con=sqlite3.connect(a.db); out.to_sql("clv",con,if_exists="replace",index=False); con.close()
    print(f"Computed churn & CLV as of {as_of.date()}. Saved to {a.out}")
if __name__=="__main__": main()
