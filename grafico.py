```python
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Marcas de Moda")

df = pd.read_csv("dados_moda.csv")

st.title("Análise de Marcas de Moda")

opcao = st.selectbox(
    "Escolha uma opção:",
    [
        "seguidores_instagram_milhoes",
        "buscas_google_milhoes",
        "avaliacao_media",
        "preco_medio_brl"
    ]
)

fig = px.bar(
    df,
    x="marca",
    y=opcao
)

st.plotly_chart(fig)
```
