-- UPI 360: Analytical SQL Queries
-- 10 analytical queries using CTEs, window functions, MoM/YoY growth, ranking, and share

-- 1. Monthly Growth Rates (MoM)
WITH monthly_growth AS (
    SELECT 
        date,
        volume_mn,
        value_cr,
        LAG(volume_mn) OVER (ORDER BY date) as prev_volume,
        LAG(value_cr) OVER (ORDER BY date) as prev_value,
        ROUND(((volume_mn - LAG(volume_mn) OVER (ORDER BY date)) / LAG(volume_mn) OVER (ORDER BY date) * 100), 2) as volume_mom_pct,
        ROUND(((value_cr - LAG(value_cr) OVER (ORDER BY date)) / LAG(value_cr) OVER (ORDER BY date) * 100), 2) as value_mom_pct
    FROM upi_monthly
    ORDER BY date
)
SELECT 
    date,
    volume_mn,
    prev_volume,
    volume_mom_pct,
    value_cr,
    prev_value,
    value_mom_pct
FROM monthly_growth
WHERE volume_mom_pct IS NOT NULL
LIMIT 20;

-- 2. Year-over-Year Growth (YoY)
WITH yearly_data AS (
    SELECT 
        EXTRACT(YEAR FROM date) as year,
        EXTRACT(MONTH FROM date) as month,
        SUM(volume_mn) as total_volume,
        SUM(value_cr) as total_value,
        COUNT(*) as month_count
    FROM upi_monthly
    GROUP BY EXTRACT(YEAR FROM date), EXTRACT(MONTH FROM date)
)
SELECT 
    year,
    month,
    total_volume,
    LAG(total_volume) OVER (PARTITION BY month ORDER BY year) as prev_year_volume,
    ROUND(((total_volume - LAG(total_volume) OVER (PARTITION BY month ORDER BY year)) / LAG(total_volume) OVER (PARTITION BY month ORDER BY year) * 100), 2) as yoy_growth_pct,
    total_value,
    LAG(total_value) OVER (PARTITION BY month ORDER BY year) as prev_year_value
FROM yearly_data
WHERE total_volume IS NOT NULL
ORDER BY month, year;

-- 3. Cumulative Volume & Value Trends
SELECT 
    date,
    volume_mn,
    value_cr,
    SUM(volume_mn) OVER (ORDER BY date) as cumulative_volume,
    SUM(value_cr) OVER (ORDER BY date) as cumulative_value,
    ROUND(AVG(volume_mn) OVER (ORDER BY date ROWS BETWEEN 11 PRECEDING AND CURRENT ROW), 2) as volume_12m_avg,
    ROUND(AVG(value_cr) OVER (ORDER BY date ROWS BETWEEN 11 PRECEDING AND CURRENT ROW), 2) as value_12m_avg
FROM upi_monthly
ORDER BY date;

-- 4. Bank Adoption & Network Growth
SELECT 
    date,
    num_banks,
    volume_mn,
    value_cr,
    RANK() OVER (ORDER BY num_banks DESC) as bank_count_rank,
    ROUND(volume_mn / num_banks, 2) as volume_per_bank,
    ROUND(value_cr / num_banks, 2) as value_per_bank,
    LAG(num_banks) OVER (ORDER BY date) as prev_banks
FROM upi_monthly
ORDER BY date DESC
LIMIT 20;

-- 5. Volume & Value Market Share Evolution
WITH monthly_agg AS (
    SELECT 
        DATE_TRUNC('year', date) as year,
        SUM(volume_mn) as yearly_volume,
        SUM(value_cr) as yearly_value
    FROM upi_monthly
    GROUP BY DATE_TRUNC('year', date)
)
SELECT 
    year,
    yearly_volume,
    ROUND(yearly_volume / SUM(yearly_volume) OVER () * 100, 2) as volume_share_pct,
    yearly_value,
    ROUND(yearly_value / SUM(yearly_value) OVER () * 100, 2) as value_share_pct
FROM monthly_agg
ORDER BY year;

