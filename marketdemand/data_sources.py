import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")


# ======================
# FILE-BASED FETCHERS
# ======================
def fetch_business_data():
    file_path = os.path.join(DATA_DIR, "sample_business_data.json")
    with open(file_path, "r") as f:
        return json.load(f)


def fetch_demographic_data():
    file_path = os.path.join(DATA_DIR, "sample_demographic_data.json")
    with open(file_path, "r") as f:
        raw = json.load(f)
        # Make city keys case-insensitive
        return {k.lower(): v for k, v in raw.items()}


def fetch_industry_data():
    file_path = os.path.join(DATA_DIR, "industry_data.json")
    with open(file_path, "r") as f:
        raw = json.load(f)
        # Make industry keys case-insensitive
        return {k.lower(): v for k, v in raw.items()}


# ======================
# API FALLBACK INTERFACES
# ======================
def get_business_data(source="file"):
    if source == "api":
        return fetch_business_api()
    return fetch_business_data()


def get_industry_data(source="file"):
    if source == "api":
        return fetch_industry_api()
    return fetch_industry_data()


def get_demographic_data(source="file"):
    if source == "api":
        return fetch_demographic_api()
    return fetch_demographic_data()


# ======================
# API STUBS (for future integration)
# ======================
def fetch_demographic_api():
    # TODO: implement Census, City Data, or similar API
    pass


def fetch_business_api():
    # TODO: implement Yelp or Google Maps API
    pass


def fetch_industry_api():
    # TODO: connect to internal industry baseline service
    pass
