# renderer.py
def render_bar(value, label, width=25, color=True):
    """
    Render a horizontal bar (0–100%) with color and qualitative label.
    Example: Demand Score: 73.5% ███████████░░░░░░░░░ (High)
    """
    value = max(0, min(100, value))
    filled = int((value / 100) * width)
    empty = width - filled
    bar = "█" * filled + "░" * empty

    # Classification + color
    if value >= 70:
        status = "High"
        color_code = "\033[92m"  # green
    elif value >= 40:
        status = "Moderate"
        color_code = "\033[93m"  # yellow
    else:
        status = "Low"
        color_code = "\033[91m"  # red

    reset = "\033[0m"
    bar_colored = f"{color_code}{bar}{reset}" if color else bar
    print(f"{label:<18} {value:6.1f}%  {bar_colored}  ({status})")


def render_results(business_list, analysis):
    """
    Dashboard-style results display.
    """
    print("\n=== BUSINESS RESULTS ===")
    for b in business_list:
        rev = b.get("revenue")
        rev_str = f"${rev:,.0f}" if isinstance(rev, (int, float)) else "N/A"
        print(f"{b.get('business_name','')} — {b.get('city','')} — {b.get('industry','')} — {rev_str}")


    print("\n=== MARKET ANALYSIS DASHBOARD ===")
    print("-" * 60)

    render_bar(analysis["demand_score"], "Demand Score")
    render_bar(analysis["confidence_score"], "Confidence Index")
    render_bar(analysis["remaining_pct"] * 100, "TAM Remaining")

    print("-" * 60)
    print(f"Population: {analysis['population']:,}  |  Businesses: {analysis['businesses']}")
    tam = round(analysis['tam'], 0)
    print(f"TAM: ${tam:,}  |  Current Revenue: ${analysis['current_revenue']:,}")
    remaining_tam = round(analysis['remaining_tam'], 0)
    print(f"Remaining TAM: ${remaining_tam:,}  ({analysis['remaining_pct']*100:.2f}%)")
    print()
