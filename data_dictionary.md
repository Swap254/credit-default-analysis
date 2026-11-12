# Data Dictionary

**Source:** UCI Machine Learning Repository, "Default of Credit Card Clients" (Yeh, I-Cheng, 2009).
Credit card customers of a bank in Taiwan, April to September 2005. 30,000 rows, one per customer.
Download: https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
The raw file is not stored in this repository. Download it and place it in `data/raw/`.

## Original columns

| Column | Meaning |
|---|---|
| ID | Customer ID |
| LIMIT_BAL | Credit limit given (NT dollars) |
| SEX | 1 = male, 2 = female |
| EDUCATION | 1 = graduate school, 2 = university, 3 = high school, 4 = others |
| MARRIAGE | 1 = married, 2 = single, 3 = others |
| AGE | Age in years |
| PAY_0, PAY_2 ... PAY_6 | Repayment status for September (PAY_0) back to April (PAY_6). Note: there is no PAY_1 |
| BILL_AMT1 ... BILL_AMT6 | Bill statement amount for September (1) back to April (6) |
| PAY_AMT1 ... PAY_AMT6 | Amount paid in September (1) back to April (6) |
| default payment next month | Target: 1 = defaulted in October 2005, 0 = did not |

## Repayment status values
-1 = paid in full, 1 = payment delayed one month, 2 = delayed two months, and so on up to 8.
The values **-2 and 0 are not described in the official documentation**. They are commonly interpreted as
-2 = no credit use that month and 0 = paid the minimum on revolving credit. This project uses that
interpretation and states it as an assumption.

## Data quality notes found in this project
- No missing values.
- EDUCATION contains codes 0, 5 and 6 that are not documented (345 customers). Merged into "Others" (4).
- MARRIAGE contains code 0 that is not documented (54 customers). Merged into "Others" (3).
- 35 rows are identical except for ID. They have different IDs, so they may be genuine different customers. They are kept and flagged.
- Some bill amounts are negative (customer overpaid or has a credit). They are kept, because they are valid.
