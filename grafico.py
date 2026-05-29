import streamlit as st
import pandas as pd
import plotly.express as px
 
df = pd.read_csv("marcas_moda.csv", encoding="utf-8-sig")
df.columns = df.columns.str.strip()
 
st.write("Colunas encontradas:", df.columns.tolist())
 
st.title("👗 Marcas de Moda")
 
colunas_disponiveis = [c for c in df.columns if c != "marca"]
 
variavel = st.selectbox("Escolha o que comparar:", colunas_disponiveis)
 
df_ordenado = df.sort_values(variavel, ascending=False)
 
fig = px.bar(df_ordenado, x="marca", y=variavel)
st.plotly_chart(fig, use_container_width=True)
 
 
