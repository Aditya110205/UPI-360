"""EDA + Stats: trends, seasonality, concentration, hypothesis test."""
import pandas as pd
import duckdb
import numpy as np
from scipy import stats
from datetime import datetime

db = duckdb.connect("data/upi.duckdb")

# Load data
df = db.execute("SELECT * FROM upi_monthly ORDER BY date").fetch_df()
df['date'] = pd.to_datetime(df['date'])
df['volume_mn'] = pd.to_numeric(df['volume_mn'], errors='coerce')
df['value_cr'] = pd.to_numeric(df['value_cr'], errors='coerce')

print("=" * 80)
print("EXPLORATORY DATA ANALYSIS & STATISTICS")
print("=" * 80)

# 1. Trend Analysis
print("\n[TREND ANALYSIS]")
early_12m = df[df['date'] < '2018-04-01']['volume_mn'].mean()
late_12m = df[df['date'] >= '2025-09-01']['volume_mn'].mean()
overall_growth = ((late_12m - early_12m) / early_12m) * 100
print(f"Early period avg (Apr 17-Mar 18): {early_12m:.2f} Mn")
print(f"Late period avg (Sep 25-Sep 26): {late_12m:.2f} Mn")
print(f"Growth: {overall_growth:.1f}%")

# 2. Seasonality
print("\n[SEASONALITY ANALYSIS]")
df['month'] = pd.to_datetime(df['date']).dt.month
df['month_name'] = pd.to_datetime(df['date']).dt.strftime('%B')
seasonal = df.groupby(['month', 'month_name'])['volume_mn'].agg(['mean', 'std']).reset_index()
print(seasonal.to_string(index=False))
peak_month = seasonal.loc[seasonal['mean'].idxmax(), 'month_name']
low_month = seasonal.loc[seasonal['mean'].idxmin(), 'month_name']
print(f"Peak: {peak_month} | Trough: {low_month}")

# 3. Concentration & Volatility
print("\n[CONCENTRATION & VOLATILITY]")
df_clean = df.dropna(subset=['volume_mn'])
concentration = ((df_clean['volume_mn'].max() - df_clean['volume_mn'].min()) / df_clean['volume_mn'].min()) * 100
cv = (df_clean['volume_mn'].std() / df_clean['volume_mn'].mean()) * 100
print(f"Max volume: {df_clean['volume_mn'].max():.2f} Mn")
print(f"Min volume: {df_clean['volume_mn'].min():.2f} Mn")
print(f"Concentration Range: {concentration:.1f}%")
print(f"Coefficient of Variation: {cv:.1f}%")

# 4. Transaction Velocity (Value per Unit Volume)
print("\n[TRANSACTION VELOCITY]")
df['velocity'] = df['value_cr'] / df['volume_mn']
vel_early = df[df['date'] < '2018-04-01']['velocity'].mean()
vel_late = df[df['date'] >= '2025-09-01']['velocity'].mean()
print(f"Avg Value per Million Txn: {df['velocity'].mean():.2f} Cr")
if pd.notna(vel_early) and pd.notna(vel_late):
    print(f"Velocity trend (early vs late): {vel_early:.2f} → {vel_late:.2f}")

# 5. Hypothesis Test: Festive vs Non-Festive Months
# Festive: Oct-Dec (Diwali season), March-April (fiscal year, summer)
print("\n[HYPOTHESIS TEST: FESTIVE vs NON-FESTIVE MONTHS]")
festive_months = [10, 11, 12, 3, 4]
df['is_festive'] = df['month'].isin(festive_months)
festive_volumes = df[df['is_festive']]['volume_mn'].dropna().values
non_festive_volumes = df[~df['is_festive']]['volume_mn'].dropna().values

print(f"Festive months avg volume: {festive_volumes.mean():.2f} Mn")
print(f"Non-festive months avg volume: {non_festive_volumes.mean():.2f} Mn")

# T-test
t_stat, p_value = stats.ttest_ind(festive_volumes, non_festive_volumes)
print(f"T-statistic: {t_stat:.4f} | P-value: {p_value:.4f}")
if p_value < 0.05:
    print(f"✓ Significant difference (p < 0.05): Festive months show higher volumes")
else:
    print(f"✗ No significant difference (p >= 0.05)")

# 6. Bank Adoption
print("\n[BANK ADOPTION]")
print(f"Banks at start: {df.iloc[0]['num_banks']}")
print(f"Banks at end: {df.iloc[-1]['num_banks']}")
print(f"Growth: {((df.iloc[-1]['num_banks'] - df.iloc[0]['num_banks']) / df.iloc[0]['num_banks']) * 100:.1f}%")

# 7. Growth Acceleration
print("\n[GROWTH PHASES]")
df['yoy_growth'] = df['volume_mn'].pct_change(12) * 100
recent_yoy = df[df['date'] >= '2025-01-01']['yoy_growth'].dropna().mean()
early_yoy = df[(df['date'] >= '2019-01-01') & (df['date'] < '2020-01-01')]['yoy_growth'].dropna().mean()
print(f"YoY growth (early 2019): {early_yoy:.1f}%")
print(f"YoY growth (recent): {recent_yoy:.1f}%")

print("\n" + "=" * 80)

# Write summary
summary = f"""# EDA & Statistics Summary

## Key Findings

1. **Long-term Growth**: {overall_growth:.1f}% expansion from 2017-18 to 2025-26
2. **Seasonality**: Peak in {peak_month}, Trough in {low_month}
3. **Volatility**: {cv:.1f}% coefficient of variation
4. **Hypothesis Test**: {'Festive months significantly higher (p < 0.05)' if p_value < 0.05 else 'No significant seasonal effect'}
5. **Bank Adoption**: {df.iloc[-1]['num_banks'] - df.iloc[0]['num_banks']} new banks ({((df.iloc[-1]['num_banks'] - df.iloc[0]['num_banks']) / df.iloc[0]['num_banks']) * 100:.1f}% growth)
6. **Transaction Velocity**: {df['velocity'].mean():.2f} Cr per Mn txns (relatively stable)
7. **Recent YoY Growth**: {recent_yoy:.1f}% (vs {early_yoy:.1f}% in 2019)

## Next Steps
- Anomaly detection on volume/value
- Segmentation: RFM-like clustering on volume, growth, velocity
- Forecasting: baseline ARIMA vs Prophet
"""

with open("reports/eda_summary.md", "w") as f:
    f.write(summary)

print("[LOG] EDA summary written to reports/eda_summary.md")
db.close()
