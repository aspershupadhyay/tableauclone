# components/chart_config.py

import streamlit as st

def configure_chart(chart_index, chart):
    """
    Provides a user interface to configure chart properties.

    Args:
        chart_index (int): The index of the chart in the session state.
        chart (dict): The chart dictionary containing type and configuration.

    Returns:
        None: Updates the chart configuration in the session state.
    """
    st.subheader(f"Configure {chart['type']} Chart {chart_index + 1}")

    config = chart.get("config", {})

    # Title and Subtitle
    config["title"] = st.text_input(
        "Title",
        value=config.get("title", f"{chart['type']} Chart")
    )
    config["subtitle"] = st.text_input(
        "Subtitle",
        value=config.get("subtitle", "")
    )

    # Color Configuration
    config["color"] = st.color_picker(
        "Choose Chart Color",
        value=config.get("color", "#1f77b4")
    )

    # Gridlines
    config["show_grid"] = st.checkbox(
        "Show Gridlines",
        value=config.get("show_grid", True)
    )

    # Legend
    config["show_legend"] = st.checkbox(
        "Show Legend",
        value=config.get("show_legend", True)
    )

    # Tick Marks
    config["show_ticks"] = st.checkbox(
        "Show Tick Marks",
        value=config.get("show_ticks", True)
    )

    # Marker Size (for applicable charts)
    if chart["type"] in ["Scatter Plot", "Line Chart", "Bar Chart"]:
        config["marker_size"] = st.slider(
            "Marker Size",
            min_value=5,
            max_value=20,
            value=config.get("marker_size", 10)
        )

    # Sorting Access: Maximum Number of Data Points
    config["max_data_points"] = st.number_input(
        "Maximum Number of Data Points to Display",
        min_value=1,
        max_value=1000,
        value=config.get("max_data_points", 100),
        step=1
    )

    # Background Color
    config["background_color"] = st.color_picker(
        "Choose Background Color",
        value=config.get("background_color", "#ffffff")
    )

    # Sorting Order (Ascending/Descending)
    sort_options = ["None", "Ascending", "Descending"]
    config["sort_order"] = st.selectbox(
        "Sort Order",
        options=sort_options,
        index=sort_options.index(config.get("sort_order", "None")) if config.get("sort_order", "None") in sort_options else 0
    )

    # Sort By Column (if applicable)
    if config.get("sort_order", "None") != "None":
        columns = list(st.session_state["data"].columns)
        config["sort_by"] = st.selectbox(
            "Sort By Column",
            options=columns,
            index=columns.index(config.get("sort_by")) if config.get("sort_by") in columns else 0
        )

    # Axis Configuration
    columns = list(st.session_state["data"].columns)
    if chart["type"] in ["Bar Chart", "Line Chart", "Scatter Plot"]:
        config["x_axis"] = st.selectbox(
            "Select X-axis",
            options=columns,
            index=columns.index(config.get("x_axis", columns[0])) if config.get("x_axis", columns[0]) in columns else 0
        )
        config["y_axis"] = st.selectbox(
            "Select Y-axis",
            options=columns,
            index=columns.index(config.get("y_axis", columns[1] if len(columns) > 1 else columns[0])) if config.get("y_axis", columns[1] if len(columns) > 1 else columns[0]) in columns else 0
        )
    elif chart["type"] == "Pie Chart":
        config["names"] = st.selectbox(
            "Select Names (Categories)",
            options=columns,
            index=columns.index(config.get("names", columns[0])) if config.get("names", columns[0]) in columns else 0
        )
        config["values"] = st.selectbox(
            "Select Values",
            options=columns,
            index=columns.index(config.get("values", columns[1] if len(columns) > 1 else columns[0])) if config.get("values", columns[1] if len(columns) > 1 else columns[0]) in columns else 0
        )

    # Update the chart configuration in session state
    st.session_state["charts"][chart_index]["config"] = config

    st.markdown("---")
