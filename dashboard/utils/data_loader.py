import streamlit as st
import pandas as pd
import os

@st.cache_data(ttl=3600)
def load_data():

    file_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_dir = os.path.dirname(file_dir)
    project_root = os.path.dirname(dashboard_dir)

    #paths to data
    csv_deprecated = os.path.join(project_root, "data", "deprecated_deps_per_api_lang_classification.csv")
    csv_total = os.path.join(project_root, "data", "total_deps_per_api_lang_classification.csv")

    
    # st.write("Ruta deprecated:", csv_deprecated)
    # st.write("Existe:", os.path.exists(csv_deprecated))
    # st.write("Ruta total:", csv_total)
    # st.write("Existe:", os.path.exists(csv_total))

   
    missing_files = []
    if not os.path.exists(csv_deprecated):
        missing_files.append(csv_deprecated)
    if not os.path.exists(csv_total):
        missing_files.append(csv_total)

    if missing_files:
        st.error("Archivos CSV no encontrados:")
        for f in missing_files:
            st.error(f"→ {f}")
        st.stop()  # Detiene la ejecución de la app

    # load data
    df_deprecated = pd.read_csv(csv_deprecated)
    df_total = pd.read_csv(csv_total)

    # date processing 
    # for df in [df_deprecated, df_total]:
    #     if 'commit_date_norm' in df.columns:
    #         df['commit_date'] = pd.to_datetime(df.columns['commit_date_norm']).dt.date
    #     elif 'commit_date' in df.columns:
    #         df['commit_date'] = pd.to_datetime(df['commit_date']).dt.date

 
    return {
        "deprecated": df_deprecated,
        "total": df_total
    }

def get_data():
    return load_data()