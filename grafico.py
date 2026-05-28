import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Clima do Rio", page_icon="🌤️", layout="centered")

df = pd.read_csv("dados_temperatura.csv")

st.title("🌤️ Como foi o clima mês a mês?")
st.write("Escolha o que você quer visualizar e veja o gráfico com uma explicação simples.")
st.divider()

opcao = st.selectbox(
    "O que você quer ver?",
    ["Temperatura (°C)", "Umidade (%)", "Chuva (mm)"]
)

explicacoes = {
    "Temperatura (°C)": {
        "titulo": "🌡️ Temperatura média do mês, em graus Celsius",
        "texto": "Cada barra mostra o quanto fez calor (ou frio) naquele mês. "
                 "Barras mais altas = meses mais quentes. Barras mais baixas = meses mais frescos. "
                 "Dá pra ver claramente que o verão (dezembro a março) é bem mais quente que o inverno (junho a agosto).",
        "cor": "#e63946"
    },
    "Umidade (%)": {
        "titulo": "💧 Umidade do ar, em porcentagem",
        "texto": "A umidade mostra o quanto de água tem no ar. "
                 "Quando está perto de 100%, o ar está muito úmido — aquela sensação de abafamento que a gente conhece bem no Rio. "
                 "Quando está baixo, o ar fica seco e pode irritar a garganta e os olhos.",
        "cor": "#457b9d"
    },
    "Chuva (mm)": {
        "titulo": "🌧️ Quantidade de chuva no mês, em milímetros",
        "texto": "Cada barra mostra o quanto choveu naquele mês. "
                 "1 milímetro de chuva equivale a 1 litro de água por metro quadrado. "
                 "Os meses de verão têm barras bem mais altas porque é quando mais chove no Rio — "
                 "o calor e a umidade juntos formam as famosas chuvas de verão.",
        "cor": "#2a9d8f"
    }
}

info = explicacoes[opcao]

fig = px.bar(
    df,
    x="Data",
    y=opcao,
    title=info["titulo"],
    color_discrete_sequence=[info["cor"]],
    text_auto=".1f",
)
fig.update_layout(
    xaxis_title="Mês",
    yaxis_title=opcao,
    xaxis_tickangle=-45,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
    font=dict(size=13),
)
fig.update_traces(marker_line_width=0)

st.plotly_chart(fig, use_container_width=True)

st.info(info["texto"])

st.caption("Dados fictícios para fins didáticos · feito com Streamlit")
