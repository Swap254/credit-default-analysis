"""Step 1: load the raw UCI file, check quality, clean it, and save data/processed/credit_clean.csv."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed" / "credit_clean.csv"


def load_raw():
    """Find the UCI file in data/raw/ whatever it is called (.xls, .xlsx or .csv).
    The UCI Excel file has an 'X1..X23' row first, so real headers are on row 2.
    The Kaggle CSV has real headers on row 1. We try row 1 first, then row 2."""
    files = [f for f in RAW.iterdir() if f.suffix.lower() in (".xls", ".xlsx", ".csv")]
    if not files:
        raise FileNotFoundError("No .xls/.xlsx/.csv file found in data/raw/ (see data_dictionary.md)")
    path = files[0]
    print(f"Loading {path.name}")
    reader = pd.read_csv if path.suffix.lower() == ".csv" else pd.read_excel
    df = reader(path)
    if "ID" not in df.columns:
        df = reader(path, header=1)
    return df


df = load_raw()
print("Shape:", df.shape)

# ---- 1. Quality checks ----
print("\nMissing values in total:", int(df.isnull().sum().sum()))
print("Duplicate IDs:", int(df["ID"].duplicated().sum()))
dups = int(df.drop(columns="ID").duplicated().sum())
print("Rows identical except for ID:", dups, "(kept, flagged)")

# ---- 2. Rename columns to clear snake_case names ----
df = df.rename(columns={
    "ID": "customer_id", "LIMIT_BAL": "credit_limit", "SEX": "sex_code",
    "EDUCATION": "education_code", "MARRIAGE": "marriage_code", "AGE": "age",
    "PAY_0": "pay_status_1",   # PAY_0 is September: renamed so that month numbers run 1..6
    "PAY_2": "pay_status_2", "PAY_3": "pay_status_3", "PAY_4": "pay_status_4",
    "PAY_5": "pay_status_5", "PAY_6": "pay_status_6",
    **{f"BILL_AMT{i}": f"bill_amount_{i}" for i in range(1, 7)},
    **{f"PAY_AMT{i}": f"payment_amount_{i}" for i in range(1, 7)},
    "default payment next month": "defaulted",
    "default.payment.next.month": "defaulted",   # name used in the Kaggle CSV
})

# ---- 3. Fix undocumented category codes ----
bad_edu = int(df["education_code"].isin([0, 5, 6]).sum())
bad_mar = int((df["marriage_code"] == 0).sum())
df["education_code"] = df["education_code"].replace({0: 4, 5: 4, 6: 4})
df["marriage_code"] = df["marriage_code"].replace({0: 3})
print(f"\nEducation codes 0/5/6 merged into 'Others': {bad_edu} rows")
print(f"Marriage code 0 merged into 'Others': {bad_mar} rows")

# ---- 4. Negative bills are valid (overpayment), so they are only reported ----
neg = int((df[[f"bill_amount_{i}" for i in range(1, 7)]] < 0).any(axis=1).sum())
print(f"Customers with at least one negative bill (kept): {neg}")

df.to_csv(OUT, index=False)
print(f"\nSaved {len(df)} rows to {OUT.relative_to(ROOT)}")
print("Default rate:", round(df["defaulted"].mean() * 100, 2), "%")
