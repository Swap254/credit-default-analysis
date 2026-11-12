"""Step 3: rule-based customer segments and KPIs.
Reads data/processed/credit_clean.csv, writes results/segment_summary.csv and results/kpi_summary.csv.

Segment rules (checked in this order, each customer lands in exactly one segment):
  1. Severe delay    : September repayment status is 2 or more (2+ months late)
  2. Mild delay      : September repayment status is 1 (1 month late)
  3. High utilisation: not late, but September bill is above 70% of the credit limit
  4. On track        : everyone else
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "data" / "processed" / "credit_clean.csv")

# ---- Derived columns ----
df["utilisation"] = df["bill_amount_1"] / df["credit_limit"]          # September bill / limit
# A September payment pays off the AUGUST statement, so compare payment_amount_1 with bill_amount_2
paid = df["payment_amount_1"]
bill = df["bill_amount_2"]
df["payment_ratio"] = np.where(bill > 0, paid / bill, np.nan)          # only when there was a bill to pay

# ---- Rule-based segments ----
conditions = [
    df["pay_status_1"] >= 2,
    df["pay_status_1"] == 1,
    df["utilisation"] > 0.7,
]
labels = ["1. Severe delay (2+ months)", "2. Mild delay (1 month)", "3. High utilisation (>70%)"]
df["segment"] = np.select(conditions, labels, default="4. On track")

# ---- Segment summary ----
seg = (df.groupby("segment")
         .agg(customers=("customer_id", "count"),
              defaulters=("defaulted", "sum"),
              default_rate_pct=("defaulted", lambda s: round(100 * s.mean(), 2)),
              avg_credit_limit=("credit_limit", "mean"),
              avg_utilisation_pct=("utilisation", lambda s: round(100 * s.mean(), 1)))
         .reset_index())
seg["share_of_customers_pct"] = (100 * seg["customers"] / len(df)).round(1)
seg["share_of_defaulters_pct"] = (100 * seg["defaulters"] / df["defaulted"].sum()).round(1)
seg["avg_credit_limit"] = seg["avg_credit_limit"].round(0)
print(seg.to_string(index=False))
seg.to_csv(ROOT / "results" / "segment_summary.csv", index=False)

# ---- KPIs ----
top2 = seg[seg["segment"].str.startswith(("1", "2"))]
kpis = {
    "customers": len(df),
    "default_rate_pct": round(100 * df["defaulted"].mean(), 2),
    "avg_credit_limit": round(df["credit_limit"].mean(), 0),
    "avg_utilisation_pct": round(100 * df["utilisation"].mean(), 1),
    "median_payment_ratio_pct": round(100 * df["payment_ratio"].median(), 1),
    "customers_late_in_september_pct": round(100 * (df["pay_status_1"] >= 1).mean(), 1),
    "default_rate_if_late_pct": round(100 * df.loc[df["pay_status_1"] >= 1, "defaulted"].mean(), 2),
    "default_rate_if_not_late_pct": round(100 * df.loc[df["pay_status_1"] < 1, "defaulted"].mean(), 2),
    "late_customers_share_of_defaulters_pct": round(top2["share_of_defaulters_pct"].sum(), 1),
}
kpi_df = pd.DataFrame({"kpi": list(kpis), "value": list(kpis.values())})
print("\n", kpi_df.to_string(index=False))
kpi_df.to_csv(ROOT / "results" / "kpi_summary.csv", index=False)
