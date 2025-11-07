import analyzer
import data_sources
import json

# ============================
# MAIN PROGRAM ENTRY POINT
# ============================

def main():
    print("=== Market Demand Analyzer ===")

    # 1. Collect filter options from the user
    # ---------------------------------------
    filter_options = set_filter_options()

    # 2. Load raw data
    # ---------------------------------------
    business_data = load_business_data()
    population_data = data_sources.fetch_population_data()

    # NOTE:
    # For now, we assume industry baselines exist in JSON.
    # Example JSON:
    # {
    #   "pest control": {"spend_per_capita": 80, "ideal_ppb": 2000}
    # }
    industry_baselines = load_industry_baselines()

    industry = filter_options["industry"].lower()
    if industry not in industry_baselines:
        print(f"\n⚠️  No industry baseline found for '{industry}'.")
        print("    Add it to baseline JSON before running full analysis.\n")
        return

    spend_per_capita = industry_baselines[industry]["spend_per_capita"]
    ideal_ppb = industry_baselines[industry]["ideal_ppb"]

    # 3. Filter and sort the business data (UI-ready results)
    # ---------------------------------------
    filtered_list = filter_businesses(business_data, filter_options)
    sorted_list = sort_businesses(filtered_list, filter_options)
    limited_list = sorted_list[:filter_options["num_to_display"]]

    # 4. Perform full market analysis (TAM, % remaining, demand score)
    # ---------------------------------------
    analysis_results = analyzer.analyze_market(
        business_data=filtered_list,
        population_data=population_data,
        filters=filter_options,
        spend_per_capita=spend_per_capita,
        ideal_people_per_business=ideal_ppb
    )

    # 5. Render final output (business list + analysis summary)
    # ---------------------------------------
    render_results(limited_list, analysis_results)


# ============================
# SUPPORTING FUNCTIONS
# ============================

def load_business_data():
    """Loads your business dataset from file."""
    with open("../data/sample_business_data.json", "r") as f:
        return json.load(f)


def load_industry_baselines():
    """Loads industry baseline (ideal_ppb, spend_per_capita)."""
    with open("../data/industry_baselines.json", "r") as f:
        return json.load(f)


# ---------------------------------------
# FILTER + SORT HELPERS (UI LAYER)
# ---------------------------------------

def filter_businesses(business_data, filters):
    """Filter by cities + industry."""
    cities = filters["cities"]
    industry = filters["industry"]

    filtered = []
    for b in business_data:
        city_ok = (not cities) or (b["city"].lower() in [c.lower() for c in cities])
        industry_ok = (not industry) or (b["industry"].lower() == industry.lower())

        if city_ok and industry_ok:
            filtered.append(b)

    return filtered


def sort_businesses(data, filters):
    """Sort based on user’s selected field."""
    sort_by = filters["sort_by"]

    # NOTE: You removed `display_options`, but leave this comment so you 
    #       can re-add display toggles later if you want to show/hide revenue, industry, etc.
    # display_options = { "revenue": False, "industry": False }

    if sort_by == "revenue":
        return sorted(data, key=lambda x: x["revenue"], reverse=True)

    elif sort_by == "industry":
        return sorted(data, key=lambda x: x["industry"].lower())

    elif sort_by == "business_name":
        return sorted(data, key=lambda x: x["business_name"].lower())

    elif sort_by == "distance":
        print("** distance sort not implemented **")
        return data

    return data


# ---------------------------------------
# USER INPUT FOR FILTERING
# ---------------------------------------

def set_filter_options():
    """Collect basic filter options for the MVP."""
    num = int(input("How many results to display? "))
    industry = input("Industry: ").strip()
    city_input = input("Cities (comma separated, blank for all): ").strip()

    cities = [c.strip() for c in city_input.split(",")] if city_input else []

    sort_by = input("Sort by (1=name, 2=revenue, 3=industry, 4=distance): ").strip()
    sort_map = {
        "1": "business_name",
        "2": "revenue",
        "3": "industry",
        "4": "distance"
    }

    return {
        "num_to_display": num,
        "industry": industry,
        "cities": cities,
        "sort_by": sort_map.get(sort_by, "business_name")
    }


# ---------------------------------------
# RENDERING OUTPUT (UI)
# ---------------------------------------

def render_results(business_list, analysis):
    """Prints both the business results and the market analysis summary."""

    print("\n=== BUSINESS RESULTS ===")
    for b in business_list:
        print(f"{b['business_name']} — {b['city']} — {b['industry']} — ${b['revenue']}")

    print("\n=== MARKET ANALYSIS ===")
    print(f"Population: {analysis['population']}")
    print(f"TAM: ${analysis['tam']:,}")
    print(f"Current Revenue: ${analysis['current_revenue']:,}")
    print(f"Remaining TAM: ${analysis['remaining_tam']:,}")
    print(f"Remaining TAM %: {analysis['remaining_pct']*100:.2f}%")
    print(f"Competition Score: {analysis['competition_score']:.2f}")
    print(f"Demand Score: {analysis['demand_score']:.2f}")


# ============================
# RUN PROGRAM
# ============================

if __name__ == "__main__":
    main()
