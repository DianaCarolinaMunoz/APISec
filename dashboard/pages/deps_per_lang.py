import streamlit as st
from utils.data_loader import get_data
from utils.plots import plot_by_language

df = get_data()

st.header("Evolution per Ecosystem")

lenguaje = st.selectbox("Select", sorted(df['language'].unique()))

fig = plot_by_language(df, lenguaje)
st.plotly_chart(fig, use_container_width=True)

total = df[df['language'] == lenguaje]['dep_count'].sum()
st.metric(f"Total deprecated dependencies {lenguaje}", f"{total:,}")