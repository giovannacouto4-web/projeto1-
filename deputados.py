import streamlit as st
import pandas as pd 
df = pd.read_csv('deputados_2022.csv')

st.title("Consulta aos deputados de 2022")

partidos = df["partido"].unique()

partidos = st.text_input('Digite o partido que você queira ver os deputados:')
uf = st.text_input('Digite a UF')

if partido:
  df_filtrado = df[df['partido'] == partido.upper()]
if partidos:
  df_filtrado = df[df['partido'] == partidos.upper()]
else: 
  df_filtrado = df

if uf: 
  df_filtrado = df_filtrado[df_filtrado['uf'] == uf.upper()]

st.dataframe(df_filtrado)
