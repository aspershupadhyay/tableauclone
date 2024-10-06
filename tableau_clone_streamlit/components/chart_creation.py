# components/chart_creation.py

import streamlit as st
from .chart_config import configure_chart
import plotly.express as px

def render_charts(data):
    """
    Renders all charts added by the user with their configurations.

    Args:
        data (pd.DataFrame): The dataset to visualize.
    """
    if "charts" not in st.session_state or not st.session_state["charts"]:
        st.info("No charts added yet. Use the sidebar to add charts.")
        return

    st.header("Your Charts")

    for idx, chart in enumerate(st.session_state["charts"]):
        with st.expander(f"{chart['type']} Chart {idx + 1}", expanded=True):
            # Configure the chart
            configure_chart(idx, chart, data)

            # Render the chart with the updated configuration
            fig = generate_plotly_chart(data, chart)
            st.plotly_chart(fig, use_container_width=True)

def generate_plotly_chart(data, chart):
    """
    Generates a Plotly chart based on the chart configuration.

    Args:
        data (pd.DataFrame): The dataset to visualize.
        chart (dict): The chart dictionary containing type and configuration.

    Returns:
        plotly.graph_objs._figure.Figure: The Plotly figure object.
    """
    chart_type = chart.get("type
