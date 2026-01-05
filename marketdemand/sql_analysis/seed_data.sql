-- Cities
INSERT INTO cities (id, name, population, median_income) VALUES
  (1, 'Salt Lake City', 200000, 65000),
  (2, 'Provo',          115000, 60000),
  (3, 'Orem',            98000, 70000),
  (4, 'Lehi',            82000, 85000),
  (5, 'Sandy',           96000, 80000);

-- Industries
INSERT INTO industries (id, name, ideal_ppb, spend_per_capita) VALUES
  (1, 'Cafes',        2000, 350),
  (2, 'Pest Control', 15000, 45),
  (3, 'Fitness',      5000, 200),
  (4, 'Auto Repair',  7000, 300);

-- Businesses
INSERT INTO businesses (id, name, city_id, industry_id, annual_revenue) VALUES
  (1,  'Mountain Coffee Co.', 1, 1, 120000),
  (2,  'Sunrise Café',        5, 1,  95000),
  (3,  'Provo Beans & Brews', 2, 1, 110000),
  (4,  'Orem Java Spot',      3, 1,  90000),

  (5,  'Bee Gone Pest Control',   2, 2, 160000),
  (6,  'Salt Lake Pest Defense',  1, 2, 220000),
  (7,  'Utah Valley Exterminators',4,2, 150000),

  (8,  'Peak Fitness Gym',    3, 3, 140000),
  (9,  'Titan Fitness',       2, 3, 130000),

  (10, 'Top Gear Auto',       4, 4, 180000),
  (11, 'Riverton Auto Care',  5, 4, 170000);
