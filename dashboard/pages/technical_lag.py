import streamlit as st
import pandas as pd
from utils.data_loader import get_data
from utils.plots_lag import plot_adoption_lag_matplotlib 
from threading import RLock

_lock = RLock()

@st.cache_data(ttl=3600)
def prepare_adoption_lag():
    raw = get_data()
    
    df_adopt = raw["lag_csv"].copy()
    
   
    if "repo" not in df_adopt.columns:
        df_adopt["repo"] = df_adopt["api_spec_id"].astype(str)  
    
    df_adopt_ok = df_adopt[
        (df_adopt["adopted"] == True) &
        (df_adopt["adoption_lag_days"].notna())
    ].copy()
    
    return df_adopt_ok

df_adopt_ok = prepare_adoption_lag()

st.title("Project Adoption Lag Analysis")

if df_adopt_ok.empty:
    st.warning("Not data found")
else:
    tab1, tab2 = st.tabs(["Adoption Lag", "Summary"])

    with tab1:
        if not df_adopt_ok.empty:
            with _lock:
                fig = plot_adoption_lag_matplotlib(df_adopt_ok)
            st.pyplot(fig)  
        else:
            st.info("No data to plot")

    with tab2:
        repos_adoptaron = df_adopt_ok['repo'].nunique() if 'repo' in df_adopt_ok.columns else "N/A"
        adoption_median = f"{df_adopt_ok['adoption_lag_days'].median():.1f}" if not df_adopt_ok.empty else "N/A"
        
        st.markdown(f"""
        ### Summary Statistics
        - **Repos that adopted at least one fix** : {repos_adoptaron}  
        - **Median adoption lag (only adopted)** : {adoption_median} days
        """)