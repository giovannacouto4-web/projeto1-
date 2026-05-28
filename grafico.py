import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Clima do Rio", layout="centered")

df = pd.read_csv("dados_temperatura.csv")

st.title("Como foi o clima mês a mês?")
st.write("Escolha o que você quer visualizar e veja o gráfico com uma explicação simples.")
st.divider()

opcao = st.selectbox(
    "O que você quer ver?",
    ["Temperatura (°C)", "Umidade (%)", "Chuva (mm)"]
)

explicacoes = {
    "Temperatura (°C)": {
        "titulo": "Temperatura média do mês, em graus Celsius",
        "texto": "Cada barra mostra o quanto fez calor (ou frio) naquele mês. "
                 "Barras mais altas = meses mais quentes. Barras mais baixas = meses mais frescos.",
        "cor": "#e63946"
    },
    "Umidade (%)": {
        "titulo": "Umidade do ar, em porcentagem",
        "texto": "A umidade mostra o quanto de água tem no ar.",
        "cor": "#457b9d"
    },
    "Chuva (mm)": {
        "titulo": "Quantidade de chuva no mês, em milímetros",
        "texto": "Cada barra mostra o quanto choveu naquele mês.",
        "cor": "#2a9d8f"
    }
}

info = explicacoes[opcao]

fig = px.bar(
    df,
    x="Data",
    y=opcao,
    title=info["titulo"],
    color_discrete_sequence=[info["cor"]]
)

fig.update_layout(
    xaxis_title="Mês",
    yaxis_title=opcao,
    xaxis_tickangle=-45,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

st.info(info["texto"])
