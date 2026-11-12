-- Q6. Average bill per month and month-over-month change (CTE + LAG window function)
WITH monthly AS (
    SELECT month_no, month_name, ROUND(AVG(bill_amount), 0) AS avg_bill
    FROM monthly_statements
    GROUP BY month_no, month_name
)
SELECT month_name,
       avg_bill,
       avg_bill - LAG(avg_bill) OVER (ORDER BY month_no DESC) AS change_vs_previous_month
FROM monthly
ORDER BY month_no DESC;

-- Q7. Customers delayed 2+ months in September vs everyone else (CTE)
WITH latest AS (
    SELECT c.customer_id, c.defaulted,
           CASE WHEN s.pay_status >= 2 THEN 'Delayed 2+ months' ELSE 'Not seriously delayed' END AS grp
    FROM customers c
    JOIN monthly_statements s ON s.customer_id = c.customer_id AND s.month_no = 1
)
SELECT grp,
       COUNT(*)                          AS customers,
       ROUND(100.0 * AVG(defaulted), 2)  AS default_rate_pct
FROM latest
GROUP BY grp;

-- Q8. Credit utilisation (September bill / limit) and default rate
WITH util AS (
    SELECT c.customer_id, c.defaulted,
           1.0 * s.bill_amount / c.credit_limit AS utilisation
    FROM customers c
    JOIN monthly_statements s ON s.customer_id = c.customer_id AND s.month_no = 1
)
SELECT CASE WHEN utilisation <= 0    THEN '1. Zero or credit balance'
            WHEN utilisation < 0.3   THEN '2. Under 30%'
            WHEN utilisation < 0.7   THEN '3. 30%-70%'
            WHEN utilisation <= 1.0  THEN '4. 70%-100%'
            ELSE                          '5. Over limit' END AS utilisation_band,
       COUNT(*)                          AS customers,
       ROUND(100.0 * AVG(defaulted), 2)  AS default_rate_pct
FROM util
GROUP BY utilisation_band
ORDER BY utilisation_band;

-- Q9. Rank education groups by default rate (DENSE_RANK over a CTE)
WITH edu AS (
    SELECT e.education,
           COUNT(*)                           AS customers,
           ROUND(100.0 * AVG(c.defaulted), 2) AS default_rate_pct
    FROM customers c
    JOIN education_codes e ON c.education_code = e.education_code
    GROUP BY e.education
)
SELECT education, customers, default_rate_pct,
       DENSE_RANK() OVER (ORDER BY default_rate_pct DESC) AS risk_rank
FROM edu
ORDER BY risk_rank;
