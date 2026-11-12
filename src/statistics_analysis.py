"""Step 7: basic statistics on the clean data: spread, outliers, correlation and a group-comparison test.
Saves results/statistics_summary.csv and two charts."""
import math
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
df = pd.read_csv(ROOT / "data" / "processed" / "credit_clean.csv")

# ---- 1. Mean, median and standard deviation ----
print("=== 1. Mean, median and standard deviation ===")
cols = ["credit_limit", "age", "bill_amount_1", "payment_amount_1"]
summary = pd.DataFrame({
    "mean": df[cols].mean(),
    "median": df[cols].median(),
    "std_dev": df[cols].std(),
}).round(0)
print(summary.to_string())
m, md = df["credit_limit"].mean(), df["credit_limit"].median()
if m > md:
    print("Note: the mean credit limit is higher than the median, so a few very large limits pull the mean up.")
else:
    print("Note: the mean and median credit limit are close, so extreme limits do not pull the mean much.")

# ---- 2. Outliers with the IQR rule ----
print("\n=== 2. Outliers in September bill (IQR rule) ===")
q1, q3 = df["bill_amount_1"].quantile([0.25, 0.75])
iqr = q3 - q1
upper = q3 + 1.5 * iqr
n_out = int((df["bill_amount_1"] > upper).sum())
print(f"Q1 = {q1:,.0f}  Q3 = {q3:,.0f}  upper limit = {upper:,.0f}")
print(f"Customers above the upper limit: {n_out:,} ({100 * n_out / len(df):.1f}%)")
print("These are real, large bills (not errors), so they are kept and the median is used when comparing.")

# ---- 3. Correlation with default (this is NOT causation) ----
print("\n=== 3. Correlation with defaulted (-1 to +1) ===")
corr_cols = ["pay_status_1", "pay_status_2", "credit_limit", "age",
             "bill_amount_1", "payment_amount_1"]
corr = df[corr_cols].corrwith(df["defaulted"]).round(3).sort_values(ascending=False)
print(corr.to_string())

# ---- 4. Is late vs not late a real difference? Two-proportion z-test ----
print("\n=== 4. Late vs not late in September: two-proportion z-test ===")
late = df[df["pay_status_1"] >= 1]["defaulted"]
ontime = df[df["pay_status_1"] <= 0]["defaulted"]
n1, n2 = len(late), len(ontime)
p1, p2 = late.mean(), ontime.mean()
pooled = (late.sum() + ontime.sum()) / (n1 + n2)
se = math.sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
z = (p1 - p2) / se
p_value = math.erfc(abs(z) / math.sqrt(2))
print(f"Late: {n1:,} customers, default rate {100 * p1:.2f}%")
print(f"Not late: {n2:,} customers, default rate {100 * p2:.2f}%")
print(f"z = {z:.1f}, p-value = {p_value:.6f}")
print("p-value below 0.05 means the gap is very unlikely to be pure chance.")
print("It does NOT prove lateness causes default.")

pd.DataFrame({
    "item": ["late_default_rate_pct", "not_late_default_rate_pct", "z_value", "p_value", "outliers_bill_sep"],
    "value": [round(100 * p1, 2), round(100 * p2, 2), round(z, 1), round(p_value, 6), n_out],
}).to_csv(RES / "statistics_summary.csv", index=False)

# ---- 5. Two charts: histogram (distribution) and box plot (outliers) ----
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(df["credit_limit"], bins=30, color="#2F6DB5")
ax.axvline(df["credit_limit"].mean(), color="#C0392B", linestyle="--", label="Mean")
ax.axvline(df["credit_limit"].median(), color="grey", linestyle="--", label="Median")
ax.set_title("Distribution of credit limit")
ax.set_xlabel("Credit limit (NT$)")
ax.set_ylabel("Number of customers")
ax.legend()
plt.tight_layout()
fig.savefig(RES / "credit_limit_histogram.png", dpi=150)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.boxplot([df["bill_amount_1"], df["payment_amount_1"]], showfliers=True)
ax.set_xticks([1, 2], ["September bill", "September payment"])
ax.set_title("Bill vs payment amounts: spread and outliers")
ax.set_ylabel("NT$")
plt.tight_layout()
fig.savefig(RES / "bill_payment_boxplot.png", dpi=150)
plt.close(fig)
print("\nSaved statistics_summary.csv, credit_limit_histogram.png, bill_payment_boxplot.png")
