

###
# Main interface function to main
###
def analyze_market(business_data, population_data, filters, spend_per_capita, ideal_people_per_business):
    # 1. Filter businesses by industry & cities (analyzer should do this)
    filtered_businesses = [
        b for b in business_data 
        if (filters["industry"].lower() == b["industry"].lower())
        and (not filters["cities"] or b["city"].lower() in [c.lower() for c in filters["cities"]])
    ]
    # 2. Sum population for selected cities
    total_population = 0
    for city in filters["cities"]:
        total_population += population_data.get(city.title(), 0)
    # 3. Compute TAM
    tam = calculate_tam(total_population, spend_per_capita)
    # 4. Compute existing revenue in the region
    current_rev = calculate_current_revenue(filtered_businesses)
    # 5. Compute remaining TAM and percentage
    remaining_tam = calculate_remaining_tam(tam, current_rev)
    remaining_pct = calculate_remaining_tam_pct(remaining_tam, tam)
    # 6. Compute real people-per-business
    if len(filtered_businesses) == 0:
        real_ppb = float("inf")
    else:
        real_ppb = total_population / len(filtered_businesses)
    # 7. Compute competition score
    competition_score = calculate_competition_score(real_ppb, ideal_people_per_business)
    # 8. Final demand score
    demand_score = calc_demand_score(competition_score, remaining_pct)
    # 9. Return all results
    return {
        "tam": tam,
        "current_revenue": current_rev,
        "remaining_tam": remaining_tam,
        "remaining_pct": remaining_pct,
        "competition_score": competition_score,
        "demand_score": demand_score,
        "businesses": filtered_businesses,
        "population": total_population,
        "filters": filters
    }


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

def calc_demand_score(competition_score,remaining_tam_pct,tam_weight=0.5):
    if competition_score == float('inf'):
        competition_score = 5  # treat as massive opportunity
    comp_weight = 1 - tam_weight
    demand_score = (competition_score*comp_weight) + (remaining_tam_pct*tam_weight)
    return demand_score

def calculate_remaining_tam_pct(remaining_tam, tam):
    if tam <= 0:
        return 0
    return remaining_tam / tam
    
def calculate_competition_score(real_people_per_biz,ideal_people_per_biz):
    if ideal_people_per_biz == 0:
        return float('inf')  # Avoid divide-by-zero, treat as massive opportunity
    competition_score = real_people_per_biz/ideal_people_per_biz
    return competition_score
    

def calculate_tam(population, spend_per_capita):
    return population * spend_per_capita

def calculate_tam_remaining(tam, current_revenue):
    remaining = tam - current_revenue
    if remaining < 0:
        return 0  # no negative market gap
    return remaining

def calculate_current_revenue(businesses):
    total_revenue = 0
    for item in businesses:
        total_revenue += item["revenue"]
    return total_revenue

def calculate_remaining_tam(tam, current_revenue):
    return tam - current_revenue
