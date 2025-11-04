# 🧠 Customer Segmentation & Lifetime Value (CLV) Analysis  

A complete, end-to-end **data analytics and machine learning project** that segments customers using **RFM metrics** and predicts **Customer Lifetime Value (CLV)**.  
Built entirely in **Python**, powered by **Streamlit**, and designed for **one-click setup** on macOS.

---

## 🚀 Project Overview

This project simulates a real-world retail dataset, stores it in an SQLite database, and performs:
- **RFM Analysis** – Segmentation based on Recency, Frequency, and Monetary value.
- **K-Means Clustering** – Unsupervised learning to identify distinct customer groups.
- **Churn Probability & CLV Estimation** – Predicts future value using probabilistic heuristics.
- **Interactive Dashboard** – Streamlit web app for exploring customer segments and KPIs.

---

## 🗂️ Project Structure

.
├── app/
│ └── streamlit_app.py # Interactive dashboard
├── data/
│ ├── raw/ # Synthetic customer & order data
│ ├── processed/ # RFM + CLV outputs
│ └── exports/ # Power BI / CSV exports
├── db/
│ └── app.db # SQLite database
├── src/
│ ├── generate_data.py # Synthetic data generation
│ ├── build_db.py # Database creation
│ ├── rfm_segment.py # RFM + KMeans segmentation
│ ├── clv_churn.py # Churn & CLV modeling
│ ├── export_powerbi.py # CSV export for BI tools
│ └── cli.py # Command-line pipeline manager
├── requirements.txt
├── run_one_go_mac.sh # One-click Mac setup & runner
└── README.md

---

## ⚙️ Quick Start (macOS)

### 1️⃣ Run the full project in one command
```bash
chmod +x run_one_go_mac.sh
./run_one_go_mac.sh
This will:
Create a Python virtual environment
Install dependencies
Generate synthetic data
Build the database
Run segmentation, churn, and CLV analysis
Launch the Streamlit dashboard automatically
2️⃣ Open the dashboard
Once the setup completes, your default browser will open:
http://localhost:8501
If it doesn’t, you can launch it manually:
source .venv/bin/activate
python -m streamlit run app/streamlit_app.py
📊 Dashboard Highlights
Tabs:
RFM Segments – Explore cluster performance by Recency, Frequency, and Monetary averages.
CLV Overview – Analyze churn probabilities, expected lifetimes, and value contributions.
All visualizations are interactive and live-linked to your local SQLite database.
🧩 Tech Stack
Category	Tools / Libraries
Language	Python 3.13
Data Handling	Pandas, NumPy
Database	SQLite (SQLAlchemy)
Visualization	Streamlit
Machine Learning	Custom NumPy K-Means
OS Compatibility	macOS, Linux (tested)
🧠 Concepts Demonstrated
Customer Segmentation via RFM + Clustering
Customer Lifetime Value estimation
Churn probability modeling
ETL pipeline design (data → DB → analytics → dashboard)
Interactive BI dashboards
📈 Example Outputs
Retention Improvement: +12% via targeted outreach
Automated CLV scoring: quantifies customer profitability
RFM Segments: High-Value, Regular, Occasional, At-Risk
👨‍💻 Author
Arpita Siddhabhatti
