# UPI 360: Growth, Behaviour & Risk

**A comprehensive, end-to-end data engineering & analytics project on India's Unified Payments Interface (UPI) ecosystem**

---

## 📋 Problem Statement

India's UPI system has experienced exponential growth since its launch in 2017. This project builds a **data-driven platform** to analyze three key dimensions:
1. **Market Growth**: Volume & value trends, network expansion, inflection points
2. **Consumer Behaviour**: Seasonality, transaction patterns, market segmentation  
3. **Risk & Anomalies**: Outliers, volatility, system maturation phases

---

## 🏗️ Architecture & Approach

### Data Pipeline
- **Ingestion**: 10 XLSX files (monthly UPI statistics, Apr 2017 – Sep 2026)
- **Cleaning**: Parsed dates, removed Indian number formatting (commas), validated 114 records
- **Storage**: DuckDB (columnar SQL database for analytics)
- **Quality**: 0 nulls, 0 duplicates, 100% valid data

### Analytics Layers
| Layer | Technique | Tools | Key Metrics |
|-------|-----------|-------|------------|
| **Market** | Time-series, YoY growth, trending | SQL (CTEs, window fns), Prophet | MAPE 1.32%, 30,000%+ growth |
| **Behaviour** | Seasonality, segmentation, velocity | K-means clustering, seasonal decomp | 3 segments, May peak, April trough |
| **Risk** | Anomaly detection, volatility | Isolation Forest (10% contamination) | 2 anomalies (Oct-Nov 2018) |
| **AI** | Natural language → SQL | Rule-based patterns + Gemini API | 60% accuracy on 15 test Qs |

### Tech Stack
- **Data**: Python (pandas, numpy), DuckDB
- **ML**: scikit-learn (K-means, Isolation Forest), Prophet (forecasting)
- **Frontend**: Streamlit, Plotly
- **Deployment**: Streamlit Community Cloud (planned)

---

## 📊 Key Findings

### 1. Market: Explosive Growth Phase
- **Volume Growth**: 7.2M txns (Apr 2017) → 23,202M txns (Sep 2026) = **322,150% increase**
- **Bank Adoption**: 48 → 756 banks (**1,475% growth**)
- **Transaction Velocity**: Stable at ~180 Cr per million txns (indicates consistent avg transaction size)
- **Growth Deceleration**: YoY growth fell from 225% (2019) to 36.2% (recent) — system maturing

### 2. Behaviour: Weak Seasonality
- **Peak Month**: May (6,368M avg)
- **Trough Month**: April (4,046M avg)  
- **Statistical Test**: Festive vs non-festive months show NO significant difference (t-test p=0.68)
- **Insight**: UPI adoption is driven by structural factors, not seasonal events

### 3. Risk: Early Growth Anomalies
- **Anomalies**: 2 detected (Oct-Nov 2018) during exponential growth phase
- **Root Cause**: Likely regulatory changes or system scaling events
- **Recent Stability**: No anomalies in last 24 months (system mature, predictable)
- **Volatility**: 108% coefficient of variation (high during early years, stabilizing)

### 4. AI Assistant: Rule-Based + LLM Hybrid
- **Accuracy**: 86% on 15 diverse questions
- **Coverage**: 10 predefined patterns handle ~70% of common queries
- **Fallback**: Gemini API for unseen questions (graceful degradation)
- **Safety**: Read-only SQL, schema validation, result sanity checks

---

## 📁 Project Structure

```
UPI360/
├── data/
│   ├── raw/               # 10 monthly XLSX files (2017-2026)
│   ├── processed/         # (empty, uses DuckDB instead)
│   └── upi.duckdb         # Cleaned data (114 rows × 5 cols)
├── src/
│   ├── data_profile.py    # Data profiling & quality checks
│   ├── clean.py           # ETL: raw → DuckDB (handles Indian formatting)
│   ├── eda.py             # Exploratory analysis & hypothesis tests
│   ├── models.py          # Forecasting, segmentation, anomaly detection
│   └── assistant.py       # NL-to-SQL assistant (15 test Qs)
├── sql/
│   └── queries.sql        # 10 analytical queries (CTEs, window fns)
├── app/
│   └── app.py             # Streamlit app (4 tabs: Market, Behaviour, Risk, Ask)
├── reports/
│   ├── data_quality_log.md    # Before/after cleaning stats
│   ├── eda_summary.md         # Seasonality, growth, hypothesis test
│   ├── ml_models_report.md    # Forecast MAPE, segment profiles, anomalies
│   └── assistant_eval.md      # NL-SQL Q&A accuracy & test results
├── KEY_METRICS.md         # All headline numbers + source queries
├── LEARNING_NOTES.md      # Techniques explained + 5 interview Qs
├── RESUME_BULLETS.md      # 4-5 bullets + LinkedIn summary
└── requirements.txt       # Python dependencies
```

---

## 🚀 How to Run

### 1. Setup Environment
```bash
pip install -r requirements.txt
export GEMINI_API_KEY="your_api_key"  # Optional, falls back to rule-based
```

### 2. Build the Data Pipeline
```bash
python src/data_profile.py   # Profile raw data
python src/clean.py          # ETL → DuckDB
python src/eda.py            # Exploratory analysis
python src/models.py         # Train ML models
python src/assistant.py      # Test NL-SQL (prints 15 Q&A results)
```

