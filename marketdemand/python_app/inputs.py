def set_filter_options():
  """Collect basic filter options for the MVP."""
  num = int(input("How many results to display? "))
  industry = input("Industry: ").strip()
  city_input = input("Cities (comma separated, blank for all): ").strip()

  cities = [c.strip() for c in city_input.split(",")] if city_input else []

  sort_by = input("Sort by (1=name, 2=revenue, 3=industry, 4=distance): ").strip()
  sort_map = {
      "1": "business_name",
      "2": "revenue",
      "3": "industry",
      "4": "distance"
  }

  return {
      "num_to_display": num,
      "industry": industry,
      "cities": cities,
      "sort_by": sort_map.get(sort_by, "business_name")
  }