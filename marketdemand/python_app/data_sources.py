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
def get_business_data(source="file", industry=None, cities=None):
    if source == "api":
        if not cities:
            print("⚠️ API business mode requires at least one city for now. Falling back to file data.")
            data = fetch_business_data()
        else:
            data = fetch_business_api(industry=industry, cities=cities)
            if not data:
                print("⚠️ Business API returned no data. Falling back to file data.")
                data = fetch_business_data()
    else:
        data = fetch_business_data()

    validate_data(data, "business")
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
        if not data:
            print("⚠️ Demographic API returned no data. Falling back to file data.")
            data = fetch_demographic_data()
    else:
        data = fetch_demographic_data()

    validate_data(data, "demographic")
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
        response = requests.get(
            base_url,
            params=params,
            timeout=30,
            headers={"User-Agent": "MarketDemandAnalyzer/0.1"}
        )

        # If Census returns HTML or blank text, response.json() will crash.
        content_type = (response.headers.get("Content-Type") or "").lower()

        if response.status_code != 200:
            print(f"⚠️ Census HTTP {response.status_code}: {response.text[:200]}")
            return {}

        if "json" not in content_type:
            print(f"⚠️ Census returned non-JSON content-type={content_type}. Body head: {response.text[:200]}")
            return {}

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


def fetch_business_api(industry: str, cities: list[str] | None = None, max_per_city: int = 20):
    """
    Google Places (New) Text Search.
    Returns list[dict] in your app's business schema.
    revenue is None because Places doesn't provide it.
    """
    try:
        api_key = (fetch_API_Keys().get("google_maps_api_key", "") or "").strip()
        if not api_key:
            print("⚠️ Google Places API key missing. Returning empty business list.")
            return []
    
        url = "https://places.googleapis.com/v1/places:searchText"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress,places.rating,places.userRatingCount",
        }
    
        if not cities:
            queries = [f"{industry} in Utah"]
        else:
            queries = [f"{industry} in {c}, UT" for c in cities]
    
        results = []
    
        for q in queries:
            payload = {
                "textQuery": q,
                "maxResultCount": max_per_city,
                "languageCode": "en",
                "regionCode": "US",
            }
    
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
    
            if resp.status_code != 200:
                print(f"⚠️ Places HTTP {resp.status_code}: {resp.text[:200]}")
                continue
    
            data = resp.json()
            places = data.get("places", [])
    
            for p in places:
                name = ((p.get("displayName") or {}).get("text")) or ""
                addr = p.get("formattedAddress") or ""
                place_id = p.get("id")
    
                # best-effort city parsing: take first segment of address
                # e.g. "155 S Freedom Blvd, Provo, UT 84601" -> "provo"
                city_guess = ""
                if "," in addr:
                    city_guess = addr.split(",")[1].strip().lower()  # 1 is city in typical formattedAddress
    
                results.append({
                    "business_name": name,
                    "city": city_guess,
                    "industry": industry,
                    "revenue": None,
                    "place_id": place_id,
                    "rating": p.get("rating"),
                    "user_ratings_total": p.get("userRatingCount"),
                })
            deduped = {}
            for b in results:
                key = b.get("place_id") or (b.get("business_name","").lower(), b.get("city","").lower())
                deduped[key] = b
            return list(deduped.values())
    except Exception as e:
        print(f"⚠️ API error (business): {e}")
        return {}
    return results



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