#!/usr/bin/env bash
set -e
python3 --version
if [ ! -d ".venv" ]; then python3 -m venv .venv; fi
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m src.cli run-all
PORT=8501
python -m streamlit run app/streamlit_app.py --server.headless=false --server.port=${PORT} &
sleep 2
open "http://localhost:${PORT}" || true
