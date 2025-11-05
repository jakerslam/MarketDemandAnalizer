from analyzer import count_by_industry, calc_demand_score, count_population_per_industry
from data_sources import fetch_business_data, fetch_population_data, fetch_industry_baselines
import utils

def main():
    filter_options = set_filter_options()
    if get_user_input():
        display_data(filter_options)

def set_filter_options():
    filter_options_num = int(input("set the number of results to display: "))
    filter_options_sort_by = input("Enter '1' to sort by business name, '2' to sort by revenue, '3' to sort by industry, '4' to sort by distance ")
    filter_options_city = input("set the city to display: ")
    filter_options_industry = input("set the industry to display: ")
    sort_by_dictionary = {
        "1" : "business_name",
        "2" : "revenue",
        "3" : "industry",
        "4" : "distance"
    }
    filter_options = {
    "num_to_display": filter_options_num,
    "city": filter_options_city,
    "industry": filter_options_industry,
    "sort_by": sort_by_dictionary[filter_options_sort_by]
    }
    show_filters(filter_options)
    return filter_options

def show_filters(filters):
    print(f"""
Active Filters:
---------------
City: {filters['city']}
Industry: {filters['industry']}
Sort by: {filters['sort_by']}
Results to display: {filters['num_to_display']}
""")

def get_user_input():
    display = input("Do you want to dsiplay data? y/n: ")
    if display == 'y':
        return True
    return False

def display_data(filter_options):
    display_options = {
        "revenue" : False,
        "industry" : False,
    }
    #open file#
    data = load_data()
    #apply filters#
    if filter_options["city"]:
        data = [item for item in data if item["city"].lower() == filter_options["city"].lower()]
    if filter_options["industry"]:
        data = [item for item in data if item["industry"].lower() == filter_options["industry"].lower()]
        display_options["industry"] = True
    #apply sorts#
    if filter_options["sort_by"] == "distance":
        #data = sorted(data, key=lambda item: item["distance"])
        print("**distance sort under construction**")
    elif filter_options["sort_by"] == "revenue":
        data = sorted(data, key=lambda item: item["revenue"], reverse=True)
        display_options["revenue"] = True
    elif filter_options["sort_by"] == "industry":
        data = sorted(data, key=lambda item: item["industry"].lower())
        display_options["industry"] = True
    elif filter_options["sort_by"] == "business_name":
        data = sorted(data, key=lambda item: item["business_name"].lower())
    #slice data to correct length of items#
    data = data[:filter_options['num_to_display']]
    #render data#
    render_results(data,display_options)
    if filter_options["industry"]:
        print_market_summary(filter_options,data)

def print_market_summary(filter_options,filtered_data):
            # analytics summary
    pop_data = fetch_population_data()
    baselines = fetch_industry_baselines()
    population = pop_data.get(filter_options["city"].title(), None)
    biz_count = len(filtered_data)
    industry_baseline = baselines.get(filter_options["industry"], baselines["Default"])

    real_ppb = population / biz_count if biz_count and population else 1
    score = calc_demand_score(real_ppb, industry_baseline)
    rating = classify_market(score)

    print("\nMarket Demand Summary")
    print("----------------------")
    print(f"City: {filter_options['city']}")
    print(f"Industry: {filter_options['industry']}")
    print(f"Population: {population:,}")
    print(f"Businesses: {biz_count}")
    print(f"People per Business: {real_ppb:,.0f}")
    print(f"Ideal per Business: {industry_baseline:,}")
    print(f"Demand Score: {score:.2f}x ({rating})")


def classify_market(score):
    if score == float("inf"):
        return "No competition yet ✅ (blue ocean)"
    if score > 3:
        return "High Opportunity ✅"
    elif score > 1:
        return "Moderate Opportunity ⚠️"
    elif score > 0.5:
        return "Crowded 🟠"
    else:
        return "Saturated ❌"

def load_data():
    data = fetch_business_data()
    return data

# render results based on filter and sort settings
def render_results(data, display_options):
    for item in data:
        rev_text = f" — ${item['revenue']}" if display_options["revenue"] else ""
        industry_text = f" — {item['industry']}" if display_options["industry"] else ""
        print(f"{item['business_name']} — {item['city']}{rev_text}{industry_text}")
        

if __name__ == "__main__":
    main()
