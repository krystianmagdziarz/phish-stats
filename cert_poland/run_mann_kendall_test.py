import json
import pymannkendall as mk

# Load JSON data
with open("./datasets/cert_cp.json", "r") as f:
    data = json.load(f)

# Convert data to time series
values = []
for year in sorted(data.keys()):
    value = data[year]["total_submissions"]
    if value is not None and value != '':
        values.append(float(str(value).replace(",", "")))

print(values)

# Perform Mann-Kendall test
result = mk.original_test(values)

print("\nMann-Kendall Test Results:")
print(f"Trend: {result.trend}")
print(f"Z-Score: {result.z}")
print(f"P-Value: {result.p}")
print(f"Tau: {result.Tau}")
print(f"S: {result.s}")
