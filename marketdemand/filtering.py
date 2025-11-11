def filter_businesses(business_data, filters):
  """Filter by cities + industry."""
  cities = filters["cities"]
  industry = filters["industry"]

  filtered = []
  for b in business_data:
      city_ok = (not cities) or (b["city"].lower() in [c.lower() for c in cities])
      industry_ok = (not industry) or (b["industry"].lower() == industry.lower())

      if city_ok and industry_ok:
          filtered.append(b)

  return filtered


def sort_businesses(data, filters):
  """Sort based on user’s selected field."""
  sort_by = filters["sort_by"]

  # NOTE: removed `display_options`, but 
  #       may re-add display toggles later if you want to show/hide revenue, industry, etc.
  # display_options = { "revenue": False, "industry": False }

  if sort_by == "revenue":
      return sorted(data, key=lambda x: x["revenue"], reverse=True)

  elif sort_by == "industry":
      return sorted(data, key=lambda x: x["industry"].lower())

  elif sort_by == "business_name":
      return sorted(data, key=lambda x: x["business_name"].lower())

  elif sort_by == "distance":
      print("** distance sort not implemented **")
      return data

  return data

