import streamlit as st
import pandas as pd

df = pd.read_csv("dados_temperatura.csv", parse_dates=["data"])

st.title("🌡️ Dados Meteorológicos")

variavel = st.selectbox("Escolha a variável:", [
    "temperatura_media_c", "umidade_relativa_pct", "precipitacao_mm"
])

st.line_chart(df.set_index("data")[variavel])
