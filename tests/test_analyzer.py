

from marketdemand.analyzer import count_businesses_by_city

# Load mock data
import json
with open("data/sample_data.json") as f:
    sample_data = json.load(f)

results = count_businesses_by_city(sample_data)
print(results)