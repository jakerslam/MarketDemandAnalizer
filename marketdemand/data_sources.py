import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

def fetch_business_data():
    file_path = os.path.join(DATA_DIR, "sample_business_data.json")
    with open(file_path, "r") as f:
        return json.load(f)

def fetch_population_data():
    file_path = os.path.join(DATA_DIR, "sample_demographic_data.json")
    with open(file_path, "r") as f:
        return json.load(f)

def fetch_industry_data():
    file_path = os.path.join(DATA_DIR, "industry_data.json")
    with open(file_path, "r") as f:
        return json.load(f)

        
