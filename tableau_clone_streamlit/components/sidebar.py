# components/sidebar.py

import streamlit as st
from utils import data_handler
from PIL import Image
import os

# Define the path to the icons
ICON_PATH = os.path.join("assets", "icons")

# Available chart types and their corresponding icon filenames
CHART_TYPES = {
    "Bar Chart": "bar_chart.png",
    "Line Chart": "line_chart.png",
    "Pie Chart": "pie_chart.png",
    "Scatter Plot": "scatter_plot.png",
    # Add more chart types and their icons as needed
}

def render_sidebar():
    st.sidebar.title("Data Upload")

    # File Uploader
    uploaded_file = st.sidebar.file_uploader("Upload your data file", type=["csv", "xlsx", "json"])

    # URL Data Fetcher
    data_url = st.sidebar.text_input("Or enter a data URL")

    # Handle data upload or URL fetch
    if uploaded_file:
        with st.spinner("Loading data..."):
            data = data_handler.load_data(uploaded_file)
        st.session_state["data"] = data
        st.success("Data loaded successfully!")
    elif data_url:
        with st.spinner("Fetching data from URL..."):
            data = data_handler.load_data_from_url(data_url)
        if data is not None:
            st.session_state["data"] = data
            st.success("Data fetched successfully!")
    else:
        st.session_state["data"] = None

    st.sidebar.markdown("---")
    st.sidebar.title("Create Charts")

    # Display chart icons
    cols = st.sidebar.columns(4)  # Adjust the number based on number of icons per row
    for idx, (chart_name, icon_file) in enumerate(CHART_TYPES.items()):
        with cols[idx % 4]:
            if st.button(f"Add {chart_name}", key=f"chart_{chart_name}"):
                if "charts" not in st.session_state:
                    st.session_state["charts"] = []
                st.session_state["charts"].append({"type": chart_name, "config": {}})
                st.success(f"{chart_name} added!")
        # Display the icon image
            icon_path = os.path.join(ICON_PATH, icon_file)
            if os.path.exists(icon_path):
                image = Image.open(icon_path)
                st.image(image, width=50)
            else:
                st.write(chart_name)

    # Option to remove charts
    if "charts" in st.session_state and st.session_state["charts"]:
        st.sidebar.markdown("---")
        st.sidebar.title("Manage Charts")
        for idx, chart in enumerate(st.session_state["charts"], start=1):
            if st.sidebar.button(f"Remove Chart {idx}", key=f"remove_chart_{idx}"):
                st.session_state["charts"].pop(idx - 1)
                st.sidebar.success(f"Chart {idx} removed!")
                st.experimental_rerun()
