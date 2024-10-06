import streamlit as st
import pandas as pd
import plotly.express as px
from utils import cache_manager
from components import chart_config

def render_main_content():
    st.header("Data Overview")

    data = st.session_state.get("data")

    if data is not None:
        # Display a glimpse of the data
        st.subheader("Data Glimpse")
        st.dataframe(data.head(10))

        # Display column information
        st.subheader("Column Information")
        col_info = get_column_info(data)
        st.table(col_info)

        # Display basic statistics
        st.subheader("Basic Statistics")
        stats = get_basic_statistics(data)
        st.table(stats)

        # Placeholder for charts
        if "charts" in st.session_state and st.session_state["charts"]:
            st.header("Your Charts")
            for idx, chart in enumerate(st.session_state["charts"], start=1):
                with st.expander(f"{chart['type']} Chart {idx}", expanded=True):
                    # Render the chart using Plotly
                    with st.spinner("Generating chart..."):
                        fig = generate_plotly_chart(data, chart)
                    st.plotly_chart(fig, use_container_width=True)

                    # Provide configuration options
                    with st.expander("Configure Chart", expanded=False):
                        chart_config.configure_chart(idx - 1, chart)

                    # Option to reset configurations
                    if st.button("Reset to Default", key=f"reset_{idx}"):
                        st.session_state["charts"][idx - 1]["config"] = {}
                        st.experimental_rerun()

    else:
        st.info("Please upload a data file or enter a data URL in the sidebar to get started.")

def get_column_info(data: pd.DataFrame) -> pd.DataFrame:
    """Generates a DataFrame containing column information."""
    col_info = pd.DataFrame({
        "Column Name": data.columns,
        "Data Type": data.dtypes.astype(str),
        "Missing Values": data.isnull().sum(),
        "Unique Values": data.nunique()
    })
    return col_info

def get_basic_statistics(data: pd.DataFrame) -> pd.DataFrame:
    """Generates basic statistics for numerical columns."""
    if data.select_dtypes(include=['number']).empty:
        return pd.DataFrame({"Message": ["No numerical columns to display statistics."]})

    stats = data.describe().T
    stats = stats.rename(columns={
        "count": "Count",
        "mean": "Mean",
        "std": "Std Dev",
        "min": "Min",
        "25%": "25%",
        "50%": "Median",
        "75%": "75%",
        "max": "Max"
    }).reset_index().rename(columns={"index": "Column"})

    return stats

def generate_plotly_chart(data: pd.DataFrame, chart: dict):
    """Generates a Plotly chart based on the chart configuration."""
    chart_type = chart.get("type")
    config = chart.get("config", {})

    # Apply Maximum Data Points
    max_data_points = config.get("max_data_points", 100)
    if max_data_points < len(data):
        data = data.head(max_data_points)

    # Apply Sorting
    sort_order = config.get("sort_order", "None")
    sort_by = config.get("sort_by", data.columns[0]) if sort_order != "None" else None
    if sort_order != "None" and sort_by:
        ascending = True if sort_order == "Ascending" else False
        data = data.sort_values(by=sort_by, ascending=ascending)

    # Axis Configuration
    if chart["type"] in ["Bar Chart", "Line Chart", "Scatter Plot"]:
        x_axis = config.get("x_axis", data.columns[0])
        y_axis = config.get("y_axis", data.columns[1] if data.shape[1] > 1 else data.columns[0])
    elif chart["type"] == "Pie Chart":
        names = config.get("names", data.columns[0])
        values = config.get("values", data.columns[1] if data.shape[1] > 1 else data.columns[0])

    # Base Plotly Express chart
    if chart_type == "Bar Chart":
        fig = px.bar(
            data,
            x=x_axis,
            y=y_axis,
            title=config.get("title", "Bar Chart"),
            color_discrete_sequence=[config.get("color", "#1f77b4")]
        )
    elif chart_type == "Line Chart":
        fig = px.line(
            data,
            x=x_axis,
            y=y_axis,
            title=config.get("title", "Line Chart"),
            color_discrete_sequence=[config.get("color", "#1f77b4")],
            markers=True if chart.get("config", {}).get("marker_size", 10) else False
        )
    elif chart_type == "Pie Chart":
        fig = px.pie(
            data,
            names=names,
            values=values,
            title=config.get("title", "Pie Chart"),
            color_discrete_sequence=[config.get("color", "#1f77b4")]
        )
    elif chart_type == "Scatter Plot":
        fig = px.scatter(
            data,
            x=x_axis,
            y=y_axis,
            title=config.get("title", "Scatter Plot"),
            color_discrete_sequence=[config.get("color", "#1f77b4")],
            size=[config.get("marker_size", 10)] * len(data)  # Uniform marker size
        )
    else:
        fig = px.scatter(title="Unsupported Chart Type")

    # Apply additional configurations
    fig.update_layout(
        title={
            'text': config.get("title", ""),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        plot_bgcolor=config.get("background_color", "#ffffff"),
        showlegend=config.get("show_legend", True)
    )

    # Update gridlines and ticks
    fig.update_xaxes(showgrid=config.get("show_grid", True), showticklabels=config.get("show_ticks", True))
    fig.update_yaxes(showgrid=config.get("show_grid", True), showticklabels=config.get("show_ticks", True))

    # Add Subtitle if available
    subtitle = config.get("subtitle", "")
    if subtitle:
        fig.add_annotation(
            text=subtitle,
            xref="paper", yref="paper",
            x=0.5, y=-0.15,
            showarrow=False,
            font=dict(size=12),
            align="center"
        )

    return fig