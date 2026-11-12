-- Q10. Education groups with a default rate ABOVE the overall rate (HAVING + subquery)
SELECT e.education,
       COUNT(*)                           AS customers,
       ROUND(100.0 * AVG(c.defaulted), 2) AS default_rate_pct
FROM customers c
JOIN education_codes e ON c.education_code = e.education_code
GROUP BY e.education
HAVING AVG(c.defaulted) > (SELECT AVG(defaulted) FROM customers)
ORDER BY default_rate_pct DESC;

-- Q11. Late payers (2+ months in September) who have an above-average credit limit (subquery in WHERE)
SELECT COUNT(*)                           AS customers,
       ROUND(100.0 * AVG(c.defaulted), 2) AS default_rate_pct
FROM customers c
JOIN monthly_statements s ON s.customer_id = c.customer_id AND s.month_no = 1
WHERE s.pay_status >= 2
  AND c.credit_limit > (SELECT AVG(credit_limit) FROM customers);

-- Q12. Duplicate check: customer IDs that appear more than once (an empty result is the good answer)
SELECT customer_id, COUNT(*) AS times_seen
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- Q13. Stack three summary rows with UNION ALL: everyone, late in September, not late
SELECT 'All customers' AS grp,
       COUNT(*)                           AS customers,
       ROUND(100.0 * AVG(defaulted), 2)   AS default_rate_pct
FROM customers
UNION ALL
SELECT 'Late in September',
       COUNT(*),
       ROUND(100.0 * AVG(c.defaulted), 2)
FROM customers c
JOIN monthly_statements s ON s.customer_id = c.customer_id AND s.month_no = 1
WHERE s.pay_status >= 1
UNION ALL
SELECT 'Not late in September',
       COUNT(*),
       ROUND(100.0 * AVG(c.defaulted), 2)
FROM customers c
JOIN monthly_statements s ON s.customer_id = c.customer_id AND s.month_no = 1
WHERE s.pay_status <= 0;

-- Q14. Top 5 customers by September bill (the kit's "top 5 customers" pattern)
SELECT c.customer_id, s.bill_amount, c.defaulted
FROM customers c
JOIN monthly_statements s ON s.customer_id = c.customer_id AND s.month_no = 1
ORDER BY s.bill_amount DESC
LIMIT 5;

-- Q15. Second highest credit limit (the kit's "second highest salary" pattern)
SELECT MAX(credit_limit) AS second_highest_limit
FROM customers
WHERE credit_limit < (SELECT MAX(credit_limit) FROM customers);

-- Q16. Highest September bill inside each education group (CTE + DENSE_RANK with PARTITION BY)
WITH ranked AS (
    SELECT e.education, c.customer_id, s.bill_amount,
           DENSE_RANK() OVER (PARTITION BY e.education ORDER BY s.bill_amount DESC) AS rnk
    FROM customers c
    JOIN education_codes e ON c.education_code = e.education_code
    JOIN monthly_statements s ON s.customer_id = c.customer_id AND s.month_no = 1
)
SELECT education, customer_id, bill_amount
FROM ranked
WHERE rnk = 1
ORDER BY education;
