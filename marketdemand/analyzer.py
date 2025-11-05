

def count_by_industry(business_data):
    industry_counts = {}
    for item in business_data:
        industry = item["industry"]
        industry_counts[industry] = industry_counts.get(industry, 0) + 1
    return industry_counts

def count_population_per_industry(population,businesses_per_industry):
    population_per_industry = {}
    for business in businesses_per_industry:
        if businesses_per_industry[business] == 0:
            population_per_industry[business] = float("inf")
        else:
            population_per_industry[business] = population/businesses_per_industry[business]
    return population_per_industry

def calc_demand_score(real_people_per_biz,ideal_people_per_biz):
    if ideal_people_per_biz == 0:
        return float('inf')  # Avoid divide-by-zero, treat as massive opportunity
    demand_score = real_people_per_biz/ideal_people_per_biz
    return demand_score
