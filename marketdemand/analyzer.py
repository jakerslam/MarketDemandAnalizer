
# analyzer.py
import math

def analyze_market(business_data, population_data, filters, industry_params):
    """
    Main market analysis pipeline.
    business_data: filtered businesses (list of dicts)
    population_data: dict { "city": population }
    filters: contains industry + list of cities
    industry_params: dict:
        {
          "ideal_ppb": int,
          "spend_per_capita": int,
          "tam_weight": float
        }
    """

    # Extract industry parameters
    ideal_ppb = industry_params["ideal_ppb"]
    spend_per_capita = industry_params["spend_per_capita"]
    tam_weight = industry_params["tam_weight"]

    # ------------------------------------
    # 1. Aggregate population for selected cities
    # ------------------------------------
    cities = filters["cities"]
    total_population = aggregate_population(population_data, cities)

    # ------------------------------------
    # 2. Compute real people per business
    # ------------------------------------
    biz_count = len(business_data)
    real_ppb = calculate_real_ppb(total_population, biz_count)

    # ------------------------------------
    # 3. TAM calculations
    # ------------------------------------
    tam = calculate_tam(total_population, spend_per_capita)
    current_rev = calculate_current_revenue(business_data)
    remaining_tam = calculate_remaining_tam(tam, current_rev)
    remaining_pct = calculate_remaining_tam_pct(remaining_tam, tam)

    # ------------------------------------
    # 4. Competition + demand scoring
    # ------------------------------------
    competition_score = calculate_competition_score(real_ppb, ideal_ppb)
    demand_score = calc_demand_score(
        competition_score=competition_score,
        remaining_tam_pct=remaining_pct,
        tam_weight=tam_weight
    )

    # ------------------------------------
    # 5. Return all computed values
    # ------------------------------------
    return {
        "tam": tam,
        "current_revenue": current_rev,
        "remaining_tam": remaining_tam,
        "remaining_pct": remaining_pct,
        "competition_score": competition_score,
        "demand_score": demand_score,
        "population": total_population,
        "businesses": biz_count
    }


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def aggregate_population(pop_data, cities):
    """Sum population for selected cities. Blank → sum all."""
    if not cities:
        return sum(pop_data.values())

    total = 0
    for c in cities:
        total += pop_data.get(c, 0)
    return total


def calculate_real_ppb(population, biz_count):
    """People per business. Handles divide-by-zero."""
    if biz_count == 0:
        return float("inf")
    return population / biz_count


def calculate_tam(population, spend_per_capita):
    """Total addressable market = population * annual spending."""
    return population * spend_per_capita


def calculate_current_revenue(businesses):
    """Sum revenue from the filtered businesses."""
    return sum(b["revenue"] for b in businesses)


def calculate_remaining_tam(tam, current_revenue):
    """How much TAM is not yet served."""
    return max(tam - current_revenue, 0)


def calculate_remaining_tam_pct(remaining, tam):
    """Remaining TAM as percentage."""
    if tam == 0:
        return 1
    return remaining / tam


def calculate_competition_score(real_ppb, ideal_ppb):
    if ideal_ppb == 0:
        return float('inf')
    ratio = real_ppb / ideal_ppb
    # avoid log(0)
    if ratio <= 0:
        return -2  # extremely empty market
    return math.log(ratio, 2)


def calc_demand_score(competition_score, remaining_tam_pct, tam_weight=0.5):
    """
    Final demand score (0–100).
    Combines:
      • remaining TAM percentage
      • competition opportunity score (inverse of competition saturation)
    """
    # 1. Remaining TAM -> 0–100
    tam_score = remaining_tam_pct * 100
    # 2. Convert competition score (log base 2) into opportunity
    if competition_score == float("inf"):
        opp_score = 5  # maximum opportunity (no competitors)
    else:
        opp_score = max(0, 5 - competition_score)
    # 3. Normalize to 0–100
    opp_score_norm = (opp_score / 5) * 100
    # 4. Weighted blend
    demand_score = (tam_weight * tam_score) + ((1 - tam_weight) * opp_score_norm)
    return demand_score

