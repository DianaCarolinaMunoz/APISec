import streamlit as st
import pandas as pd
import os
import json

@st.cache_data(ttl=3600)
def load_data():

    file_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_dir = os.path.dirname(file_dir)
    project_root = os.path.dirname(dashboard_dir)

    #paths to data
    csv_deprecated = os.path.join(project_root, "data", "deprecated_deps_per_api_lang_classification.csv")
    csv_gone = os.path.join(project_root, "data", "gone_deps_per_api_lang_classification.csv")
    csv_vulnerable = os.path.join(project_root, "data", "vuln_deps_per_api_lang_classification.csv")
    csv_total = os.path.join(project_root, "data", "total_deps_per_api_lang_classification.csv")
    csv_lag = os.path.join(project_root, "data", "apis_adoption_lag.csv")
    csv_sec = os.path.join(project_root, "data", "auth_schemes_evolution.csv")
    csv_auth = os.path.join(project_root, "data", "auth_schemes_evolution_clean.csv")
                                                                                                                                                                
    
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
        st.error("CSV not found:")
        for f in missing_files:
            st.error(f"→ {f}")
        st.stop()  

    # load data
    df_deprecated = pd.read_csv(csv_deprecated)
    df_gone = pd.read_csv(csv_gone)
    df_vulnerable = pd.read_csv(csv_vulnerable)
    df_total = pd.read_csv(csv_total)
    df_lag_csv = pd.read_csv(csv_lag)
    # df_lag_json = pd.read_json(json_api_lag)
    df_sec = pd.read_csv(csv_sec)
    df_auth = pd.read_csv(csv_auth)
    

    
    # with open(json_api_lag, 'r', encoding='utf-8') as f:
    #     df_lag_json = json.load(f)

  
 
    return {
        "deprecated": df_deprecated,
        "gone": df_gone,
        "vulnerable": df_vulnerable,
        "total": df_total,
        "lag_csv": df_lag_csv,
        # "lag_json": df_lag_json
        "sec": df_sec,
        "auth_by_class": df_auth
    }

def get_data():
    return load_data()