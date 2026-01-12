import streamlit as st
import pandas as pd
from utils.data_loader import get_data
from utils.plots_lag import plot_adoption_lag_matplotlib  # solo esta función
from threading import RLock

_lock = RLock()

@st.cache_data(ttl=3600)
def prepare_adoption_lag():
    raw = get_data()
    
    # Solo usamos el CSV de adoption lag
    df_adopt = raw["lag_csv"].copy()
    
    # Si necesitas 'repo' pero no tienes el mapeo del JSON, usa un placeholder
    # o agrupa por 'api_spec_id' en lugar de 'repo'
    if "repo" not in df_adopt.columns:
        df_adopt["repo"] = df_adopt["api_spec_id"].astype(str)  # placeholder simple
    
    df_adopt_ok = df_adopt[
        (df_adopt["adopted"] == True) &
        (df_adopt["adoption_lag_days"].notna())
    ].copy()
    
    return df_adopt_ok

# Carga datos
df_adopt_ok = prepare_adoption_lag()

st.title("Project Adoption Lag Analysis")

if df_adopt_ok.empty:
    st.warning("No se encontraron datos de adopción válidos en el CSV.")
else:
    tab1, tab2 = st.tabs(["Adoption Lag", "Resumen"])

    with tab1:
        if not df_adopt_ok.empty:
            with _lock:
                fig = plot_adoption_lag_matplotlib(df_adopt_ok)
            st.pyplot(fig)  # o st.plotly_chart(fig) si usas Plotly
        else:
            st.info("No hay datos para graficar")

    with tab2:
        repos_adoptaron = df_adopt_ok['repo'].nunique() if 'repo' in df_adopt_ok.columns else "N/A"
        adoption_median = f"{df_adopt_ok['adoption_lag_days'].median():.1f}" if not df_adopt_ok.empty else "N/A"
        
        st.markdown(f"""
        ### Resumen
        - **Repos que adoptaron al menos un fix** : {repos_adoptaron}  
        - **Adoption lag mediana (solo adoptados)** : {adoption_median} días
        """)