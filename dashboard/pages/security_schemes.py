import streamlit as st
from utils.data_loader import get_data
from utils.plots_sec import plot_security_by_language



st.title("OpenAPI Security Schemes Evolution")
# st.markdown("""((""")

data = get_data()
st.write("Claves disponibles en data:", list(data.keys()))


if "sec" not in data:
    st.error("¡'sec' NO está en el diccionario devuelto por get_data()!")
    st.stop()

df_sec = data["sec"]

data = get_data()
df_sec = data["sec"]


languages_available = sorted(df_sec['language'].unique())
selected_language = st.selectbox(
    "Select Language",
    options=languages_available,
    index=languages_available.index('python') if 'python' in languages_available else 0
)


fig = plot_security_by_language(df=df_sec,language=selected_language,height=600)

if fig is not None:
    st.plotly_chart(fig, use_container_width=True)
    
    # Opcional: mostrar tabla debajo
    if st.checkbox("Show Data Table"):
        table = df_sec[df_sec['language'] == selected_language].pivot(
            index='year_str',
            columns='auth_group',
            values='count'
        ).fillna(0).astype(int)
        st.dataframe(table.style.format("{:,}"))