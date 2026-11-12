"""Run a .sql file against data/processed/credit.db and print every result.
Usage: python src/run_sql.py sql/01_overview_and_segments.sql"""
import sqlite3
import sys
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
con = sqlite3.connect(ROOT / "data" / "processed" / "credit.db")
text = Path(sys.argv[1]).read_text()
for q in [x.strip() for x in text.split(";") if "SELECT" in x.upper() or "WITH" in x.upper()]:
    title = next((l[2:].strip() for l in q.splitlines() if l.startswith("--")), "Query")
    print(f"\n=== {title} ===")
    print(pd.read_sql_query(q, con).to_string(index=False))
