# utils/data_handler.py

import pandas as pd
import requests
from io import StringIO, BytesIO
import json

def load_data(uploaded_file):
    file_type = uploaded_file.type
    if "csv" in file_type:
        return pd.read_csv(uploaded_file)
    elif "excel" in file_type:
        return pd.read_excel(uploaded_file)
    elif "json" in file_type:
        return pd.read_json(uploaded_file)
    else:
        raise ValueError("Unsupported file type")

def load_data_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type')
        if 'csv' in content_type:
            return pd.read_csv(StringIO(response.text))
        elif 'json' in content_type:
            return pd.read_json(StringIO(response.text))
        elif 'excel' in content_type:
            return pd.read_excel(BytesIO(response.content))
        else:
            raise ValueError("Unsupported URL data format")
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from URL: {e}")
        return None
    except ValueError as ve:
        st.error(ve)
        return None
