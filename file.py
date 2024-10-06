import os

# Define the project structure
project_structure = {
    "tableau_clone_streamlit": {
        "app.py": "",
        "requirements.txt": "",
        "README.md": "",
        "assets": {
            "icons": {
                "bar_chart.png": "",
                "line_chart.png": "",
                "line_chart.png": "",
                "pie_chart.png": "",
                "scatter_plot.png": "",
                # Add more icons as needed
            }
        },
        "components": {
            "sidebar.py": "",
            "main_content.py": "",
            "chart_creation.py": "",
            "chart_config.py": "",
        },
        "pages": {
            "chart_creation_page.py": "",
        },
        "utils": {
            "data_handler.py": "",
            "cache_manager.py": "",
            "config.py": "",
        },
        "styles": {
            "styles.css": "",
        },
        "tests": {
            "test_data_handler.py": "",
            "test_cache_manager.py": "",
            # Add more test modules as needed
        },
    }
}

# Function to create the directories and files
def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):  # Create a directory
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)  # Recur for subdirectories
        else:  # Create a file
            with open(path, 'w') as f:
                f.write(content)

# Create the project structure in the current directory
create_structure(".", project_structure)
