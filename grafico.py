import streamlit as st
import pandas as pd
import plotly.express as px

# configuração da página
st.set_page_config(page_title="Gráfico de Moda")

# ler o arquivo CSV
df = pd.read_csv("marcas_moda.csv")

# título
st.title("Marcas de Moda")

# escolher coluna
coluna = st.selectbox(
    "Escolha o gráfico:",
    [
        "seguidores_instagram_milhoes",
        "buscas_google_milhoes",
        "avaliacao_media",
        "preco_medio_brl"
    ]
)

# criar gráfico
fig = px.bar(
    data_frame=df,
    x="marca",
    y=coluna,
    text=coluna
)

# mostrar gráfico
st.plotly_chart(fig, use_container_width=True)
