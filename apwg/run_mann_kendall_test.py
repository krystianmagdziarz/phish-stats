import json
import pymannkendall as mk

# Load JSON data
with open("./datasets/APWG.json", "r") as f:
    data = json.load(f)

# Convert data to time series and split by period
values = []
values_before_2015 = []
values_after_2015 = []

for year in sorted(data.keys()):
    for month in sorted(data[year].keys()):
        value = data[year][month]
        if value is not None and value != '':
            float_value = float(str(value).replace(",", ""))
            values.append(float_value)
            
            if int(year) < 2015:
                values_before_2015.append(float_value)
            else:
                values_after_2015.append(float_value)

print("\nAnalyzing trends in phishing reports from APWG:")
print("\nMonthly values:", values)

# Perform Mann-Kendall test for full period
result = mk.original_test(values)

print("\nMann-Kendall Test Results (Full Period):")
print(f"Trend: {result.trend}")
print(f"Z-Score: {result.z}")
print(f"P-Value: {result.p}")
print(f"Tau: {result.Tau}")
print(f"S: {result.s}")

# Perform Mann-Kendall test for period before 2015
result_before = mk.original_test(values_before_2015)

print("\nMann-Kendall Test Results (Before 2015):")
print(f"Trend: {result_before.trend}")
print(f"Z-Score: {result_before.z}")
print(f"P-Value: {result_before.p}")
print(f"Tau: {result_before.Tau}")
print(f"S: {result_before.s}")

# Perform Mann-Kendall test for period after 2015
result_after = mk.original_test(values_after_2015)

print("\nMann-Kendall Test Results (2015 and After):")
print(f"Trend: {result_after.trend}")
print(f"Z-Score: {result_after.z}")
print(f"P-Value: {result_after.p}")
print(f"Tau: {result_after.Tau}")
print(f"S: {result_after.s}")

print("\nInterpretation:")
print("This analysis examines phishing reports from APWG over different time periods:")
print("1. Full period: Entire dataset")
print("2. Before 2015: Early period")
print("3. 2015 and After: Recent period")
print("\nThe Mann-Kendall test helps identify if there's a statistically")
print("significant upward or downward trend in these periods.")
print("A p-value < 0.05 indicates a statistically significant trend.")
