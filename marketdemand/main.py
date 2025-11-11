from data_sources import (
    fetch_business_data,
    fetch_population_data,
    fetch_industry_data
)
import analyzer
from renderer import render_results
from filtering import filter_businesses, sort_businesses

def main():
    print("=== Market Demand Analyzer ===")
    # 1. Collect filter options
    filter_options = set_filter_options()
    # 2. Load raw datasets
    business_data = fetch_business_data()
    population_data = fetch_population_data()
    industry_data = fetch_industry_data()
    # 3. Fetch unified industry params
    industry_key = filter_options["industry"].lower()
    if industry_key not in industry_data:
        print(f"\n⚠️ Industry '{industry_key}' not found in industry_data.json.")
        return
    industry_params = industry_data[industry_key]
    # 4. Filter and sort businesses (UI layer)
    filtered_list = filter_businesses(business_data, filter_options)
    sorted_list = sort_businesses(filtered_list, filter_options)
    limited_list = sorted_list[:filter_options["num_to_display"]]
    # 5. Full market analysis (now uses unified industry_params)
    analysis_results = analyzer.analyze_market(
        business_data=filtered_list,
        population_data=population_data,
        filters=filter_options,
        industry_params=industry_params
    )
    # 6. Render final output (business list + analysis summary)
    # ---------------------------------------
    render_results(limited_list, analysis_results)

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

# ============================
# RUN PROGRAM
# ============================
if __name__ == "__main__":
    main()
