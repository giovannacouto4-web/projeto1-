import streamlit as st
import pandas as pd 
df = pd.read_csv('deputados_2022.csv')

partidos = df["partido"].unique()

partido_selecionado = st.selectbox("Escolha um partido:", partidos)

deputados_filtrados = df[df["partido"] == partido_selecionado]

st.dataframe(deputados_filtrados)
