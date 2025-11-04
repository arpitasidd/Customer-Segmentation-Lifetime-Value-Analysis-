import streamlit as st, pandas as pd, sqlite3
from pathlib import Path
st.set_page_config(page_title="Customer Segmentation & CLV", layout="wide")
st.title("📊 Customer Segmentation & Lifetime Value")
db=Path("db/app.db")
if not db.exists():
    st.warning("Database not found. Please run `python -m src.cli run-all` first.")
else:
    con=sqlite3.connect(db); rfm=pd.read_sql_query("SELECT * FROM rfm",con); clv=pd.read_sql_query("SELECT * FROM clv",con); con.close()
    t1,t2=st.tabs(["RFM Segments","CLV Overview"])
    with t1:
        st.subheader("RFM Segmentation Results"); st.dataframe(rfm.head()); st.bar_chart(rfm.groupby("cluster")["Monetary"].mean())
    with t2:
        st.subheader("Customer Lifetime Value"); st.dataframe(clv.head()); st.bar_chart(clv.groupby("cluster")["CLV"].mean())
st.caption("Run: `python -m src.cli run-all` to generate data if needed.")
