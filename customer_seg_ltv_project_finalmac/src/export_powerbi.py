from __future__ import annotations
import argparse, sqlite3, pandas as pd
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--db",type=str,default="db/app.db"); ap.add_argument("--outdir",type=str,default="data/exports"); a=ap.parse_args()
    Path(a.outdir).mkdir(parents=True,exist_ok=True); con=sqlite3.connect(a.db)
    for t in ["customers","orders","rfm","segments","clv"]:
        try:
            df=pd.read_sql_query(f"SELECT * FROM {t}",con); df.to_csv(Path(a.outdir)/f"{t}.csv",index=False); print(f"Exported {t} -> {a.outdir}/{t}.csv")
        except Exception as e:
            print(f"Skipping {t}: {e}")
    con.close()
if __name__=="__main__": main()
