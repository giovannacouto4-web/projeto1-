import streamlit as st
import pandas as pd 
df = pd.read_csv('deputados_2022.csv')
st.dataframe(df)

# Pegar lista de partidos únicos
partidos = df["partido"].unique()

# Criar a caixa de seleção
partido_selecionado = st.selectbox("Escolha um partido:", partidos)

# Filtrar os deputados do partido escolhido
deputados_filtrados = df[df["partido"] == partido_selecionado]

# Mostrar resultado
st.dataframe(deputados_filtrados)
