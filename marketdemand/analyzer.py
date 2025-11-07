

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
