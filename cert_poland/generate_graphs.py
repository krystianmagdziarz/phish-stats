import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def setup_scientific_plot():
    plt.figure(figsize=(10, 6))
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tick_params(axis="both", which="major", labelsize=10)


# Load JSON data
with open("./datasets/cert_cp.json", "r") as f:
    data = json.load(f)

# Create DataFrame
df = pd.DataFrame(
    [(year, stats["total_submissions"]) for year, stats in data.items()],
    columns=["year", "total_submissions"],
)
df["year"] = pd.to_numeric(df["year"])
df = df.sort_values("year")

# Set style for all plots
sns.set_style("whitegrid")
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]

# 1. Total incidents over time
setup_scientific_plot()
ax = plt.gca()

plt.plot(
    df["year"],
    df["total_submissions"],
    linewidth=2,
    color="#1f77b4",
    marker="o",
    label="Total Incidents",
)

# Calculate and plot trendline
x = df["year"].values
y = df["total_submissions"].values
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(
    x,
    p(x),
    linestyle="--",
    color="#ff7f0e",
    label=f"Trend (R² = {np.corrcoef(x, y)[0, 1] ** 2:.3f})",
)

plt.title(
    "Total Phishing Incidents Reported to CERT Poland (2010-2024)",
    pad=20,
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Year", fontsize=12, labelpad=10)
plt.ylabel("Number of Incidents", fontsize=12, labelpad=10)
plt.legend()
plt.xticks(df["year"], rotation=45)
plt.tight_layout()
plt.savefig("./graphs/total_incidents.png", dpi=300, bbox_inches="tight")
plt.close()

# 2. Year-over-year growth
setup_scientific_plot()
df["pct_change"] = df["total_submissions"].pct_change() * 100

plt.bar(df["year"][1:], df["pct_change"][1:], color="#2ca02c", alpha=0.7)

plt.title(
    "Year-over-Year Growth in Phishing Incidents (%)",
    pad=20,
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Year", fontsize=12, labelpad=10)
plt.ylabel("Percent Change", fontsize=12, labelpad=10)
plt.xticks(df["year"][1:], rotation=45)
plt.axhline(y=0, color="black", linestyle="-", alpha=0.3)
plt.tight_layout()
plt.savefig("./graphs/yearly_growth.png", dpi=300, bbox_inches="tight")
plt.close()

# Print basic statistics
print("\nBasic Statistics:")
print(df["total_submissions"].describe())
print("\nYear-over-Year Growth Statistics:")
print(df["pct_change"].describe())
