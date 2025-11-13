# Overview

The **Market Demand Analyzer** is a modular Python project designed to practice real-world data analysis, aggregation, and statistical evaluation. As a software engineer, my goal with this project is to strengthen my ability to collect data, organize it into structured formats, and build analytical tools that provide useful insights across datasets.

This project uses combined datasets—business locations, demographic populations, and industry economic benchmarks—to explore how data can reveal **patterns in market opportunity, competition, and spending potential**. The software uses filtering, sorting, aggregation, and scoring models to answer meaningful business-related analytical questions.

The dataset used consists of:
- **Business Data** (JSON): city, industry, and estimated revenue  
- **Demographic Data** (JSON): population and average income  
- **Industry Data** (JSON): spend-per-capita, ideal population-per-business benchmarks, and weights for demand scoring  

These files simulate what a real API-driven dataset might look like once integrated with Yelp, Google Places, or U.S. Census endpoints.

The purpose of this project is to:
- Practice real data analysis through code  
- Demonstrate the ability to sort, filter, aggregate, and interpret datasets  
- Build a multi-factor scoring model (Demand Score)  
- Explore how software engineering can support entrepreneurship and market research  

### Demo Video  
[Software Demo Video](https://www.youtube.com/watch?v=qtUHCCfTMug)

---

# Data Analysis Results

The program answers two core analytical questions:

### **1. Which cities show the highest market opportunity for a given industry?**  
To answer this, the software:
- Filters businesses by city and industry  
- Aggregates population for selected areas  
- Calculates competition as *real people per business vs ideal people per business*  
- Computes Total Addressable Market (TAM)  
- Generates a **0–100 Demand Score**  

This allows identification of cities where demand is high and competition is low.

---

### **2. How well do current businesses capture the available revenue in a region?**  
To answer this, the program:
- Sums current revenue for all businesses in the selected region  
- Estimates expected revenue per business using weighted economic baselines  
- Compares expected vs actual revenue  
- Generates a **Revenue Opportunity Score (0–100)**  

This identifies markets where existing businesses significantly underperform relative to demand.

---

# Development Environment

**Tools Used**
- Visual Studio Code  
- Replit  
- GitHub for version control  
- Lucidchart for diagramming  

**Programming Language & Libraries**
- **Python 3.13**
  - `json` — data loading and storage  
  - `math` — logarithmic competition scoring  
  - Modular files:
    - `data_sources.py` — loads datasets & handles future API integration  
    - `analyzer.py` — core analytics (TAM, competition, revenue, demand score)  
    - `filtering.py` — business filtering logic  
    - `renderer.py` — CLI printing and upcoming bar-scale visualization  
    - `inputs.py` — user input interface  
    - `main.py` — orchestrates the pipeline  

---

# Useful Websites

* [Python JSON Documentation](https://docs.python.org/3/library/json.html)  
* [Python Math Library](https://docs.python.org/3/library/math.html)  
* [Pandas Documentation](https://pandas.pydata.org/docs/)  
* [U.S. Census API](https://www.census.gov/data/developers/data-sets.html)  
* [Yelp Fusion API](https://docs.developer.yelp.com/docs/fusion-intro)  

---

# Future Work

* Integrate real APIs (Yelp, Google Places, U.S. Census)  
* Replace static spend-per-capita with **income-weighted spend models**  
* Add **growth rate**, **migration**, and **seasonality** adjustments  
* Add CLI bar visualization for demand score  
* Build a web application using React or Django  
* Add automatic caching to reduce repeat API calls  

