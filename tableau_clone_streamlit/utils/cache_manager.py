# utils/cache_manager.py

import streamlit as st

@st.cache_data
def get_cached_data(data):
    return data.copy()

@st.cache_resource
def get_cached_charts(charts):
    return charts.copy()
