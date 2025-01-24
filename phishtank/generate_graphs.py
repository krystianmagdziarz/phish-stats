import json
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.dates import DateFormatter, YearLocator
from scipy import stats


def create_df_for_metric(data, metric):
    rows = []
    for year in data[metric]:
        for month in data[metric][year]:
            value = data[metric][year][month]
            if value is not None and value != '':
                value = float(str(value).replace(",", ""))
                date = datetime.strptime(f"{year}-{month}", "%Y-%m")
                rows.append({"date": date, "value": value})
    return pd.DataFrame(rows).sort_values("date")


def setup_scientific_plot():
    plt.figure(figsize=(10, 6))
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tick_params(axis="both", which="major", labelsize=10)


def format_axis(ax, title):
    ax.set_title(title, pad=20, fontsize=14, fontweight="bold")
    ax.set_xlabel("Year", fontsize=12, labelpad=10)
    ax.xaxis.set_major_locator(YearLocator())
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))
    plt.xticks(rotation=45)


# Load JSON data
with open("./datasets/phishtank_stats.json", "r") as f:
    data = json.load(f)


# Create individual DataFrames
metrics = {
    "total_submissions": "Total Submissions",
    "valid_phishes": "Valid Phishes", 
    "invalid_phishes": "Invalid Phishes",
    "median_time": "Median Time To Verify",
    "total_votes": "Total Votes",
}

dfs = {key: create_df_for_metric(data, value) for key, value in metrics.items()}

# Set style for all plots
sns.set_style("whitegrid")
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]


def add_trendline(ax, dates, values, color, alpha=0.5, linestyle="--"):
    # Convert dates to numeric values for regression
    dates_numeric = np.array([(d - dates.min()).days for d in dates])

    # Remove NaN values
    mask = ~np.isnan(values)
    dates_numeric = dates_numeric[mask]
    values = values[mask]

    # Calculate trend
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        dates_numeric, values
    )
    trend_line = slope * dates_numeric + intercept

    # Plot trend line
    ax.plot(
        dates[mask],
        trend_line,
        color=color,
        alpha=alpha,
        linestyle=linestyle,
        label=f"Trend (R² = {r_value**2:.3f})",
    )


# 1. Total Submissions over time
setup_scientific_plot()
ax = plt.gca()
ax.plot(
    dfs["total_submissions"]["date"],
    dfs["total_submissions"]["value"],
    linewidth=2,
    color="#1f77b4",
    label="Total Submissions",
)
add_trendline(
    ax, dfs["total_submissions"]["date"], dfs["total_submissions"]["value"], "#1f77b4"
)
format_axis(ax, "Total Phishing Submissions Over Time (2009-2017)")
plt.ylabel("Number of Submissions", fontsize=12, labelpad=10)
plt.legend()
plt.tight_layout()
plt.savefig("./graphs/total_submissions.png", dpi=300, bbox_inches="tight")
plt.close()

# 1a. Total Submissions grouped by year
setup_scientific_plot()
yearly_submissions = dfs["total_submissions"].copy()
yearly_submissions["year"] = yearly_submissions["date"].dt.year
yearly_totals = yearly_submissions.groupby("year")["value"].sum()

plt.plot(yearly_totals.index, yearly_totals.values, color="#1f77b4", linewidth=2, marker='o')
plt.title("Total Yearly Phishing Submissions (2009-2017)", 
         pad=20, fontsize=14, fontweight="bold")
plt.xlabel("Year", fontsize=12, labelpad=10)
plt.ylabel("Number of Submissions", fontsize=12, labelpad=10)
plt.xticks(yearly_totals.index, rotation=45)
plt.tight_layout()
plt.savefig("./graphs/yearly_total_submissions.png", dpi=300, bbox_inches="tight")
plt.close()

# 2. Valid Phishes over time
setup_scientific_plot()
ax = plt.gca()
ax.plot(
    dfs["valid_phishes"]["date"],
    dfs["valid_phishes"]["value"],
    linewidth=2,
    color="#2ca02c",
    label="Valid Phishes",
)
add_trendline(
    ax, dfs["valid_phishes"]["date"], dfs["valid_phishes"]["value"], "#2ca02c"
)
format_axis(ax, "Valid Phishing Reports Over Time (2009-2017)")
plt.ylabel("Number of Valid Phishes", fontsize=12, labelpad=10)
plt.legend()
plt.tight_layout()
plt.savefig("./graphs/valid_phishes.png", dpi=300, bbox_inches="tight")
plt.close()

