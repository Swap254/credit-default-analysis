"""Step 2: turn the clean file into a small SQLite star schema (data/processed/credit.db)."""
import sqlite3
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "data" / "processed" / "credit_clean.csv")
DB = ROOT / "data" / "processed" / "credit.db"
if DB.exists():
    DB.unlink()
con = sqlite3.connect(DB)

# Dimension table: one row per customer
customers = df[["customer_id", "credit_limit", "sex_code", "education_code",
                "marriage_code", "age", "defaulted"]]
customers.to_sql("customers", con, index=False)

# Fact table: one row per customer per month (6 rows per customer)
MONTHS = {1: "Sep", 2: "Aug", 3: "Jul", 4: "Jun", 5: "May", 6: "Apr"}
parts = []
for m in range(1, 7):
    part = df[["customer_id"]].copy()
    part["month_no"] = m
    part["month_name"] = MONTHS[m]
    part["pay_status"] = df[f"pay_status_{m}"]
    part["bill_amount"] = df[f"bill_amount_{m}"]
    part["payment_amount"] = df[f"payment_amount_{m}"]
    parts.append(part)
pd.concat(parts).to_sql("monthly_statements", con, index=False)

# Lookup tables: code -> label
pd.DataFrame({"sex_code": [1, 2], "sex": ["Male", "Female"]}).to_sql("sex_codes", con, index=False)
pd.DataFrame({"education_code": [1, 2, 3, 4],
              "education": ["Graduate school", "University", "High school", "Others"]}
             ).to_sql("education_codes", con, index=False)
pd.DataFrame({"marriage_code": [1, 2, 3], "marriage": ["Married", "Single", "Others"]}
             ).to_sql("marriage_codes", con, index=False)
pay = {-2: "No credit use", -1: "Paid in full", 0: "Paid minimum (revolving)"}
pay.update({i: f"Delayed {i} month(s)" for i in range(1, 10)})
pd.DataFrame({"pay_status": list(pay), "pay_label": list(pay.values())}
             ).to_sql("pay_status_codes", con, index=False)

con.execute("CREATE INDEX idx_ms_customer ON monthly_statements(customer_id)")
con.commit()
for t in ["customers", "monthly_statements", "sex_codes", "education_codes",
          "marriage_codes", "pay_status_codes"]:
    print(t, con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0], "rows")
con.close()
