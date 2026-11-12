-- Q1. Overall default rate
SELECT COUNT(*)                          AS customers,
       SUM(defaulted)                    AS defaulters,
       ROUND(100.0 * AVG(defaulted), 2)  AS default_rate_pct
FROM customers;

-- Q2. Default rate by education (JOIN to the lookup table)
SELECT e.education,
       COUNT(*)                          AS customers,
       ROUND(100.0 * AVG(c.defaulted), 2) AS default_rate_pct
FROM customers c
JOIN education_codes e ON c.education_code = e.education_code
GROUP BY e.education
ORDER BY default_rate_pct DESC;

-- Q3. Default rate by age band
SELECT CASE WHEN age < 30 THEN '1. Under 30'
            WHEN age < 40 THEN '2. 30-39'
            WHEN age < 50 THEN '3. 40-49'
            ELSE               '4. 50 and over' END AS age_band,
       COUNT(*)                          AS customers,
       ROUND(100.0 * AVG(defaulted), 2)  AS default_rate_pct
FROM customers
GROUP BY age_band
ORDER BY age_band;

-- Q4. Default rate by credit limit band
SELECT CASE WHEN credit_limit < 50000   THEN '1. Under 50k'
            WHEN credit_limit < 150000  THEN '2. 50k-150k'
            WHEN credit_limit < 300000  THEN '3. 150k-300k'
            ELSE                             '4. 300k and over' END AS limit_band,
       COUNT(*)                          AS customers,
       ROUND(100.0 * AVG(defaulted), 2)  AS default_rate_pct
FROM customers
GROUP BY limit_band
ORDER BY limit_band;

-- Q5. Default rate by latest repayment status (September), groups with 100+ customers only
SELECT s.pay_status,
       p.pay_label,
       COUNT(*)                          AS customers,
       ROUND(100.0 * AVG(c.defaulted), 2) AS default_rate_pct
FROM monthly_statements s
JOIN customers c        ON s.customer_id = c.customer_id
JOIN pay_status_codes p ON s.pay_status = p.pay_status
WHERE s.month_no = 1
GROUP BY s.pay_status, p.pay_label
HAVING COUNT(*) >= 100
ORDER BY s.pay_status;
