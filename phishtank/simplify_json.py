import json


def simplify_json_structure(data):
    simplified = {}
    for metric in data:
        simplified[metric] = {}
        for year in data[metric]:
            for month in data[metric][year]:
                value = data[metric][year][month][year][month]
                if year not in simplified[metric]:
                    simplified[metric][year] = {}
                simplified[metric][year][month] = value
    return simplified


# Load original JSON
with open("phishtank_stats.json", "r") as f:
    data = json.load(f)

# Simplify and save
simplified_data = simplify_json_structure(data)
with open("simplified_stats.json", "w") as f:
    json.dump(simplified_data, f, indent=2)
