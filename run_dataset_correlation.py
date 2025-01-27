import json
import pandas as pd
from scipy import stats

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
df = cert_df.merge(phishtank_df, on="year", how="inner")
df = df.merge(apwg_df, on="year", how="inner")

print("\nAnalyzed years range:", df["year"].min(), "-", df["year"].max())
print("Number of years analyzed:", len(df))

# Calculate correlation matrix
correlation_matrix = df[["cert_submissions", "phishtank_submissions", "apwg_submissions"]].corr()

# Print correlation matrix
print("\nCorrelation Matrix:")
print(correlation_matrix)

# Print the data used for correlation
print("\nYearly data used for correlation:")
print(df.to_string(index=False))
