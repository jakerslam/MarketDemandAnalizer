

def render_results(business_list, analysis):
    """Prints both the business results and the market analysis summary."""
    render_business_list(business_list)

    print("\n=== MARKET ANALYSIS ===")
    print(f"Population: {analysis['population']}")
    print(f"TAM: ${analysis['tam']:,}")
    print(f"Current Revenue: ${analysis['current_revenue']:,}")
    print(f"Remaining TAM: ${analysis['remaining_tam']:,}")
    print(f"Remaining TAM %: {analysis['remaining_pct']*100:.2f}%")
    print(f"Competition Score: {analysis['competition_score']:.2f}")
    print(f"Demand Score: {analysis['demand_score']:.2f}")
    classify_market(analysis["demand_score"])

def classify_market(score):
    if score == float("inf"):
        return "blue ocean of opportunity✅"
    if score > 80:
        return "High Opportunity ✅"
    elif score > 50:
        return "Moderate Opportunity ⚠️"
    elif score < 50:
        return "Crowded 🟠"
    else:
        return "Saturated ❌"
    
def render_business_list(business_list):
    print("\n=== BUSINESS RESULTS ===")
    for b in business_list:
        print(f"{b['business_name']} — {b['city']} — {b['industry']} — ${b['revenue']}")

