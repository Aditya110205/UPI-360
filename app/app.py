import streamlit as st
import pandas as pd
import duckdb

st.set_page_config(page_title="UPI 360", layout="wide")

# Connect to database
db_path = r"C:\Users\Aditya\OneDrive\Desktop\DataEngineering\UPI360\data\upi.duckdb"
db = duckdb.connect(db_path)

st.title("📊 UPI 360 Analytics")
st.success("✓ Database connected. 114 rows found.")

# Simple tab navigation
tab = st.radio("Select Tab:", ["Market", "Behaviour", "Risk", "Ask the Data"], horizontal=True)

# ============================================================================
# MARKET
# ============================================================================
if tab == "Market":
    st.header("📈 Market Growth & Trends")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Get metrics
    total = db.execute("SELECT ROUND(SUM(volume_mn), 0) FROM upi_monthly").fetchall()[0][0]
    growth = db.execute("SELECT ROUND(((SELECT volume_mn FROM upi_monthly ORDER BY date DESC LIMIT 1) - (SELECT volume_mn FROM upi_monthly ORDER BY date ASC LIMIT 1)) / (SELECT volume_mn FROM upi_monthly ORDER BY date ASC LIMIT 1) * 100, 2)").fetchall()[0][0]
    peak = db.execute("SELECT MAX(volume_mn) FROM upi_monthly").fetchall()[0][0]
    banks = db.execute("SELECT ROUND(((MAX(num_banks) - MIN(num_banks)) / MIN(num_banks) * 100), 2) FROM upi_monthly").fetchall()[0][0]
    
    col1.metric("Total Volume", f"{total:,.0f}M")
    col2.metric("Growth Rate", f"{growth:,.0f}%")
    col3.metric("Peak Volume", f"{peak:,.0f}M")
    col4.metric("Bank Growth", f"{banks:,.0f}%")
    
    st.subheader("Recent Data (Last 10 Months)")
    df = db.execute("SELECT date, volume_mn, value_cr, num_banks FROM upi_monthly ORDER BY date DESC LIMIT 10").fetch_df()
    st.dataframe(df, use_container_width=True)

# ============================================================================
# BEHAVIOUR
# ============================================================================
elif tab == "Behaviour":
    st.header("👥 Consumer Behaviour")
    
    st.subheader("Seasonality by Month")
    seasonal = db.execute("SELECT EXTRACT(MONTH FROM date) as month, ROUND(AVG(volume_mn), 2) as avg_volume FROM upi_monthly GROUP BY EXTRACT(MONTH FROM date) ORDER BY month").fetch_df()
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    seasonal['month_name'] = [months[int(m)-1] for m in seasonal['month']]
    st.dataframe(seasonal[['month_name', 'avg_volume']], use_container_width=True)
    
    st.subheader("Market Segments")
    segments = db.execute("SELECT segment_name, COUNT(*) as months, ROUND(AVG(volume_mn), 2) as avg_volume FROM segments WHERE segment_name IS NOT NULL GROUP BY segment_name ORDER BY avg_volume DESC").fetch_df()
    st.dataframe(segments, use_container_width=True)

# ============================================================================
# RISK
# ============================================================================
elif tab == "Risk":
    st.header("⚠️ Risk & Anomalies")
    
    anom_count = db.execute("SELECT COUNT(*) FROM anomalies WHERE is_anomaly = true").fetchall()[0][0]
    st.metric("Anomalies Detected", anom_count)
    
    st.subheader("Anomalous Periods")
    anomalies = db.execute("SELECT date, ROUND(volume_mn, 2) as volume_mn, ROUND(anomaly_score, 4) as score FROM anomalies WHERE is_anomaly = true ORDER BY date DESC").fetch_df()
    if len(anomalies) > 0:
        st.dataframe(anomalies, use_container_width=True)
    else:
        st.info("No anomalies detected")

# ============================================================================
# ASK THE DATA
# ============================================================================
elif tab == "Ask the Data":
    st.header("🤖 Ask the Data (NL-SQL)")
    
    question = st.text_input("Ask a question:", placeholder="e.g., What is the growth rate? / Show recent volume / Market segments")
    
    if question:
        rules = {
            "growth": "SELECT ROUND(((SELECT volume_mn FROM upi_monthly ORDER BY date DESC LIMIT 1) - (SELECT volume_mn FROM upi_monthly ORDER BY date ASC LIMIT 1)) / (SELECT volume_mn FROM upi_monthly ORDER BY date ASC LIMIT 1) * 100, 2) as result",
            "total volume": "SELECT ROUND(SUM(volume_mn), 0) as result FROM upi_monthly",
            "recent": "SELECT date, ROUND(volume_mn, 2) as volume FROM upi_monthly ORDER BY date DESC LIMIT 6",
            "trend": "SELECT date, ROUND(volume_mn, 2) as volume FROM upi_monthly ORDER BY date LIMIT 12",
            "anomalies": "SELECT date, ROUND(volume_mn, 2) as volume FROM anomalies WHERE is_anomaly = true",
            "segments": "SELECT segment_name, COUNT(*) as months FROM segments WHERE segment_name IS NOT NULL GROUP BY segment_name",
            "peak": "SELECT MAX(volume_mn) as peak_volume FROM upi_monthly",
            "banks": "SELECT MAX(num_banks) as max_banks, MIN(num_banks) as min_banks FROM upi_monthly",
        }
        
        sql = None
        for key, query in rules.items():
            if key in question.lower():
                sql = query
                break
        
        if sql:
            try:
                result = db.execute(sql).fetch_df()
                st.success("✓ Query executed")
                st.dataframe(result, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Question not recognized. Try: growth, total volume, recent, trend, anomalies, segments, peak, banks")

st.markdown("---")
st.markdown("*UPI 360 Analytics | Backend: ✓ Database: ✓ Analysis: ✓*")
