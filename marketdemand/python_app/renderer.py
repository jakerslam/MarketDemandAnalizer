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
        print(f"{b['business_name']} — {b['city']} — {b['industry']} — ${b['revenue']:,}")

    print("\n=== MARKET ANALYSIS DASHBOARD ===")
    print("-" * 60)

    render_bar(analysis["demand_score"], "Demand Score")
    render_bar(analysis["confidence_score"], "Confidence Index")
    render_bar(analysis["remaining_pct"] * 100, "TAM Remaining")

    print("-" * 60)
    print(f"Population: {analysis['population']:,}  |  Businesses: {analysis['businesses']}")
    print(f"TAM: ${analysis['tam']:,}  |  Current Revenue: ${analysis['current_revenue']:,}")
    print(f"Remaining TAM: ${analysis['remaining_tam']:,}  ({analysis['remaining_pct']*100:.2f}%)")
    print()
