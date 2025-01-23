import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def setup_scientific_plot():
    plt.figure(figsize=(12, 7))
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tick_params(axis="both", which="major", labelsize=10)


# Load data from all sources
with open("./cert_poland/datasets/cert_cp.json", "r") as f:
    cert_data = json.load(f)

with open("./phishtank/datasets/phishtank_stats.json", "r") as f:
    phishtank_data = json.load(f)

with open("./apwg/datasets/APWG.json", "r") as f:
    apwg_data = json.load(f)

# Process CERT Poland data
cert_df = pd.DataFrame(
    [(year, stats["total_submissions"]) for year, stats in cert_data.items()],
    columns=["year", "cert_submissions"],
)
cert_df["year"] = pd.to_numeric(cert_df["year"])

# Process PhishTank data - sum monthly submissions for each year
phishtank_yearly = {}
for year, months in phishtank_data["Total Submissions"].items():
    yearly_sum = sum(int(val.replace(",", "")) for val in months.values())
    phishtank_yearly[year] = yearly_sum

phishtank_df = pd.DataFrame(
    [(year, submissions) for year, submissions in phishtank_yearly.items()],
    columns=["year", "phishtank_submissions"],
)
phishtank_df["year"] = pd.to_numeric(phishtank_df["year"])

# Process APWG data - sum monthly submissions for each year
apwg_yearly = {}
for year, months in apwg_data.items():
    if year != "2024":  # Skip incomplete current year
        yearly_sum = sum(months.values())
        apwg_yearly[year] = yearly_sum

apwg_df = pd.DataFrame(
    [(year, submissions) for year, submissions in apwg_yearly.items()],
    columns=["year", "apwg_submissions"],
)
apwg_df["year"] = pd.to_numeric(apwg_df["year"])

# Merge all dataframes
df = cert_df.merge(phishtank_df, on="year", how="outer")
df = df.merge(apwg_df, on="year", how="outer")

# Normalize data (min-max scaling)
for col in ["cert_submissions", "phishtank_submissions", "apwg_submissions"]:
    if col in df.columns:
        df[f"{col}_normalized"] = (df[col] - df[col].min()) / (
            df[col].max() - df[col].min()
        )

# Create plot
sns.set_style("whitegrid")
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]

setup_scientific_plot()
plt.plot(
    df["year"],
    df["cert_submissions_normalized"],
    linewidth=2,
    marker="o",
    label="CERT Poland",
)
plt.plot(
    df["year"],
    df["phishtank_submissions_normalized"],
    linewidth=2,
    marker="s",
    label="PhishTank",
)
plt.plot(
    df["year"], df["apwg_submissions_normalized"], linewidth=2, marker="^", label="APWG"
)

plt.title(
    "Normalized Phishing Incidents Across Different Sources (2009-2023)",
    pad=20,
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Year", fontsize=12, labelpad=10)
plt.ylabel("Normalized Number of Incidents", fontsize=12, labelpad=10)
plt.legend(fontsize=10)
plt.xticks(df["year"], rotation=45)
plt.tight_layout()
plt.savefig("normalized_comparison.png", dpi=300, bbox_inches="tight")
plt.close()

# Print correlation matrix
print("\nCorrelation Matrix between Sources:")
corr_matrix = df[
    [
        "cert_submissions_normalized",
        "phishtank_submissions_normalized",
        "apwg_submissions_normalized",
    ]
].corr()
print(corr_matrix)