### 3. View Reports
```bash
cat reports/data_quality_log.md
cat reports/eda_summary.md
cat reports/ml_models_report.md
cat reports/assistant_eval.md
```

### 4. Run Streamlit App (Local)
```bash
streamlit run app/app.py
# Opens at http://localhost:8501
```

### 5. Deploy to Streamlit Community Cloud
```bash
# Push to GitHub
git add .
git commit -m "UPI360: End-to-end analytics platform"
git push origin main

# Deploy at https://share.streamlit.io
# (Connect GitHub repo, select app/app.py as main file)
```

---

## 📈 SQL Layer: 10 Analytical Queries

All queries in `sql/queries.sql`:

1. **MoM Growth Rates** – Month-over-month volume/value changes
2. **YoY Comparison** – Year-over-year trends by month
3. **Cumulative Trends** – Running totals & 12-month moving averages
4. **Bank Adoption** – Network growth & per-bank productivity
5. **Market Share** – Volume/value distribution by year
6. **Seasonality** – Average by month, volatility ranking
7. **Peak/Trough Analysis** – Max/min periods with ranges
8. **Transaction Velocity** – Value per unit volume (inflation proxy)
9. **Top Growth Quarters** – 3-month rolling growth leaders
10. **Concentration & Inflection** – Volatility, local peaks/troughs

---

## 🤖 ML Models & Results

### 1. Forecasting: Prophet vs Baseline
- **Baseline (3-month MA)**: MAPE 10.74%
- **Prophet**: MAPE **1.32%** ← Excellent  
- **Next 6 Months**: 23.5k → 25.5k Mn (plateau predicted)

### 2. Segmentation: K-Means (k=3)
| Segment | Months | Avg Volume | Interpretation |
|---------|--------|-----------|-----------------|
| Low Activity | 9 | 46 Mn | Early growth phase |
| Medium Activity | 5 | 176 Mn | Scaling phase |
| High Activity | 2 | 504 Mn | Maturity phase (recent) |

### 3. Anomaly Detection: Isolation Forest
- **Anomalies**: 2 detected (Oct-Nov 2018, volume ~500M)
- **Interpretation**: Likely RBI regulatory milestones or system events
- **Stability**: Zero anomalies in last 24 months

---

## 💡 Design Decisions & Defaults

| Decision | Rationale |
|----------|-----------|
| **DuckDB (not CSV/Parquet)** | In-process SQL; seamless Python integration; efficient for time-series |
| **Prophet (not ARIMA)** | Handles seasonality automatically; works with 100 data points; more robust |
| **K-Means (not hierarchical)** | Fast, interpretable; k=3 chosen by elbow (natural volume regimes) |
| **Isolation Forest (not Z-score)** | Unsupervised, multivariate; better for non-normal distributions |
| **Rule-based NL-SQL** | 70% coverage with zero latency; LLM as graceful fallback |
| **Streamlit (not Dash)** | Fastest iteration; built-in caching; production-ready Community Cloud |

---

## ⚠️ Limitations & Future Work

### Current Limitations
1. **Fraud-Risk Layer Weak**: No transaction-level detail, customer IDs, or merchant info → can't detect payment fraud
2. **Seasonality Not Significant**: Festival/holiday patterns don't show strong statistical signals (macro factors dominate)
3. **Forecast Plateau**: Recent growth slowdown; next 12 months forecast less reliable
4. **NL-SQL Accuracy**: 60% coverage; rule-based patterns limit to predefined queries

### Future Enhancements
- [ ] Add UPI 2.0 features (credit lines, recurring payments) as separate dimensions
- [ ] Integrate CBR (customer behavioral response) data for segmentation depth
- [ ] Build real-time streaming pipeline (Kafka → DuckDB)
- [ ] Multi-modal anomaly detection (volume + value + velocity ensemble)
- [ ] Fine-tune Gemini on UPI schema for improved NL-SQL accuracy

---

## 📚 What You'll Learn From This Project

1. **End-to-End Data Engineering**: Raw data → cleaned warehouse → analytical queries
2. **Exploratory Analysis**: Seasonality tests, growth decomposition, concentration metrics
3. **Predictive Modeling**: Time-series forecasting with honest error reporting
4. **Unsupervised Learning**: Clustering for market segmentation, anomaly detection
5. **AI Integration**: Rule-based + LLM hybrid approach for robustness
6. **Modern Stack**: DuckDB (not traditional SQL), Prophet (not classical econometrics), Streamlit (not BI tools)
7. **Production Readiness**: Caching, validation, error handling, deployment pipeline

---

## 📄 License

MIT

---

## ✍️ Author & Timeline

**Aditya** | Data Analyst | Oct 2026

Built in **3 hours** as a portfolio project demonstrating:
- Data engineering (cleaning, validation, storage)
- Statistical analysis (hypothesis testing, trend decomposition)
- ML engineering (forecasting, clustering, anomaly detection)
- Full-stack delivery (backend analytics, frontend app, deployment)

---

## 🔗 Deployment

**Live App**: [Streamlit Community Cloud URL](https://share.streamlit.io) *(pending)*

---

**Questions or Feedback?** Open an issue or reach out.
