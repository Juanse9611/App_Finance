import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Valoraciones Russell 1000", layout="wide")
st.title("Análisis de Valoraciones - Russell 1000")

# Cargar datos desde el Excel
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_excel("Russell_1000_Valoraciones.csv")
        return df
    except FileNotFoundError:
        st.error("No se encontró el archivo. Asegúrate de tener 'Russell_1000_Valoraciones.csv' en el mismo directorio.")
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    st.sidebar.header("Filtros")

    empresas = st.sidebar.multiselect("Selecciona empresas", options=df['empresa'].unique(), default=df['empresa'].unique())

    df_filtrado = df[df['empresa'].isin(empresas)]

    st.subheader("📊 Tabla de Valoraciones")
    st.dataframe(df_filtrado)

    st.subheader("📈 PER Promedio por Empresa")
    fig1 = px.bar(df_filtrado, x="empresa", y="PER Promedio", color="empresa", title="PER Promedio por Empresa")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("📉 Comparación Precio Actual vs Objetivo")
    fig2 = px.bar(df_filtrado, x="empresa", y=["Precio Actual", "Precio Objetivo"], barmode="group", title="Precio Actual vs Objetivo")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("🎯 Distribución de Diferencia (%) entre precios")
    fig3 = px.histogram(df_filtrado, x="diff", nbins=30, title="Distribución del diff (%)")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.stop()
