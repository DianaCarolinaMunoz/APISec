import streamlit as st
from utils.data_loader import get_data

data = get_data()

df_deprecated = data["deprecated"]
df_total = data["total"]

st.header("Global")
col1, col2 = st.columns(2)
col1.metric("Total dependenceis", f"{df_total['dep_count'].sum():,}")
col2.metric("Ecosystems", df_total['language'].nunique())

is_clicked = st.button("click")

st.bar_chart(df_total.groupby('language')['dep_count'].sum())
