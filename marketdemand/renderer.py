

def render_results(data, display_options):
    for item in data:
        rev_text = f" — ${item['revenue']}" if display_options["revenue"] else ""
        industry_text = f" — {item['industry']}" if display_options["industry"] else ""
        print(f"{item['business_name']} — {item['city']}{rev_text}{industry_text}")

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
    
def print_market_summary(filter_options,filtered_data):
            # analytics summary
    pop_data = fetch_population_data()
    baselines = fetch_industry_baselines()
    total_population = 0
    for city in filter_options["cities"]:
        total_population += pop_data.get(city.title(), 0)
    biz_count = len(filtered_data)
    industry_baseline = baselines.get(filter_options["industry"], baselines["Default"])

    if biz_count == 0:
        real_ppb = float("inf")
    else:
        real_ppb = total_population / biz_count
    score = calc_demand_score(real_ppb, industry_baseline)
    rating = classify_market(score)

    print("\nMarket Demand Summary")
    print("----------------------")
    print(f"Cities: {filter_options['cities']}")
    print(f"Industry: {filter_options['industry']}")
    print(f"Population: {total_population:,}")
    print(f"Businesses: {biz_count}")
    print(f"People per Business: {real_ppb:,.0f}")
    print(f"Ideal per Business: {industry_baseline:,}")
    print(f"Demand Score: {score:.2f}x ({rating})")