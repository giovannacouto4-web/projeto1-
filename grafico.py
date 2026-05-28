import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Marcas de Moda", page_icon="👗", layout="centered")

df = pd.read_csv("marcas_moda.csv")

# Nome legível para cada coluna técnica
colunas = {
    "seguidores_instagram_milhoes": "Seguidores no Instagram (milhões)",
    "buscas_google_milhoes":        "Buscas no Google (milhões/mês)",
    "avaliacao_media":              "Avaliação dos clientes (0 a 5)",
    "preco_medio_brl":              "Preço médio dos produtos (R$)",
}

explicacoes = {
    "seguidores_instagram_milhoes": {
        "cor": "#e63946",
        "texto": (
            "Cada barra mostra quantos milhões de pessoas seguem a marca no Instagram. "
            "Quanto maior a barra, mais a marca está presente na vida das pessoas nas redes sociais. "
            "Marcas esportivas como Nike e Adidas costumam liderar porque faturam muito com conteúdo de estilo de vida, "
            "não só roupa."
        ),
    },
    "buscas_google_milhoes": {
        "cor": "#f4a261",
        "texto": (
            "Cada barra mostra quantas vezes por mês as pessoas pesquisam a marca no Google. "
            "Isso indica curiosidade e intenção de compra. "
            "Uma marca com muitas buscas está na cabeça das pessoas — elas querem saber preços, coleções e novidades."
        ),
    },
    "avaliacao_media": {
        "cor": "#2a9d8f",
        "texto": (
            "Cada barra mostra a nota média que os clientes deram para a marca, de 0 a 5. "
            "Essa nota considera qualidade do produto, atendimento e experiência de compra. "
            "Marcas de luxo como Gucci e Louis Vuitton tendem a ter notas altas porque o cliente paga mais "
            "e espera (e recebe) um atendimento impecável."
        ),
    },
    "preco_medio_brl": {
        "cor": "#457b9d",
        "texto": (
            "Cada barra mostra o preço médio de uma peça da marca, em reais. "
            "Dá pra ver claramente a diferença entre marcas populares e acessíveis (como Shein e Renner) "
            "e marcas de luxo (como Louis Vuitton e Gucci), onde uma única peça pode custar milhares de reais."
        ),
    },
}

st.title("👗 Marcas de Moda — Quem está em alta?")
st.write("Escolha o que você quer comparar entre as marcas e veja o gráfico com uma explicação simples.")
st.divider()

col_selecionada = st.selectbox(
    "O que você quer comparar?",
    options=list(colunas.keys()),
    format_func=lambda k: colunas[k],
)

info = explicacoes[col_selecionada]
nome_legivel = colunas[col_selecionada]

df_ordenado = df.sort_values(col_selecionada, ascending=False)

fig = px.bar(
    df_ordenado,
    x="marca",
    y=col_selecionada,
    labels={"marca": "Marca", col_selecionada: nome_legivel},
    color_discrete_sequence=[info["cor"]],
    text_auto=".1f",
)
fig.update_layout(
    title=dict(text=nome_legivel, font=dict(size=18)),
    xaxis_tickangle=-30,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    showlegend=False,
    font=dict(size=13),
)
fig.update_traces(marker_line_width=0)

st.plotly_chart(fig, use_container_width=True)
st.info(info["texto"])

with st.expander("📋 Ver tabela completa"):
    st.dataframe(
        df[["marca"] + list(colunas.keys())].rename(columns={"marca": "Marca", **colunas}),
        use_container_width=True,
        hide_index=True,
    )

st.caption("Dados fictícios para fins didáticos · feito com Streamlit")