-- 6. Seasonality Analysis (Average by Month)
WITH seasonal_data AS (
    SELECT 
        EXTRACT(MONTH FROM date) as month_num,
        MONTHNAME(date) as month_name,
        AVG(volume_mn) as avg_volume,
        AVG(value_cr) as avg_value,
        STDDEV(volume_mn) as stddev_volume
    FROM upi_monthly
    GROUP BY EXTRACT(MONTH FROM date), MONTHNAME(date)
)
SELECT 
    month_num,
    month_name,
    ROUND(avg_volume, 2) as avg_volume_mn,
    ROUND(avg_value, 2) as avg_value_cr,
    ROUND(stddev_volume, 2) as volatility,
    RANK() OVER (ORDER BY avg_volume DESC) as volume_rank
FROM seasonal_data
ORDER BY month_num;

-- 7. Peak vs Trough Analysis
SELECT 
    'Peak Volume' as metric_type,
    MAX(volume_mn) as peak_value,
    (SELECT date FROM upi_monthly WHERE volume_mn = (SELECT MAX(volume_mn) FROM upi_monthly)) as peak_date,
    ROUND(MAX(volume_mn) - MIN(volume_mn), 2) as range,
    ROUND((MAX(volume_mn) - MIN(volume_mn)) / MIN(volume_mn) * 100, 2) as range_pct
FROM upi_monthly
UNION ALL
SELECT 
    'Trough Volume' as metric_type,
    MIN(volume_mn) as peak_value,
    (SELECT date FROM upi_monthly WHERE volume_mn = (SELECT MIN(volume_mn) FROM upi_monthly)) as peak_date,
    ROUND(MAX(volume_mn) - MIN(volume_mn), 2) as range,
    ROUND((MAX(volume_mn) - MIN(volume_mn)) / MIN(volume_mn) * 100, 2) as range_pct
FROM upi_monthly;

-- 8. Transaction Velocity (Value per Volume Unit)
SELECT 
    date,
    ROUND(value_cr / volume_mn, 2) as value_per_txn_unit,
    ROUND(AVG(value_cr / volume_mn) OVER (ORDER BY date ROWS BETWEEN 5 PRECEDING AND CURRENT ROW), 2) as velocity_6m_avg,
    RANK() OVER (ORDER BY value_cr / volume_mn DESC) as velocity_rank
FROM upi_monthly
ORDER BY date DESC
LIMIT 20;

-- 9. Top Growth Quarters (3-Month Rolling)
WITH quarterly_data AS (
    SELECT 
        date,
        SUM(volume_mn) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling_volume_3m,
        SUM(value_cr) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as rolling_value_3m,
        LAG(SUM(volume_mn) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)) OVER (ORDER BY date) as prev_rolling_volume
    FROM upi_monthly
)
SELECT 
    date,
    ROUND(rolling_volume_3m, 2) as rolling_volume_3m,
    ROUND(rolling_value_3m, 2) as rolling_value_3m,
    ROUND(((rolling_volume_3m - prev_rolling_volume) / prev_rolling_volume * 100), 2) as growth_vs_prev_3m
FROM quarterly_data
WHERE prev_rolling_volume IS NOT NULL
ORDER BY rolling_volume_3m DESC
LIMIT 10;

-- 10. Market Concentration & Inflection Points
WITH concentration_data AS (
    SELECT 
        date,
        volume_mn,
        MAX(volume_mn) OVER (ORDER BY date ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) as max_12m_volume,
        MIN(volume_mn) OVER (ORDER BY date ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) as min_12m_volume,
        ROUND((MAX(volume_mn) OVER (ORDER BY date ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) - MIN(volume_mn) OVER (ORDER BY date ROWS BETWEEN 11 PRECEDING AND CURRENT ROW)) / MIN(volume_mn) OVER (ORDER BY date ROWS BETWEEN 11 PRECEDING AND CURRENT ROW) * 100, 2) as concentration_range_pct,
        CASE 
            WHEN volume_mn > LAG(volume_mn) OVER (ORDER BY date) 
             AND volume_mn > LEAD(volume_mn) OVER (ORDER BY date) THEN 'Local Peak'
            WHEN volume_mn < LAG(volume_mn) OVER (ORDER BY date) 
             AND volume_mn < LEAD(volume_mn) OVER (ORDER BY date) THEN 'Local Trough'
            ELSE 'Normal'
        END as inflection_type
    FROM upi_monthly
)
SELECT 
    date,
    volume_mn,
    concentration_range_pct,
    inflection_type,
    RANK() OVER (ORDER BY concentration_range_pct DESC) as volatility_rank
FROM concentration_data
ORDER BY date
LIMIT 30;
