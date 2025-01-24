import json
import pymannkendall as mk

# Load JSON data
with open("./datasets/phishtank_stats.json", "r") as f:
    data = json.load(f)

# Convert data to time series for Total Submissions
submissions_values = []
for year in sorted(data["Total Submissions"].keys()):
    for month in sorted(data["Total Submissions"][year].keys()):
        value = data["Total Submissions"][year][month]
        if value is not None and value != "":
            submissions_values.append(float(str(value).replace(",", "")))

# Convert data to time series for Total Votes
votes_values = []
for year in sorted(data["Total Votes"].keys()):
    for month in sorted(data["Total Votes"][year].keys()):
        value = data["Total Votes"][year][month]
        if value is not None and value != "":
            votes_values.append(float(str(value).replace(",", "")))

print("\nAnalyzing trends in phishing reports and community voting behavior:")
print("\n1. Total Submissions Analysis")
print("Monthly values:", submissions_values)

# Perform Mann-Kendall test for submissions
submissions_result = mk.original_test(submissions_values)

print("\nMann-Kendall Test Results for Total Submissions:")
print(f"Trend: {submissions_result.trend}")
print(f"Z-Score: {submissions_result.z}")
print(f"P-Value: {submissions_result.p}")
print(f"Tau: {submissions_result.Tau}")
print(f"S: {submissions_result.s}")

print("\n2. Total Votes Analysis")
print("Monthly values:", votes_values)

# Perform Mann-Kendall test for votes
votes_result = mk.original_test(votes_values)

print("\nMann-Kendall Test Results for Total Votes:")
print(f"Trend: {votes_result.trend}")
print(f"Z-Score: {votes_result.z}")
print(f"P-Value: {votes_result.p}")
print(f"Tau: {votes_result.Tau}")
print(f"S: {votes_result.s}")

print("\nInterpretation:")
print("This analysis examines two key metrics from PhishTank:")
print("1. Total Submissions: Number of reported phishing sites per month")
print("2. Total Votes: Number of community votes cast per month")
print("\nThe Mann-Kendall test helps identify if there's a statistically")
print("significant upward or downward trend in these metrics over time.")
print("A p-value < 0.05 indicates a statistically significant trend.")
