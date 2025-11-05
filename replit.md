# Market Demand Analyzer

## Overview
A Python-based command-line tool for analyzing market demand across different cities and industries. The tool uses business data, demographic data, and industry baselines to calculate demand scores and identify market opportunities.

## Project Type
**Python CLI Application** - Interactive command-line interface for data analysis

## Current State
- **Status**: Fully functional CLI application
- **Language**: Python 3.11
- **Dependencies**: None (uses only Python standard library)
- **Last Updated**: 2025-11-05 (Replit import setup)

## Project Structure
```
marketdemand/
├── __init__.py
├── main.py           # Main CLI interface and display logic
├── analyzer.py       # Market demand analysis functions
├── data_sources.py   # Data loading utilities
├── data_storage.py   # Data persistence layer
└── utils.py          # Helper utilities

data/
├── sample_business_data.json      # Business listings with revenue
├── sample_demographic_data.json   # City population data
├── industry_baselines.json        # Ideal people-per-business ratios
└── industry_spend_per_capita.json # Industry spending data

data_cache/
├── business_spend_cache.json
├── census_cache.json
├── google_places_cache.json
└── yelp_cache.json

tests/
└── test_analyzer.py
```

## How to Run
The application is launched via the workflow:
```bash
cd marketdemand && python main.py
```

The interactive CLI will prompt for:
1. Number of results to display
2. Sort method (business name, revenue, industry, or distance)
3. City filter
4. Industry filter
5. Whether to display the filtered data

## Features
- **Market Demand Analysis**: Calculates demand scores based on people-per-business ratios
- **Multi-City Support**: Analyzes Utah cities (Salt Lake City, Provo, Orem, Logan, St. George, etc.)
- **Industry Coverage**: Cafes, Fitness, Auto Repair, Dentistry, Landscaping, Childcare, Tech IT Services, Real Estate, Pest Control
- **Filtering & Sorting**: Filter by city/industry, sort by various criteria
- **Market Ratings**: Classifies markets as Blue Ocean, High Opportunity, Moderate, Crowded, or Saturated

## Market Demand Score Formula
```
Demand Score = (Real People per Business) / (Ideal People per Business)

Ratings:
- Infinite: No competition yet ✅ (blue ocean)
- > 3x: High Opportunity ✅
- > 1x: Moderate Opportunity ⚠️
- > 0.5x: Crowded 🟠
- < 0.5x: Saturated ❌
```

## Planned Expansion
According to readme.md:
- `/frontend/` — React dashboard for viewing and filtering analysis results
- `/node_api/` — Express backend to handle user queries and connect to the Python analyzer

## Architecture Notes
- Pure Python implementation with no external dependencies
- JSON-based data storage for business, demographic, and baseline data
- Modular design with separation between data sources, analysis, and presentation
- Cache directory suggests future API integration capability

## Recent Changes
- **2025-11-05**: Replit environment setup
  - Installed Python 3.11
  - Created requirements.txt (no external dependencies)
  - Configured workflow for CLI application
  - Created project documentation
