import streamlit as st
from utils.data_loader import get_data
from utils.plots import plot_by_language

data = get_data()

df_deprecated = data["deprecated"]
st.header("Deprecated Dependencies per Ecosystem")

lenguaje = st.selectbox("Select", sorted(df_deprecated['language'].unique()))


group_by = st.radio(
    "view by:",
    options=["day", "month", "year"],
    format_func=lambda x: {"day": "day", "month": "month", "year": "Year (Stacked)"}[x],
    horizontal=True
)

fig = plot_by_language(df_deprecated, lenguaje, group_by=group_by)
st.plotly_chart(fig, use_container_width=True)

total = df_deprecated[df_deprecated['language'] == lenguaje]['dep_count'].sum()
st.metric(f"Total deprecated dependencies {lenguaje}", f"{total:,}")