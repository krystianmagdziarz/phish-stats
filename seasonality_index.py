import json
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


def calculate_seasonality_index(data, is_phishtank=True):
    """
    Calculates seasonality index based on the formula:
    X_m = sum(X_m,y) / n  - mean for given month
    X = sum(X_m) / 12     - global mean
    SI_m = (X_m / X) * 100 - seasonality index
    """
    # Convert JSON data to DataFrame
    rows = []
    if is_phishtank:
        data_iter = data['Total Submissions']
    else:
        data_iter = data
        
    for year in data_iter:
        for month in data_iter[year]:
            value = data_iter[year][month]
            if value is not None and value != "":
                value = float(str(value).replace(",", ""))
                date = datetime.strptime(f"{year}-{month}", "%Y-%m")
                rows.append({"date": date, "value": value})

    df = pd.DataFrame(rows)
    df["month"] = df["date"].dt.month
    df["year"] = df["date"].dt.year
    return df

def calculate_common_period_seasonality(phishtank_df, apwg_df):
    # Find common years
    phishtank_years = set(phishtank_df["year"])
    apwg_years = set(apwg_df["year"])
    common_years = sorted(phishtank_years.intersection(apwg_years))
    
    print(f"\nAnalyzing common period: {min(common_years)}-{max(common_years)}")
    
    # Filter data for common years
    phishtank_filtered = phishtank_df[phishtank_df["year"].isin(common_years)]
    apwg_filtered = apwg_df[apwg_df["year"].isin(common_years)]
    
    # Calculate seasonality indices for filtered data
    def calculate_indices(df):
        monthly_stats = df.groupby("month")["value"].agg(['mean', 'std']).reset_index()
        global_mean = monthly_stats['mean'].mean()
        
        monthly_stats['seasonality_index'] = (monthly_stats['mean'] / global_mean) * 100
        monthly_stats['si_std'] = (monthly_stats['std'] / global_mean) * 100
        
        return monthly_stats
    
    return calculate_indices(phishtank_filtered), calculate_indices(apwg_filtered)

def main():
    # Load PhishTank data
    with open("./phishtank/datasets/phishtank_stats.json", "r") as f:
        phishtank_data = json.load(f)

    # Load APWG data
    with open("./apwg/datasets/APWG.json", "r") as f:
        apwg_data = json.load(f)

    # Convert data to DataFrames with dates
    phishtank_df = calculate_seasonality_index(phishtank_data, is_phishtank=True)
    apwg_df = calculate_seasonality_index(apwg_data, is_phishtank=False)
    
    # Calculate seasonality indices for common period
    phishtank_seasonality, apwg_seasonality = calculate_common_period_seasonality(phishtank_df, apwg_df)

    # Set style for plot
    sns.set_style("whitegrid")
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]

    # Create visualization
    plt.figure(figsize=(10, 6))
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tick_params(axis="both", which="major", labelsize=10)

    # Plot PhishTank data with confidence interval
    plt.plot(
        phishtank_seasonality["month"],
        phishtank_seasonality["seasonality_index"],
        color="#2ca02c",
        linewidth=2,
        marker='o',
        label='PhishTank'
    )
    plt.fill_between(
        phishtank_seasonality["month"],
        phishtank_seasonality["seasonality_index"] - phishtank_seasonality["si_std"],
        phishtank_seasonality["seasonality_index"] + phishtank_seasonality["si_std"],
        color="#2ca02c",
        alpha=0.2
    )

    # Plot APWG data with confidence interval
    plt.plot(
        apwg_seasonality["month"],
        apwg_seasonality["seasonality_index"],
        color="#1f77b4",
        linewidth=2,
        marker='s',
        label='APWG'
    )
    plt.fill_between(
        apwg_seasonality["month"],
        apwg_seasonality["seasonality_index"] - apwg_seasonality["si_std"],
        apwg_seasonality["seasonality_index"] + apwg_seasonality["si_std"],
        color="#1f77b4",
        alpha=0.2
    )

    plt.title(
        "Seasonality Index Comparison: PhishTank vs APWG (Common Period)",
        pad=20,
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("Month", fontsize=12, labelpad=10)
    plt.ylabel("Seasonality Index", fontsize=12, labelpad=10)
    plt.legend(fontsize=10)

    # Set month labels
    plt.xticks(range(1, 13), rotation=45)

    # Add line at 100 (mean)
    plt.axhline(y=100, color="black", linestyle="-", alpha=0.3)

    plt.tight_layout()
    plt.savefig("seasonality_comparison.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Display statistics
    print("\nPhishTank Seasonality statistics:")
    print("\nMonthly means with standard deviation:")
    print(phishtank_seasonality[["month", "mean", "std"]].to_string(index=False))
    print("\nSeasonality indices with standard deviation:")
    print(phishtank_seasonality[["month", "seasonality_index", "si_std"]].to_string(index=False))

    print("\nAPWG Seasonality statistics:")
    print("\nMonthly means with standard deviation:")
    print(apwg_seasonality[["month", "mean", "std"]].to_string(index=False))
    print("\nSeasonality indices with standard deviation:")
    print(apwg_seasonality[["month", "seasonality_index", "si_std"]].to_string(index=False))


if __name__ == "__main__":
    main()
