# utils/config.py

import streamlit as st
import os

def load_css(file_path='styles/styles.css'):
    """
    Loads and injects the CSS styles into the Streamlit app.

    Args:
        file_path (str): The path to the CSS file.

    Returns:
        None
    """
    if os.path.exists(file_path):
        with open(file_path) as f:
            css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found at {file_path}. Skipping custom styles.")
