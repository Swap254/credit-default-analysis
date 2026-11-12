"""Step 8: export tables from credit.db for the Excel workbook and for Power BI.
Creates data/processed/bi_export/ with:
  - credit_excel_practice.xlsx  (sheet Data = one row per customer, sheet Lookup = education codes)
  - customers.csv, monthly_statements.csv, education_codes.csv, sex_codes.csv,
    marriage_codes.csv, pay_status_codes.csv   (the star schema for Power BI)"""
import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "processed" / "bi_export"
OUT.mkdir(parents=True, exist_ok=True)
con = sqlite3.connect(ROOT / "data" / "processed" / "credit.db")

# ---- Power BI: one CSV per table ----
for table in ["customers", "monthly_statements", "education_codes",
              "sex_codes", "marriage_codes", "pay_status_codes"]:
    df = pd.read_sql_query(f"SELECT * FROM {table}", con)
    df.to_csv(OUT / f"{table}.csv", index=False)
    print(f"{table}.csv  {len(df):,} rows")

# ---- Excel: a flat Data sheet (September view) and a Lookup sheet ----
data = pd.read_sql_query("""
    SELECT c.customer_id, c.credit_limit, c.education_code, c.age,
           s.pay_status AS sept_pay_status,
           s.bill_amount AS sept_bill,
           s.payment_amount AS sept_payment,
           c.defaulted
    FROM customers c
    JOIN monthly_statements s ON s.customer_id = c.customer_id AND s.month_no = 1
    ORDER BY c.customer_id
""", con)
lookup = pd.read_sql_query("SELECT education_code, education FROM education_codes", con)
with pd.ExcelWriter(OUT / "credit_excel_practice.xlsx") as writer:
    data.to_excel(writer, sheet_name="Data", index=False)
    lookup.to_excel(writer, sheet_name="Lookup", index=False)
print(f"credit_excel_practice.xlsx  Data {len(data):,} rows, Lookup {len(lookup)} rows")
print("Saved in", OUT)
