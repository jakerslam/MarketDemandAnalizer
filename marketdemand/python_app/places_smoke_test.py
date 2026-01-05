import requests
import json

API_KEY = "AIzaSyBBcrE_HqWe7a4gflNSI2NDDv6SYwhfZrg"

url = "https://places.googleapis.com/v1/places:searchText"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    # FieldMask is REQUIRED for Places (New)
    "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.id"
}

payload = {
    "textQuery": "pest control in Provo, UT",
    "maxResultCount": 5,
    "languageCode": "en",
    "regionCode": "US"
}

resp = requests.post(url, headers=headers, json=payload, timeout=30)

print("STATUS:", resp.status_code)
print("CONTENT-TYPE:", resp.headers.get("Content-Type"))
print("BODY (first 800 chars):")
print(resp.text[:800])

# If it is JSON, pretty print a bit
try:
    data = resp.json()
    print("\nPARSED JSON KEYS:", list(data.keys()))
    if "places" in data:
        print("\nPLACES:")
        for p in data["places"]:
            name = (p.get("displayName") or {}).get("text")
            addr = p.get("formattedAddress")
            print("-", name, "|", addr)
except Exception as e:
    print("\nJSON parse failed:", e)
