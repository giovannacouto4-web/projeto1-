import streamlit as st
import pandas as pd
 
df = pd.read_csv("marcas_moda.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()
 
st.title("👗 Marcas de Moda")
 
variavel = st.selectbox("Escolha o que comparar:", [
    "seguidores_instagram_milhoes",
    "buscas_google_milhoes",
    "avaliacao_media",
    "preco_medio_brl"
])
 
st.bar_chart(df.set_index("marca")[variavel])
 
 
