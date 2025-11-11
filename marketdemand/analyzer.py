# analyzer.py
import math

def analyze_market(business_data, population_data, filters, industry_params):
    """
    Main market analysis pipeline.
    business_data: filtered businesses (list of dicts)
    population_data: dict {city: population}
    filters: contains industry + list of cities
    industry_params: dict:
        {
          "ideal_ppb": int,
          "spend_per_capita": int,
          "tam_weight": float,
          "rev_weight": float (optional)
        }
    """

    # Extract industry parameters
    ideal_ppb = industry_params["ideal_ppb"]
    spend_per_capita = industry_params["spend_per_capita"]
    tam_weight = industry_params.get("tam_weight", 0.5)
    rev_weight = industry_params.get("rev_weight", 0.2)

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
    # 4. Competition normalization
    # ------------------------------------
    competition_log = calculate_competition_score(real_ppb, ideal_ppb)
    competition_norm_0_100 = normalize_competition_to_0_100(competition_log)

    # ------------------------------------
    # 5. Revenue benchmarking
    # ------------------------------------
    expected_per_biz = calculate_expected_revenue_per_business(
        population=total_population,
        ideal_ppb=ideal_ppb,
        tam=tam
    )
    actual_per_biz = calculate_actual_revenue_per_business(
        current_rev=current_rev,
        biz_count=biz_count
    )
    rev_opp_score = calculate_revenue_gap_score(
        expected=expected_per_biz,
        actual=actual_per_biz
    )

    # ------------------------------------
    # 6. Final demand score (0–100)
    # ------------------------------------
    demand_score = calc_demand_score(
        competition_norm_0_100=competition_norm_0_100,
        remaining_tam_pct=remaining_pct,
        rev_opp_score=rev_opp_score,
        tam_weight=tam_weight,
        rev_weight=rev_weight
    )

    # ------------------------------------
    # 7. Return all computed values
    # ------------------------------------
    return {
        "tam": tam,
        "current_revenue": current_rev,
        "remaining_tam": remaining_tam,
        "remaining_pct": remaining_pct,
        "competition_score": competition_log,
        "competition_norm": competition_norm_0_100,
        "rev_opp_score": rev_opp_score,
        "demand_score": demand_score,
        "population": total_population,
        "businesses": biz_count
    }



# ============================================================
# POPULATION + BASIC MATH
# ============================================================

def aggregate_population(pop_data, cities):
    """Sum population for selected cities (case-insensitive)."""
    if not cities:
        return sum(pop_data.values())

    total = 0
    by_lower = {k.strip().lower(): v for k, v in pop_data.items()}

    for c in cities:
        key = (c or "").strip().lower()
        total += by_lower.get(key, 0)

    return total


def calculate_real_ppb(population, biz_count):
    """People per business."""
    if biz_count == 0:
        return float("inf")
    return population / biz_count


def calculate_tam(population, spend_per_capita):
    """Total addressable market."""
    return population * spend_per_capita


def calculate_current_revenue(businesses):
    """Sum revenue across all businesses."""
    return sum(b["revenue"] for b in businesses)



# ============================================================
# TAM REMAINING
# ============================================================

def calculate_remaining_tam(tam, current_revenue):
    return max(0, tam - current_revenue)


def calculate_remaining_tam_pct(remaining, tam):
    if tam <= 0:
        return 0.0
    return remaining / tam



# ============================================================
# COMPETITION (log scale)
# ============================================================

def calculate_competition_score(real_ppb, ideal_ppb):
    """log2(real/ideal). Negative = crowded, positive = open."""
    if ideal_ppb == 0:
        return float("inf")

    ratio = real_ppb / ideal_ppb

    if ratio <= 0:
        return -10  # extreme crowding protection

    return math.log(ratio, 2)


def normalize_competition_to_0_100(log_score, low=-2.0, high=2.0):
    """
    Convert log competition score into a 0–100 opportunity score.
    low  = saturated (0)
    high = extremely open (100)
    """
    if log_score == float("inf"):
        return 100.0

    # clamp into range
    s = max(low, min(high, log_score))

    return ((s - low) / (high - low)) * 100.0



# ============================================================
# REVENUE BENCHMARKING
# ============================================================

def calculate_expected_revenue_per_business(population, ideal_ppb, tam):
    """Expected rev per business in balanced market."""
    if ideal_ppb == 0:
        return 0

    ideal_business_count = population / ideal_ppb
    if ideal_business_count <= 0:
        return 0

    return tam / ideal_business_count


def calculate_actual_revenue_per_business(current_rev, biz_count):
    """Actual rev per business."""
    if biz_count == 0:
        return 0
    return current_rev / biz_count


def calculate_revenue_gap_score(expected, actual):
    """
    Revenue opportunity score: 0–100.
    Positive gap = opportunity.
    """
    if expected <= 0:
        return 0

    gap = expected - actual
    gap_pct = gap / expected

    if gap_pct <= 0:
        return 0
    if gap_pct >= 1:
        return 100

    return gap_pct * 100



# ============================================================
# FINAL DEMAND SCORE (0–100)
# ============================================================

def calc_demand_score(
    competition_norm_0_100,
    remaining_tam_pct,
    rev_opp_score,
    tam_weight=0.5,
    rev_weight=0.2
):
    """
    Final demand score (0–100).
    Combines:
      TAM opportunity (0–100)
      Competition opportunity (0–100)
      Revenue gap opportunity (0–100)
    """

    tam_score = max(0.0, min(100.0, remaining_tam_pct * 100))
    comp_score = max(0.0, min(100.0, competition_norm_0_100))
    rev_score = max(0.0, min(100.0, rev_opp_score))

    comp_weight = 1.0 - tam_weight - rev_weight
    comp_weight = max(0.0, comp_weight)

    demand = (
        (tam_weight * tam_score) +
        (comp_weight * comp_score) +
        (rev_weight * rev_score)
    )

    return max(0.0, min(100.0, demand))
