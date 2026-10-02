# Healthcare Underpayment Analysis

A personal portfolio project inspired by healthcare revenue cycle analysis. All records are synthetic. This project does not use employer or patient data.

## Business question
Which payers and denial categories account for the largest payment gaps, and which claims should an analyst review first?

## Run
Requires Python 3.9+; no external packages.

```bash
python analysis.py
```

Outputs: `data/claims.csv`, `output/claims.db`, `output/payer_summary.csv`, `output/review_queue.csv`, and `output/report.md`.

## Method
Generate 2,000 reproducible claims with a fixed random seed. Calculate signed payment variance as expected minus paid, and positive payment gap as the maximum of that variance and zero. Aggregate by payer and denial category; rank claims with positive gaps above $100 for manual review.

Inspect `queries.sql` for the SQL used by the analysis. The expected reimbursement is a simulated input, not a calculation from actual contracts.

## Interpretation and limits
A payment gap flags a case for review; it is not confirmed recoverable revenue. Pending adjustments, contract terms, timely filing, and claim status must be checked before pursuing recovery. Simulated findings do not measure job performance or employer results. The queue ranks by dollars only and does not model deadlines or effort.

## Next improvements
Add contract tables, multiple payments per claim, adjustment rules, filing deadlines, and a Power BI dashboard. Publish a dashboard only after it is implemented and validated.
