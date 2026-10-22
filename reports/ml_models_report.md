# ML Models Report

All results computed on the full series: 114 months, Apr 2017 to Sep 2026.

## 1. Forecast (holdout: train to Mar 2026, test Apr 2026 to Sep 2026)

| Model | Holdout MAPE |
|---|---|
| naive | 3.65% |
| drift_12m (selected) | 2.20% |
| ets_damped_log | 2.48% |

Selected model refit on all data. Next 6 months (approx. 80% band from recent volatility):

| Month | Forecast (M txns) | Low | High |
|---|---|---|---|
| Oct 2026 | 24,438 | 22,848 | 26,138 |
| Nov 2026 | 24,808 | 22,556 | 27,283 |
| Dec 2026 | 25,177 | 22,408 | 28,288 |
| Jan 2027 | 25,547 | 22,331 | 29,226 |
| Feb 2027 | 25,916 | 22,297 | 30,123 |
| Mar 2027 | 26,286 | 22,293 | 30,994 |

## 2. Seasonality (detrended: ratio to centred 12-month average)

- Highest month index: 12 (1.104); lowest: 6 (0.948)
- Oct-Dec vs rest, Mann-Whitney p = 0.0000 (festive mean 1.073 vs 0.999)

## 3. Growth phases (K-means k=3 on log volume)

| Phase | Months | Period | Avg volume (M) | Avg ticket (Rs) |
|---|---|---|---|---|
| Launch & ramp-up | 15 | Apr 2017 to Jun 2018 | 102.7 | 1,823 |
| Scale-up | 39 | Jul 2018 to Sep 2021 | 1,488.7 | 1,760 |
| Mature | 60 | Oct 2021 to Sep 2026 | 13,506.4 | 1,488 |

## 4. Anomalies (Isolation Forest, contamination 6%, 101 months scored from May 2018)

Features: deviation of month-on-month volume growth and of ticket-size change from their trailing 12-month median.

| Month | Volume (M) | MoM % | Trend MoM % | Score |
|---|---|---|---|---|
| May 2018 | 189 | -0.3 | +21.1 | 0.746 |
| Sep 2018 | 406 | +30.1 | +13.4 | 0.736 |
| May 2020 | 1,234 | +23.5 | +3.4 | 0.734 |
| Apr 2020 | 1,000 | -19.8 | +3.4 | 0.718 |
| May 2019 | 734 | -6.2 | +12.5 | 0.647 |
| Jul 2018 | 274 | +11.1 | +21.2 | 0.611 |
