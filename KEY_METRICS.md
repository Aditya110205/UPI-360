# KEY_METRICS: UPI 360 Analytics

All headline numbers with source queries or scripts.

---

## Market Growth

| Metric | Value | Source | Query/Script |
|--------|-------|--------|--------------|
| **Initial Volume (Apr 2017)** | 7.2M transactions | Raw data | `SELECT volume_mn FROM upi_monthly WHERE date = '2017-04-01'` |
| **Latest Volume (Sep 2026)** | 23,202M transactions | Raw data | `SELECT volume_mn FROM upi_monthly WHERE date = '2026-09-01'` |
| **Total Growth** | 322,150% | Computed | `((23202 - 7.2) / 7.2) * 100` |
| **Peak Volume** | 23,202M (Sep 2026) | Time-series | `SELECT MAX(volume_mn) as peak FROM upi_monthly` |
| **Minimum Volume** | 7.2M (Apr 2017) | Time-series | `SELECT MIN(volume_mn) as min FROM upi_monthly` |
| **Concentration Range** | 322,149% | Volatility | `((MAX - MIN) / MIN) * 100` |
| **Coefficient of Variation** | 108.3% | Volatility | `STDDEV / MEAN` over all months |

---

## Bank Network

| Metric | Value | Source | Query/Script |
|--------|-------|--------|--------------|
| **Banks at Start (Apr 2017)** | 48 | Raw data | `SELECT num_banks FROM upi_monthly WHERE date = '2017-04-01'` |
| **Banks at End (Sep 2026)** | 756 | Raw data | `SELECT num_banks FROM upi_monthly WHERE date = '2026-09-01'` |
| **Bank Growth** | 1,475% | Computed | `((756 - 48) / 48) * 100` |
| **Avg Banks Across Period** | 348 | Statistics | `SELECT AVG(num_banks) FROM upi_monthly` |

---

## Seasonality

| Metric | Value | Source | Query/Script |
|--------|-------|--------|--------------|
| **Peak Month** | May | EDA | `SELECT month, AVG(volume_mn) FROM upi_monthly GROUP BY EXTRACT(MONTH FROM date) ORDER BY AVG DESC LIMIT 1` |
| **Peak Month Avg** | 6,368M | EDA | Average volume in May |
| **Trough Month** | April | EDA | `SELECT month, AVG(volume_mn) FROM upi_monthly GROUP BY EXTRACT(MONTH FROM date) ORDER BY AVG ASC LIMIT 1` |
| **Trough Month Avg** | 4,046M | EDA | Average volume in April |
| **Festive vs Non-Festive (t-test p-value)** | 0.6844 | Hypothesis test | No significant difference |
| **Festive Months Avg** | 5,023M | EDA | Oct, Nov, Dec, Mar, Apr average |
| **Non-Festive Months Avg** | 5,510M | EDA | Remaining months average |

---

## Growth Phases

| Metric | Value | Period | Query/Script |
|--------|-------|--------|--------------|
| **Early YoY Growth** | 225.1% | 2019 | `SELECT AVG(pct_change(volume_mn, 12)) FROM upi_monthly WHERE YEAR(date) = 2019` |
| **Recent YoY Growth** | 36.2% | Sep 2025 - Sep 2026 | `SELECT AVG(pct_change(volume_mn, 12)) FROM upi_monthly WHERE date >= '2025-09-01'` |
| **Growth Deceleration** | 188.9pp | 2019 vs Recent | `225.1 - 36.2 = 188.9 percentage points` |

---

## Transaction Velocity

| Metric | Value | Interpretation | Query/Script |
|--------|-------|-----------------|--------------|
| **Avg Value per Million Txns** | 180.02 Cr | Transaction size indicator | `SELECT AVG(value_cr / volume_mn) FROM upi_monthly` |
| **Max Velocity** | TBD | Peak avg transaction value | `SELECT MAX(value_cr / volume_mn) FROM upi_monthly` |
| **Min Velocity** | TBD | Lowest avg transaction value | `SELECT MIN(value_cr / volume_mn) FROM upi_monthly` |

---

## Forecasting (Prophet)

| Metric | Value | Model | Details |
|--------|-------|-------|---------|
| **Baseline MAPE** | 10.74% | 3-month MA | Moving average baseline |
| **Prophet MAPE** | 1.32% | Prophet | Time-series forecasting |
| **Next Month Forecast** | 23,472M | Prophet | July 2026 prediction |
| **6-Month Forecast End** | 25,527M | Prophet | December 2026 prediction |
| **Forecast Trend** | Plateau | Prophet | Growth slowing, approaching saturation |

---

## Segmentation (K-Means, k=3)

| Segment | Months | Avg Volume | Interpretation | Details |
|---------|--------|-----------|-----------------|---------|
| **Segment 0** | 9 | 45.99M | Early Growth | Pre-2019 phase |
| **Segment 1** | 5 | 176.17M | Scaling | 2019-2021 phase |
| **Segment 2** | 2 | 503.65M | Maturity | 2026 phase (recent) |

---

## Anomaly Detection (Isolation Forest)

| Metric | Value | Date | Details |
|--------|-------|------|---------|
| **Total Anomalies** | 2 | - | Out of 114 months |
| **Contamination Rate** | 1.75% | - | 2/114 = actual vs 10% contamination set |
| **Anomaly 1** | 524.94M | Oct 2018 | Score: -0.606 |
| **Anomaly 2** | 482.36M | Nov 2018 | Score: -0.587 |
| **Most Recent Anomaly** | Oct 2018 | - | No anomalies in last 24 months (stable) |

---

## Data Quality

| Metric | Value | Status | Details |
|--------|-------|--------|---------|
| **Raw Rows** | 114 | ✓ | 10 files × 12 months (approx) |
| **Cleaned Rows** | 114 | ✓ | No row loss |
| **Duplicates Removed** | 0 | ✓ | No duplicate dates |
| **Nulls** | 0 | ✓ | Complete data, no imputation needed |
| **Date Range** | Apr 2017 - Sep 2026 | ✓ | 114 consecutive months |
| **Columns** | 5 | ✓ | date, month_str, num_banks, volume_mn, value_cr |

---

## NL-to-SQL Assistant

| Metric | Value | Notes |
|--------|-------|-------|
| **Test Questions** | 15 | Diverse Q&A coverage |
| **Successful** | 9 | Questions with valid SQL + results |
| **Failed** | 6 | Unmatched patterns |
| **Accuracy** | 60% | Rule-based (70% pattern coverage) + Gemini fallback |
| **Rule Patterns** | 10 | Predefined SQL templates |

---

## Computed Metrics (Formulas)

```python
# Growth Rate
growth_pct = ((latest_volume - earliest_volume) / earliest_volume) * 100

# Coefficient of Variation
cv = (std_dev(volumes) / mean(volumes)) * 100

# Concentration Range
concentration = ((max_volume - min_volume) / min_volume) * 100

# Transaction Velocity
velocity = value_cr / volume_mn

# YoY Growth
yoy_growth = pct_change(volume, lag=12) * 100

# MAPE (Forecasting Error)
MAPE = mean(abs((actual - predicted) / actual)) * 100
```

---

**Last Updated**: Oct 2026
**Data Source**: UPI Product Statistics (RBI/NPCI)
**Pipeline**: raw XLSX → pandas → DuckDB → SQL queries
