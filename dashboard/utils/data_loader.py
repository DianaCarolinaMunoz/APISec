import streamlit as st
import pandas as pd
import os

@st.cache_data(ttl=3600)
def load_data():

    file_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_dir = os.path.dirname(file_dir)
    project_root = os.path.dirname(dashboard_dir)
    csv_path = os.path.join(project_root, "data", "deprecated_deps_per_api_lang_classification.csv")
    
    # st.write(f"Intentando cargar CSV desde: {csv_path}")
    # st.write(f"¿Existe el archivo?: {os.path.exists(csv_path)}")
    
    if not os.path.exists(csv_path):
        st.error(f"Not CSV Found in: {csv_path}")
        st.stop()  
    
    df = pd.read_csv(csv_path)
    
    if 'commit_date_norm' in df.columns:
        df['commit_date'] = pd.to_datetime(df['commit_date_norm']).dt.date
    elif 'commit_date' in df.columns:
        df['commit_date'] = pd.to_datetime(df['commit_date']).dt.date
    else:
        st.error("Not column (commit_date o commit_date_norm)")
        return pd.DataFrame()
    
    return df

def get_data():
    return load_data()