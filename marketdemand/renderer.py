

def render_results(business_list, analysis):
    """Prints both the business results and the market analysis summary."""
    render_business_list(business_list)

    print("\n=== MARKET ANALYSIS ===")
    
    print(f"Population: {analysis['population']}")
    print(f"TAM: ${analysis['tam']:,}")
    print(f"Current Revenue: ${analysis['current_revenue']:,}")
    print(f"Remaining TAM: ${analysis['remaining_tam']:,}")
    print(f"Competition Score: {analysis['competition_score']:.2f}x")
    render_bar(analysis["remaining_pct"] * 100, "TAM Remaining")
    render_bar(analysis["confidence_score"], "Confidence Index")
    render_bar(analysis["demand_score"], "Demand Score")
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

def render_bar(value, label, width=25, color=True):
    """
    Render a horizontal bar (0–100%) with optional ANSI color.
    Example: Demand Score: 73.5% ███████████░░░░░░░░░
    """
    # Clamp value
    value = max(0, min(100, value))

    # Calculate filled and empty segments
    filled = int((value / 100) * width)
    empty = width - filled
    bar = "█" * filled + "░" * empty

    # Determine color
    if color:
        if value >= 70:
            color_code = "\033[92m"  # Green
        elif value >= 40:
            color_code = "\033[93m"  # Yellow
        else:
            color_code = "\033[91m"  # Red
        reset = "\033[0m"
        bar_colored = f"{color_code}{bar}{reset}"
    else:
        bar_colored = bar

    # Print formatted line
    print(f"{label:<18} {value:6.1f}%  {bar_colored}")

