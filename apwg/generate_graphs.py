import json
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.dates import DateFormatter, YearLocator
from scipy import stats


def create_df_for_metric(data):
    rows = []
    for year in data:
        for month in data[year]:
            value = data[year][month]
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
with open("./datasets/APWG.json", "r") as f:
    data = json.load(f)

# Create DataFrame
df = create_df_for_metric(data)

# Set style for all plots
sns.set_style("whitegrid")
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]


def add_trendline(ax, dates, values, color, alpha=0.5, linestyle="--", label_suffix=""):
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
        label=f"Trend {label_suffix}(R² = {r_value**2:.3f})",
    )


# 1. Total Submissions over time (monthly)
setup_scientific_plot()
ax = plt.gca()
ax.plot(
    df["date"],
    df["value"],
    linewidth=2,
    color="#1f77b4",
    label="Total Submissions",
)

# Split data into two periods
split_date = pd.Timestamp('2015-01-01')
df_early = df[df['date'] < split_date]
df_late = df[df['date'] >= split_date]

# Add trendlines for both periods
add_trendline(
    ax, df_early["date"], df_early["value"], "#ff7f0e", label_suffix="2009-2015 "
)
add_trendline(
    ax, df_late["date"], df_late["value"], "#2ca02c", label_suffix="2015-2024 "
)

format_axis(ax, "Total Phishing Submissions Over Time (2009-2024)")
plt.ylabel("Number of Submissions", fontsize=12, labelpad=10)
plt.legend()
plt.tight_layout()
plt.savefig("./graphs/total_submissions.png", dpi=300, bbox_inches="tight")
plt.close()

# 2. Total Submissions by Year
yearly_df = df.copy()
yearly_df['year'] = yearly_df['date'].dt.year
yearly_totals = yearly_df.groupby('year')['value'].sum().reset_index()

setup_scientific_plot()
ax = plt.gca()
plt.plot(
    yearly_totals['year'],
    yearly_totals['value'],
    linewidth=2,
    color="#1f77b4",
    marker='o'
)
plt.title("Total Phishing Submissions by Year (2009-2024)", pad=20, fontsize=14, fontweight="bold")
plt.xlabel("Year", fontsize=12, labelpad=10)
plt.ylabel("Number of Submissions", fontsize=12, labelpad=10)
plt.xticks(yearly_totals['year'], rotation=45)
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("./graphs/yearly_submissions.png", dpi=300, bbox_inches="tight")
plt.close()

# Print basic statistics
print("\nBasic Statistics:")
print("\nMonthly Statistics:")
print(df["value"].describe())
print("\nYearly Statistics:")
print(yearly_totals["value"].describe())
