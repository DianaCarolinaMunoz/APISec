import streamlit as st
import pandas as pd
from utils.data_loader import get_data
from utils.plots_class_sec import plot_security_by_classification   

data = get_data()
df_class = data["auth_by_class"]

st.header("Security Schemes Evolution per Classification")


lenguaje = st.selectbox(
    "Select Language",
    options=sorted(df_class['language'].unique()),
    index=0 if 'javascript' in df_class['language'].unique() else 0
)


with st.expander("Preview of data (first 10 rows)"):
    st.dataframe(df_class[df_class['language'] == lenguaje].head(10))


fig = plot_security_by_classification(
    df_class,
    language=lenguaje,
    height=650
)

if fig:
    st.plotly_chart(fig, use_container_width=True)

    
    total_schemes = df_class[df_class['language'] == lenguaje]['scheme_count'].sum()
    st.metric(
        label=f"Total Security Schemes in {lenguaje.capitalize()}",
        value=f"{int(total_schemes):,}",
        delta=None  
    )

   
    # total_apis_with_schemes = df_class[df_class['language'] == lenguaje]['api_spec_id'].nunique() if 'api_spec_id' in df_class.columns else "N/A"
    # st.metric("APIs with at least one security scheme", total_apis_with_schemes)