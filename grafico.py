import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Marcas de Moda")

df = pd.read_csv("dados_moda.csv", sep=";")

# remove espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

st.title("Análise de Marcas de Moda")

opcao = st.selectbox(
    "Escolha o que visualizar:",
    [
        "Seguidores no Instagram",
        "Buscas no Google",
        "Avaliação Média",
        "Preço Médio"
    ]
)

colunas = {
    "Seguidores no Instagram": "seguidores_instagram_milhoes",
    "Buscas no Google": "buscas_google_milhoes",
    "Avaliação Média": "avaliacao_media",
    "Preço Médio": "preco_medio_brl"
}

fig = px.bar(
    df,
    x="marca",
    y=colunas[opcao]
)

st.plotly_chart(fig, use_container_width=True)
