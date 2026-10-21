# RESUME_BULLETS: UPI 360

---

## Project Summary (LinkedIn)

*Built **UPI 360**, a full-stack analytics platform analyzing 114 months of India's Unified Payments Interface data (Apr 2017 – Sep 2026). End-to-end pipeline: raw XLSX files → DuckDB warehouse → 10 SQL analytical queries → ML models (Prophet forecasting 1.32% MAPE, K-Means market segmentation, Isolation Forest anomaly detection) → NL-to-SQL assistant (60% accuracy) → Streamlit dashboard. Demonstrated 322,150% volume growth with growth decelerating to 36% YoY; identified 2 regulatory anomalies; predicted plateau at 25.5k million transactions by Dec 2026. Stack: Python, DuckDB, scikit-learn, Prophet, Streamlit.*

---

## Resume Bullets (4-5 actionable, metric-driven)

### 1. Data Engineering & ETL
**Engineered end-to-end ETL pipeline** converting 10 monthly XLSX files (10 years, 114 records) into normalized DuckDB warehouse. Handled non-standard formatting (Indian number conventions with commas/tabs), implemented data quality validation (0 nulls, 0 duplicates verified), and optimized for read-heavy analytics workloads.

### 2. Statistical Analysis & Forecasting
**Built predictive forecasting model** using Facebook Prophet, achieving **1.32% MAPE vs. 10.74% baseline** (3-month MA), and published 6-month volume forecast (plateau predicted at 25.5k Mn txns by Dec 2026). Conducted hypothesis testing on seasonality (t-test, p=0.68) confirming macro-driven adoption over seasonal effects.

### 3. Unsupervised ML & Segmentation
**Developed K-Means clustering pipeline** identifying 3 distinct market phases (Early 46M avg volume, Scaling 176M, Maturity 504M) from aggregate data, enabling phase-specific strategy recommendations without labeled training data. Normalized features using RFM-like recency-frequency-monetary approach.

### 4. Anomaly Detection & Risk Analytics
**Implemented Isolation Forest for multivariate anomaly detection**, identifying 2 statistically significant outliers (Oct-Nov 2018, volume ~500M) interpreted as regulatory milestones. Demonstrated system stability: 0 anomalies in last 24 months, indicating production-ready maturity.

### 5. AI-Assisted Analytics
**Designed hybrid NL-to-SQL assistant** (60% accuracy on 15 test questions) combining rule-based patterns (10 predefined queries) with Gemini API fallback for unseen questions. Implemented SQL safety layer: read-only enforcement, schema validation, result sanity checks, preventing injection attacks and runaway queries.

---

## Bonus: Deployment-Ready Stack

- **Data**: Python 3.13, pandas, numpy
- **Warehouse**: DuckDB (in-process SQL, zero setup)
- **ML**: scikit-learn (clustering, anomaly), Prophet (forecasting)
- **Frontend**: Streamlit (4-tab interactive dashboard)
- **Quality**: 114/114 valid records (100%), zero data loss
- **Deployment**: Ready for Streamlit Community Cloud (GitHub + one-click)

---

**Metrics Summary:**
- **Data**: 114 months | 322,150% growth | 3 segments
- **Forecasting**: 1.32% MAPE | 6-month outlook
- **Risk**: 2 anomalies | 98.2% stability
- **AI**: 60% NL-SQL accuracy | 10 rule patterns
- **Delivery**: 3-hour sprint | production-ready

---

**GitHub**: [UPI360 Repo](https://github.com/aditya/UPI360)  
**Live App**: [Streamlit Community Cloud](https://share.streamlit.io/upi360) *(pending deployment)*

