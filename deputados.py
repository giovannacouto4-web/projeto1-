import streamlit as st
import pandas as pd 
df = pd.read_csv('deputados_2022.csv')
st.title("Consulta aos deputados de 2022")

partidos = df["partido"].unique()

partido_selecionado = st.selectbox("Escolha um partido:", partidos)

deputados_filtrados = df[df["partido"] == partido_selecionado]

st.dataframe(deputados_filtrados)

partidos = st.text_input('Digite o partido que você queira ver os deputados:')
uf = st.text_input('Digite a UF')

if sigla:
  df_filtrado = df[df['partido'] == sigla.upper()]
else: 
  df_filtrado = df
  
if uf: 
  df_filtrado = df_filtrado[df_filtrado['uf'] == uf.upper()]
