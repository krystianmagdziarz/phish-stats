import json
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def calculate_seasonality_index(data):
    """
    Calculates seasonality index based on the formula:
    X_m = sum(X_m,y) / n  - mean for given month
    X = sum(X_m) / 12     - global mean
    SI_m = (X_m / X) * 100 - seasonality index
    """
    # Convert JSON data to DataFrame
    rows = []
    for year in data:
        for month in data[year]:
            value = data[year][month]
            if value is not None and value != "":
                value = float(str(value).replace(",", ""))
                date = datetime.strptime(f"{year}-{month}", "%Y-%m")
                rows.append({"date": date, "value": value})

    df = pd.DataFrame(rows)
    df["month"] = df["date"].dt.month

    # Calculate X_m (mean for each month)
    monthly_means = df.groupby("month")["value"].mean()

    # Calculate X (global mean)
    global_mean = monthly_means.mean()

    # Calculate SI_m (seasonality index)
    seasonality_index = (monthly_means / global_mean) * 100

    return pd.DataFrame(
        {
            "month": range(1, 13),
            "monthly_mean": monthly_means,
            "seasonality_index": seasonality_index,
        }
    )


def main():
    # Load data
    with open("./datasets/APWG.json", "r") as f:
        data = json.load(f)

    # Calculate seasonality index
    seasonality = calculate_seasonality_index(data)

    # Save results to CSV
    seasonality.to_csv("./datasets/seasonality_index.csv", index=False)

    # Set style for plot
    sns.set_style("whitegrid")
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["font.serif"] = ["Times New Roman"]

    # Create visualization
    plt.figure(figsize=(10, 6))
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.tick_params(axis="both", which="major", labelsize=10)

    plt.plot(
        seasonality["month"],
        seasonality["seasonality_index"],
        color="#2ca02c",
        linewidth=2,
        marker='o'
    )

    plt.title(
        "APWG Phishing Reports Seasonality Index (2009-2025)",
        pad=20,
        fontsize=14,
        fontweight="bold",
    )
    plt.xlabel("Month", fontsize=12, labelpad=10)
    plt.ylabel("Seasonality Index", fontsize=12, labelpad=10)

    # Set month labels
    plt.xticks(range(1, 13), rotation=45)

    # Add line at 100 (mean)
    plt.axhline(y=100, color="black", linestyle="-", alpha=0.3)

    plt.tight_layout()
    plt.savefig("./graphs/seasonality_index.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Display statistics
    print("\nSeasonality statistics:")
    print("\nMonthly means:")
    print(seasonality[["month", "monthly_mean"]].to_string(index=False))
    print("\nSeasonality indices:")
    print(seasonality[["month", "seasonality_index"]].to_string(index=False))


if __name__ == "__main__":
    main()
