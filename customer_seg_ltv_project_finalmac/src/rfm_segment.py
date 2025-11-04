from __future__ import annotations
import argparse, sqlite3, numpy as np, pandas as pd
from pathlib import Path
def compute_rfm(db_path: str, as_of: str | None = None):
    con=sqlite3.connect(db_path)
    orders=pd.read_sql_query("SELECT customer_id, order_ts, amount FROM orders",con,parse_dates=["order_ts"]); con.close()
    if orders.empty: raise SystemExit("No orders found. Generate data and build DB first.")
    as_of_ts=pd.to_datetime(as_of) if as_of is not None else orders["order_ts"].max().normalize()+pd.Timedelta(days=1)
    g=orders.groupby("customer_id")
    last_order=g["order_ts"].max()
    recency=(as_of_ts-last_order).dt.days.rename("Recency")
    frequency=g.size().rename("Frequency")
    monetary=g["amount"].sum().rename("Monetary")
    rfm=pd.concat([recency,frequency,monetary],axis=1).reset_index()
    return rfm, as_of_ts
def _standardize(arr: np.ndarray):
    mu=np.nanmean(arr,axis=0); sd=np.nanstd(arr,axis=0); sd[sd==0]=1.0; return (arr-mu)/sd, mu, sd
def _init_centroids(X: np.ndarray, k:int, seed:int=42):
    rng=np.random.default_rng(seed); idx=rng.choice(X.shape[0],size=k,replace=False); return X[idx].copy()
def _closest_centroids(X: np.ndarray, C: np.ndarray):
    d=np.sqrt(((X[:,None,:]-C[None,:,:])**2).sum(axis=2)); return np.argmin(d,axis=1)
def _recompute_centroids(X: np.ndarray, labels: np.ndarray, k:int):
    cents=[]; 
    for j in range(k):
        sel=X[labels==j]; cents.append(sel.mean(axis=0) if len(sel)>0 else X[np.random.randint(0,len(X))])
    return np.vstack(cents)
def kmeans_cluster(rfm: pd.DataFrame, k:int=4, random_state:int=42):
    feats=rfm[["Recency","Frequency","Monetary"]].copy(); feats["Recency"]=feats["Recency"].fillna(feats["Recency"].max()); feats=feats.fillna(0.0)
    X,mu,sd=_standardize(feats.values.astype(float)); np.random.seed(random_state); C=_init_centroids(X,k,seed=random_state)
    for _ in range(50):
        labels=_closest_centroids(X,C); C_new=_recompute_centroids(X,labels,k)
        if np.allclose(C_new,C): break
        C=C_new
    rfm["cluster"]=labels; return rfm, C, (mu,sd)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--db",type=str,default="db/app.db"); ap.add_argument("--k",type=int,default=4)
    ap.add_argument("--as_of",type=str,default=None); ap.add_argument("--out",type=str,default="data/processed/rfm_segments.csv"); a=ap.parse_args()
    Path("data/processed").mkdir(parents=True,exist_ok=True); rfm, as_of = compute_rfm(a.db, a.as_of)
    rfm_lbl, centers, scaler = kmeans_cluster(rfm, k=a.k); rfm_lbl.to_csv(a.out,index=False)
    con=sqlite3.connect(a.db); rfm_lbl.to_sql("rfm",con,if_exists="replace",index=False)
    con.execute("CREATE INDEX IF NOT EXISTS idx_rfm_customer ON rfm(customer_id);")
    summary=rfm_lbl.groupby("cluster",as_index=False).agg(n=("customer_id","count"),Recency_mean=("Recency","mean"),Frequency_mean=("Frequency","mean"),Monetary_mean=("Monetary","mean"))
    summary.to_sql("segments",con,if_exists="replace",index=False); con.close()
    print(f"RFM+KMeans done (k={a.k}). As of {as_of.date()}. Saved to {a.out}")
if __name__=="__main__": main()
