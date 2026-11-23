"""How well do the simple rules find defaulters?
Reads data/processed/credit_clean.csv and saves results/rule_performance.csv and .md"""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

df = pd.read_csv(ROOT / "data" / "processed" / "credit_clean.csv")
utilisation = df["bill_amount_1"] / df["credit_limit"]

rules = {
    "2+ months late in September": df["pay_status_1"] >= 2,
    "1+ month late in September": df["pay_status_1"] >= 1,
    "Late, or utilisation over 70%": (df["pay_status_1"] >= 1) | (utilisation > 0.7),
}

total_defaulters = int(df["defaulted"].sum())
baseline = df["defaulted"].mean()

rows = []
for name, flag in rules.items():
    flagged = int(flag.sum())
    caught = int(df.loc[flag, "defaulted"].sum())
    precision = caught / flagged
    recall = caught / total_defaulters
    rows.append({
        "Rule": name,
        "Customers flagged": flagged,
        "Defaulters caught": caught,
        "Hit rate (precision)": round(100 * precision, 1),
        "Defaulters caught (recall)": round(100 * recall, 1),
        "Times higher than baseline": round(precision / baseline, 2),
    })

out = pd.DataFrame(rows)
out.to_csv(RESULTS / "rule_performance.csv", index=False)

lines = [f"Baseline default rate: {100 * baseline:.2f}% ({total_defaulters:,} of {len(df):,} customers).", "",
         "| Rule | Customers flagged | Defaulters caught | Hit rate (precision) | Share of all defaulters caught (recall) | Times higher than baseline |",
         "|---|---|---|---|---|---|"]
for _, r in out.iterrows():
    lines.append(f"| {r['Rule']} | {r['Customers flagged']:,} | {r['Defaulters caught']:,} | "
                 f"{r['Hit rate (precision)']:.1f}% | {r['Defaulters caught (recall)']:.1f}% | "
                 f"{r['Times higher than baseline']:.2f} |")
(RESULTS / "rule_performance.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
print("\nSaved results/rule_performance.csv and results/rule_performance.md")