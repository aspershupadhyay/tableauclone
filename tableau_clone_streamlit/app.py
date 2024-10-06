# app.py

import streamlit as st
from components import sidebar, main_content
from utils import cache_manager, config

def main():
    st.set_page_config(page_title="Streamlit Tableau Clone", layout="wide")
    
    # Load custom CSS
    config.load_css()

    # Initialize session state variables
    if "data" not in st.session_state:
        st.session_state["data"] = None
    if "charts" not in st.session_state:
        st.session_state["charts"] = []
    
    # Initialize sidebar
    sidebar.render_sidebar()
    
    # Initialize main content
    main_content.render_main_content()

if __name__ == "__main__":
    main()
