# Market Demand Analyzer — Calculation Notes

## 1) Goal
Estimate market opportunity for an industry in one or more Utah cities using:
- Demographics (population, income)
- Competitive density (business count)
- Revenue benchmarking (when available)

This is a heuristic scoring model intended for directional guidance, not a financial forecast.

## 2) Data Inputs

### 2.1 Demographics (per city)
- population: int (people)
- avg_income: int (median household income in USD)

Source: Census ACS 5-year (Utah places), normalized keys (e.g., "Provo city" → "provo").

### 2.2 Businesses (per row)
- business_name: str
- city: str
- industry: str
- revenue: int | float | None (USD/year)
- rating: float | None
- user_ratings_total: int | None

Note: If revenue is missing, revenue-based outputs may be 0 or de-emphasized.

### 2.3 Industry parameters (per industry)
- ideal_ppb: int (ideal people-per-business; higher means fewer businesses supported)
- spend_per_capita: float (USD/person/year baseline)
- income_elasticity: float (dimensionless; used only when dynamic SPC enabled)
- tam_weight: float (0–1)
- rev_weight: float (0–1)

## 3) Normalization / Matching Rules
- City keys lowercased; Census suffixes removed: city/town/cdp/metro township/village
- Industry keys lowercased
- Invalid income values (<=0 or extremely large) dropped during ingestion
- Missing revenue treated as 0 in totals (skipped)

## 4) Core Calculations

### 4.1 Population aggregation
For selected cities:
total_population = sum(population[city])

### 4.2 Weighted income
weighted_income = sum(avg_income[city] * population[city]) / total_population

### 4.3 Real people-per-business (PPB)
real_ppb = total_population / business_count
If business_count == 0 → real_ppb = inf

### 4.4 Total Addressable Market (TAM)
tam = total_population * spend_per_capita
Units: USD/year

### 4.5 Current revenue
current_revenue = sum(revenue_i) for all businesses with numeric revenue

### 4.6 Remaining TAM
remaining_tam = max(0, tam - current_revenue)
remaining_pct = remaining_tam / tam (if tam > 0 else 0)

### 4.7 Competition score (log scale)
competition_log = log2(real_ppb / ideal_ppb)
Interpretation:
- Negative → crowded (real_ppb < ideal_ppb)
- Positive → undersupplied (real_ppb > ideal_ppb)

### 4.8 Competition normalized 0–100
Clamp competition_log to [-2, +2], then linear-map to [0,100].

### 4.9 Expected revenue per business (balanced market)
ideal_business_count = total_population / ideal_ppb
expected_per_biz = tam / ideal_business_count

### 4.10 Actual revenue per business
actual_per_biz = current_revenue / business_count (if business_count > 0 else 0)

### 4.11 Revenue gap score (0–100)
gap_pct = (expected_per_biz - actual_per_biz) / expected_per_biz
rev_opp_score = clamp(gap_pct, 0..1) * 100

### 4.12 Final demand score (0–100)
tam_score = remaining_pct * 100
comp_score = competition_norm_0_100
rev_score = rev_opp_score

comp_weight = max(0, 1 - tam_weight - rev_weight)

demand_score = tam_weight*tam_score + comp_weight*comp_score + rev_weight*rev_score

### 4.13 Confidence index (0–100)
confidence = log1p(business_count) / log1p(15) * 100, capped at 100.

## 5) Optional: Dynamic Spend Per Capita (experimental)
If enabled:
dynamic_spc = base_spend * (weighted_income/benchmark_income)^income_elasticity * competition_multiplier
benchmark_income = 60000
competition_multiplier = clamp(1/(real_ppb/ideal_ppb), 0.6..1.5)

Note: Including competition inside TAM is a modeling choice and may be revised.

## 6) Known Limitations / Future Work
- Places API provides business counts but not revenue
- income is median household, not category-specific spend capacity
- spend_per_capita baselines are heuristic and require calibration
- future: NAICS mapping + CBP establishment counts + regression calibration for elasticities
