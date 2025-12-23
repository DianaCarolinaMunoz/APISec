import streamlit as st
from utils.data_loader import get_data
from utils.plots import plot_by_language

data = get_data()

df_total = data["total"]


st.header("Total Dependencies Evolution per Ecosystem")

lenguaje = st.selectbox("Select", sorted(df_total['language'].unique()))


group_by = st.radio(
    "view by:",
    options=["day", "month", "year"],
    format_func=lambda x: {"day": "day", "month": "month", "year": "Year (Stacked)"}[x],
    horizontal=True
)

fig = plot_by_language(df_total, lenguaje, group_by=group_by)
st.plotly_chart(fig, use_container_width=True)

total = df_total[df_total['language'] == lenguaje]['dep_count'].sum()
st.metric(f"Total dependencies {lenguaje}", f"{total:,}")