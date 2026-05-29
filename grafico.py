import streamlit as st
import pandas as pd
import plotly.express as px
 
df = pd.read_csv("marcas_moda.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()
 
st.title("👗 Marcas de Moda")
 
variavel = st.selectbox("Escolha o que comparar:", [
    "seguidores_instagram_milhoes",
    "buscas_google_milhoes",
    "avaliacao_media",
    "preco_medio_brl"
])
 
df_ordenado = df.sort_values(variavel, ascending=False)
 
fig = px.bar(df_ordenado, x="marca", y=variavel)
st.plotly_chart(fig, use_container_width=True)
 
