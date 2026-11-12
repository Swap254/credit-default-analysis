# Insights Summary: Credit Card Default Risk

*Written for a business manager. Data: UCI "Default of Credit Card Clients" (30,000 customers, Taiwan, April to September 2005). Public data, personal project.*

## The question
Which customers are most likely to default next month, and what should the lender do about it?

## The short answer
**Missed payments are the clearest warning sign.** Customers who were 2 or more months late in September defaulted 69.55% of the time. Customers who were on time defaulted 13.83% of the time. The overall default rate is 22.12%.

## What the data shows

1. **Late payers are a small group with a big share of the problem.** Customers 1 or more months late in September are 22.7% of all customers but 51.7% of all defaulters. Their default rate is 50.29%, against 13.83% for everyone else. The gap is far too big to be chance (two-proportion z-test, p-value close to 0).
2. **The risk jumps at the second missed month.** Default rate is about 13% for on-time customers, 34% at 1 month late and 69% at 2 months late.
3. **Lower credit limits default more.** The rate falls steadily as the limit rises: 36.1% under 50k, 26.0% for 50k to 99k, 20.8% for 100k to 199k, 16.4% for 200k to 299k and 13.7% for 300k and above.
4. **A high credit limit does not protect a late payer.** Late payers with an above-average limit still defaulted at 68.95%, about the same as late payers overall.
5. **Bills are growing.** The average monthly bill rose every month, from 38,872 in April to 51,223 in September, so exposure is increasing.

## What I would recommend
- **Watch anyone 1 month late and act on anyone 2 months late.** Reminders, a call or a payment plan are cheaper than a default.
- **Be careful with low limits for customers with weak repayment history.**
- **Treat high utilisation as a secondary signal.** It matters much less than late payment.
- **Use these rules as a screening list, not a final decision.** A human should review before any action on a customer.

## What the data cannot tell us
- 31.8% of defaulters were "On track" in September, so simple rules miss many defaulters. A predictive model could do better; I have not built one.
- The data is one bank, one country and 6 months from 2005. It may not describe other lenders or today's customers.
- Correlation is not causation. Late payment goes with default, but the data does not prove it causes default.
- Repayment codes -2 and 0 are not documented. I assumed -2 = no credit use and 0 = paid the minimum.
- Groups with 5 or more months of delay are tiny (9 to 26 customers each), so I do not draw conclusions from them.

## Next steps if this were a real project
1. Test the late-payment rule on a newer period of data.
2. Build a simple prediction model (for example logistic regression) and compare it with these rules.
3. Add customer income and transaction data, if available.
