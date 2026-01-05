import json
import os
import requests

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
        # Lowercase city names for matching, preserve subfields
        normalized = {k.lower(): v for k, v in raw.items()}
        return normalized


def fetch_industry_data():
    file_path = os.path.join(DATA_DIR, "industry_data.json")
    with open(file_path, "r") as f:
        raw = json.load(f)
        # Make industry keys case-insensitive
        normalized = {k.lower(): v for k, v in raw.items()}
        return normalized


# ======================
# API FALLBACK INTERFACES
# ======================
def get_business_data(source="file"):
    if source == "api":
        data = fetch_business_api()
    else:
        data = fetch_business_data()
    validate_data(data,"business")
    return data


def get_industry_data(source="file"):
    if source == "api":
        data = fetch_industry_api()
    else:
        data = fetch_industry_data()
    validate_data(data,"industry")
    return data


def get_demographic_data(source="file"):
    if source == "api":
        data = fetch_demographic_api()
    else:
        data = fetch_demographic_data()
    validate_data(data,"demographic")
    return data


# ======================
# API STUBS (for future integration)
# ======================

def fetch_API_Keys():
    file_path = os.path.join(DATA_DIR, "apiKeys.json")
    try:
        with open(file_path, "r") as f:
            return json.load(f) or {}
    except FileNotFoundError:
        print("⚠️ apiKeys.json not found in /data. Continuing without API key.")
        return {}
    except json.JSONDecodeError:
        print("⚠️ apiKeys.json is not valid JSON. Continuing without API key.")
        return {}

def fetch_demographic_api():
    try:
        api_key = fetch_API_Keys().get("Census_API_Key", "")
        base_url = "https://api.census.gov/data/2022/acs/acs5"
        # Utah FIPS = 49
        params = {
        "get": "NAME,B01003_001E,B19013_001E",
        "for": "place:*",
        "in": "state:49",
        }
        if api_key:
            params["key"] = api_key
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        headers = data[0]
        rows = data[1:]
        name_idx = headers.index("NAME")
        pop_idx = headers.index("B01003_001E")
        income_idx = headers.index("B19013_001E")

        result = {}
        for row in rows:
                name = row[name_idx]
                place_part = name.split(",")[0].strip().lower()
                city = normalize_place_name(place_part)

                try:
                    population = int(row[pop_idx])
                    income = int(row[income_idx])
                    # Filter Census sentinel / invalid values
                    if income <= 0 or income > 1_000_000:
                        continue
                except (TypeError, ValueError):
                    continue

                result[city] = {
                    "population": population,
                    "avg_income": income
                }
        return result
    except Exception as e:
        print(f"⚠️ API error (demographic): {e}")
    return {}


def fetch_business_api():
    try:
        # later: actual API logic
        return []
    except Exception as e:
        print(f"⚠️ API error (business): {e}")
        return []


def fetch_industry_api():
    try:
        # later: actual API logic
        return []
    except Exception as e:
        print(f"⚠️ API error (business): {e}")
        return []



def validate_data(data, data_type):
    """Warn if no data loaded."""
    if not data:
        print(f"⚠️  Warning: No {data_type} data loaded.")


def normalize_place_name(raw_name: str) -> str:
    """
    Converts Census place names like 'Provo city' or 'Alta town'
    to a stable key like 'provo' or 'alta'.
    """
    s = (raw_name or "").strip().lower()

    # remove common Census place suffixes (Utah)
    suffixes = [
        " city", " town", " metro township", " cdp", " village"
    ]
    for suf in suffixes:
        if s.endswith(suf):
            s = s[: -len(suf)].strip()

    return s