# 3. Invalid Phishes over time
setup_scientific_plot()
ax = plt.gca()
ax.plot(
    dfs["invalid_phishes"]["date"],
    dfs["invalid_phishes"]["value"],
    linewidth=2,
    color="#d62728",
    label="Invalid Phishes",
)
add_trendline(
    ax, dfs["invalid_phishes"]["date"], dfs["invalid_phishes"]["value"], "#d62728"
)
format_axis(ax, "Invalid Phishing Reports Over Time (2009-2017)")
plt.ylabel("Number of Invalid Phishes", fontsize=12, labelpad=10)
plt.legend()
plt.tight_layout()
plt.savefig("./graphs/invalid_phishes.png", dpi=300, bbox_inches="tight")
plt.close()

# 4. Combined phishing reports over time
setup_scientific_plot()
ax = plt.gca()

ax.plot(
    dfs["total_submissions"]["date"],
    dfs["total_submissions"]["value"],
    linewidth=2,
    color="#1f77b4",
    label="Total Submissions"
)

ax.plot(
    dfs["valid_phishes"]["date"],
    dfs["valid_phishes"]["value"],
    linewidth=2,
    color="#2ca02c",
    label="Valid Phishes"
)

ax.plot(
    dfs["invalid_phishes"]["date"],
    dfs["invalid_phishes"]["value"],
    linewidth=2,
    color="#d62728",
    label="Invalid Phishes"
)

format_axis(ax, "Combined Phishing Reports Over Time (2009-2017)")
plt.ylabel("Number of Reports", fontsize=12, labelpad=10)
plt.legend()
plt.tight_layout()
plt.savefig("./graphs/combined_reports.png", dpi=300, bbox_inches="tight")
plt.close()

# 5. Median Time To Verify over time
setup_scientific_plot()
plt.plot(
    dfs["median_time"]["date"],
    dfs["median_time"]["value"],
    linewidth=2,
    color="#ff7f0e",
)
format_axis(plt.gca(), "Median Verification Time Over Time (2009-2017)")
plt.ylabel("Hours", fontsize=12, labelpad=10)
plt.tight_layout()
plt.savefig("./graphs/median_time.png", dpi=300, bbox_inches="tight")
plt.close()

# 6. Median Time To Verify ratio to total submissions
setup_scientific_plot()

# Synchronize dates between median_time and total_submissions
common_dates = set(dfs["median_time"]["date"]) & set(dfs["total_submissions"]["date"])
median_time_df = dfs["median_time"][dfs["median_time"]["date"].isin(common_dates)]
total_submissions_df = dfs["total_submissions"][
    dfs["total_submissions"]["date"].isin(common_dates)
]

# Sort both dataframes by date and reset indices
median_time_df = median_time_df.sort_values("date").reset_index(drop=True)
total_submissions_df = total_submissions_df.sort_values("date").reset_index(drop=True)

# Ensure we have matching dates
merged_df = pd.merge(
    median_time_df, total_submissions_df, on="date", suffixes=("_median", "_total")
)

# Calculate ratio
ratio = merged_df["value_median"] / merged_df["value_total"]

plt.plot(merged_df["date"], ratio, linewidth=2, color="#9467bd")
format_axis(plt.gca(), "Verification Time per Submission Ratio (2009-2017)")
plt.ylabel("Hours per Submission", fontsize=12, labelpad=10)
plt.tight_layout()
plt.savefig("./graphs/median_time_ratio.png", dpi=300, bbox_inches="tight")
plt.close()

# 7. Total Votes over time
setup_scientific_plot()
plt.plot(
    dfs["total_votes"]["date"],
    dfs["total_votes"]["value"],
    linewidth=2,
    color="#8c564b",
)
format_axis(plt.gca(), "Total Community Votes Over Time (2009-2017)")
plt.ylabel("Number of Votes", fontsize=12, labelpad=10)
plt.tight_layout()
plt.savefig("./graphs/total_votes.png", dpi=300, bbox_inches="tight")
plt.close()

# Print basic statistics for each metric
print("\nBasic Statistics:")
for key, metric in metrics.items():
    print(f"\n{metric}:")
    print(dfs[key]["value"].describe())
