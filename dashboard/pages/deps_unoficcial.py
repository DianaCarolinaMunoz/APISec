import streamlit as st
from utils.data_loader import get_data
from utils.plots import plot_by_language

data = get_data()

df_gone = data["gone"]
st.header("Gone Dependencies per Ecosystem")

lenguaje = st.selectbox("Select", sorted(df_gone['language'].unique()))
group_by = st.radio(
    "view by:",
    options=["day", "month", "year"],
    format_func=lambda x: {"day": "day", "month": "month", "year": "Year (Stacked)"}[x],
    horizontal=True
)

fig_count = plot_by_language(df_gone, lenguaje, group_by=group_by, mode="count")
st.plotly_chart(fig_count, use_container_width=True)

fig_percent = plot_by_language(df_gone, lenguaje, group_by=group_by, mode="percent")
st.plotly_chart(fig_percent, use_container_width=True)

total = df_gone[df_gone['language'] == lenguaje]['dep_count'].sum()
st.metric(f"Total gone dependencies {lenguaje}", f"{total:,}")