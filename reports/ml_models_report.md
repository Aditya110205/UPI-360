# ML Models Report

## 1. Forecasting
- **Baseline MAPE:** 10.74%
- **Model:** 3-month moving average
- **Status:** Baseline established for comparison

## 2. Segmentation (K-Means, k=3)
- **Features:** Recent volume, frequency of highs, transaction value
- **Segments:** 4 clusters identified
- **Use:** Identify market phases and volume regimes

## 3. Anomaly Detection (Isolation Forest)
- **Features:** Volume & transaction velocity
- **Contamination:** 10%
- **Anomalies Found:** 2
- **Top Anomaly:** 2018-11-01 (volume 524.94 Mn, velocity 156.65)

## Key Insights
- System showing exponential growth phase (volumes 30,000%+ over 9 years)
- Recent growth stabilizing (36.2% YoY vs 225% in 2019)
- Anomalies concentrated in early years and recent months (system maturation vs new phase)

