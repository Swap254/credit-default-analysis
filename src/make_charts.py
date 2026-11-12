"""Step 4: save four charts into results/ (matplotlib only)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")          # draw to files, no window needed
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
df = pd.read_csv(ROOT / "data" / "processed" / "credit_clean.csv")
overall = 100 * df["defaulted"].mean()
BLUE, RED = "#2F6DB5", "#C0392B"


def bar_chart(labels, values, title, filename, xlabel):
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = [RED if v > overall else BLUE for v in values]
    bars = ax.bar(labels, values, color=colors)
    ax.axhline(overall, color="grey", linestyle="--", linewidth=1)
    ax.text(len(labels) - 0.5, overall + 1, f"Overall {overall:.1f}%", ha="right", color="grey", fontsize=9)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v + 1, f"{v:.1f}%", ha="center", fontsize=9)
    ax.set_ylabel("Default rate (%)")
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.set_ylim(0, max(values) * 1.2)
    plt.xticks(rotation=15, ha="right")
    plt.tight_layout()
    fig.savefig(RES / filename, dpi=150)
    plt.close(fig)
    print("Saved", filename)


# 1. Default rate by segment (reuse the saved segment summary)
seg = pd.read_csv(RES / "segment_summary.csv")
bar_chart(seg["segment"], seg["default_rate_pct"],
          "Default rate by customer segment", "default_rate_by_segment.png", "Segment")

# 2. Default rate by credit limit band
bands = pd.cut(df["credit_limit"], [0, 50000, 150000, 300000, 10**7],
               labels=["Under 50k", "50k-150k", "150k-300k", "300k+"], right=False)
lim = 100 * df.groupby(bands, observed=True)["defaulted"].mean()
bar_chart(lim.index.astype(str), lim.values,
          "Default rate by credit limit", "default_rate_by_credit_limit.png", "Credit limit (NT$)")

# 3. Default rate by September repayment status
pay = df[df["pay_status_1"].between(-2, 3)].groupby("pay_status_1")["defaulted"].mean() * 100
names = {-2: "No use", -1: "Paid in full", 0: "Min. paid", 1: "1 month late", 2: "2 months late", 3: "3 months late"}
bar_chart([names[i] for i in pay.index], pay.values,
          "Default rate by September repayment status", "default_rate_by_repayment_status.png",
          "September repayment status")

# 4. Average monthly bill, April to September
months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep"]
avg_bill = [df[f"bill_amount_{m}"].mean() for m in [6, 5, 4, 3, 2, 1]]
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(months, avg_bill, marker="o", color=BLUE)
for x, y in zip(months, avg_bill):
    ax.text(x, y + 800, f"{y:,.0f}", ha="center", fontsize=9)
ax.set_title("Average bill amount per month (2005)")
ax.set_ylabel("NT$")
ax.set_ylim(min(avg_bill) * 0.9, max(avg_bill) * 1.1)
plt.tight_layout()
fig.savefig(RES / "avg_bill_trend.png", dpi=150)
plt.close(fig)
print("Saved avg_bill_trend.png")
