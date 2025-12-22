import streamlit as st
from utils.data_loader import get_data

df = get_data()

st.header("Global")
col1, col2, col3 = st.columns(3)
col1.metric("Total deprecated dependenceis", f"{df['dep_count'].sum():,}")
# col2.metric("Total APIs Analized", df['api_spec_id'].nunique())
col3.metric("Ecosystems", df['language'].nunique())

st.bar_chart(df.groupby('language')['dep_count'].sum())