import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análisis Financiero del Russell 1000", layout="wide")
st.title("Análisis Financiero del Russell 1000")

# Cargar los datos procesados (puedes reemplazar esto por tu fuente final)
@st.cache_data
def cargar_datos():
    # Aquí deberías usar el DataFrame final que generaste en el notebook
    try:
        df = pd.read_csv("Russell_1000_Valoraciones.csv")
        return df
    except FileNotFoundError:
        st.error("No se encontró el archivo de datos. Asegúrate de tener 'Russell_1000_Valoraciones.csv' en el mismo directorio.")
        return pd.DataFrame()

# Cargar DataFrame
r1000 = cargar_datos()

if not r1000.empty:
    # Filtros interactivos
    st.sidebar.header("Filtros")
    tickers = st.sidebar.multiselect("Selecciona Tickers", options=r1000['Ticker'].unique(), default=r1000['Ticker'].unique())
    sectores = st.sidebar.multiselect("Selecciona Sectores", options=r1000['Sector'].dropna().unique(), default=r1000['Sector'].dropna().unique())
    anios = st.sidebar.multiselect("Años fiscales", options=sorted(r1000['Año'].unique()), default=sorted(r1000['Año'].unique()))

    df_filtrado = r1000[
        (r1000['Ticker'].isin(tickers)) &
        (r1000['Sector'].isin(sectores)) &
        (r1000['Año'].isin(anios))
    ]

    st.subheader("Datos Filtrados")
    st.dataframe(df_filtrado)

    # Gráfico 1: PER promedio por sector y año
    st.subheader("PER promedio por Sector y Año")
    if not df_filtrado.empty:
        per_sector = df_filtrado.groupby(['Sector', 'Año'])['PER'].mean().reset_index()
        fig = px.line(per_sector, x="Año", y="PER", color="Sector", markers=True)
        st.plotly_chart(fig, use_container_width=True)

    # Gráfico 2: Comparativa entre empresas seleccionadas
    st.subheader("Comparativa PER por Empresa")
    per_empresa = df_filtrado.groupby(['Ticker', 'Año'])['PER'].mean().reset_index()
    fig2 = px.line(per_empresa, x="Año", y="PER", color="Ticker", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: Distribución del PER
    st.subheader("Distribución del PER")
    fig3 = px.histogram(df_filtrado, x="PER", nbins=50, color="Sector")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.stop()
