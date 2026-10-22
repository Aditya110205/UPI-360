"""Streamlit wrapper: shows the UPI 360 dashboard (dashboard/index.html).
Run: streamlit run app/app.py
"""
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="UPI 360", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.block-container{padding:0.5rem 0.5rem 0}header,footer{visibility:hidden}</style>", unsafe_allow_html=True)

page = Path(__file__).resolve().parent.parent / "dashboard" / "index.html"
if not page.exists():
    st.error("dashboard/index.html not found. Run: python src/models.py, then python src/build_dashboard.py")
else:
    components.html(page.read_text(encoding="utf-8"), height=1650, scrolling=True)