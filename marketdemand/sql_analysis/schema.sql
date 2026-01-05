
CREATE TABLE cities (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  population INTEGER NOT NULL,
  median_income INTEGER
);

CREATE TABLE industries (
  id INTEGER PRIMARY KEY, 
  name TEXT NOT NULL UNIQUE,
  ideal_ppb INTEGER,
  spend_per_capita INTEGER,
  tam_weight REAL,

  FOREIGN KEY (city_id) REFERENCES cities(id),
  FOREIGN KEY (industry_id) REFERENCES industries(id)
);