# RESUME_BULLETS: UPI 360

Every figure comes from KEY_METRICS.md. Check each one against the dashboard before use.

## Resume bullets

- Built an end-to-end analytics pipeline on 114 months of NPCI UPI statistics (Apr 2017 to Sep 2026): pandas cleaning, a DuckDB warehouse and 10 SQL queries using CTEs and window functions, surfacing a 137% volume CAGR and growth slowing from 225% (2019 avg YoY) to 25% (last 12 months).
- Found that average UPI ticket size fell 61% (Rs 3,154 to Rs 1,220) while monthly volume reached 24,068M transactions, showing growth driven by small payments.
- Benchmarked three forecasting models on a 6-month holdout; drift_12m reached 2.20% MAPE against 3.65% for a naive baseline, then produced a 6-month forecast with an uncertainty band.
- Detrended the series to test seasonality: Oct-Dec runs 7.5% above the rest of the year (Mann-Whitney p < 0.001); naive month averages hid this because of the growth trend.
- Used Isolation Forest on detrended growth and ticket size to flag 6 unusual months, including the April and May 2020 lockdown dip and rebound.
- Shipped an interactive 4-view dashboard (market, behaviour, risk, ask-the-data) with date-range filters, deployed publicly.

## LinkedIn summary

UPI 360 analyses 114 months of India's UPI statistics with SQL, Python and DuckDB: growth, seasonality, ticket-size trends, a holdout-tested forecast and anomaly detection, delivered as an interactive dashboard.
