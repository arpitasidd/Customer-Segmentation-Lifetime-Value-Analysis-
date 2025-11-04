from __future__ import annotations
import argparse, sqlite3, pandas as pd
from pathlib import Path
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--datadir",type=str,default="data/raw"); ap.add_argument("--db",type=str,default="db/app.db"); a=ap.parse_args()
    Path("db").mkdir(parents=True,exist_ok=True)
    customers=pd.read_csv(Path(a.datadir)/"customers.csv"); orders=pd.read_csv(Path(a.datadir)/"orders.csv",parse_dates=["order_ts"])
    con=sqlite3.connect(a.db)
    customers.to_sql("customers",con,if_exists="replace",index=False); orders.to_sql("orders",con,if_exists="replace",index=False)
    con.execute("CREATE INDEX IF NOT EXISTS idx_orders_cust ON orders(customer_id);"); con.execute("CREATE INDEX IF NOT EXISTS idx_orders_ts ON orders(order_ts);")
    con.execute("""        CREATE VIEW IF NOT EXISTS v_customer_kpis AS
        SELECT c.customer_id, COUNT(o.rowid) AS order_count, SUM(o.amount) AS total_spend,
               AVG(o.amount) AS avg_order_value, MAX(o.order_ts) AS last_order_ts
        FROM customers c LEFT JOIN orders o USING(customer_id) GROUP BY 1;
    """); con.commit(); con.close(); print(f"Built database at {a.db}")
if __name__=="__main__": main()
