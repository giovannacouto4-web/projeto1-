import streamlit as st
import pandas as pd 
df = pd.read_csv('deputados_2022.csv')
st.dataframe(df)

print(df.columns)
partidos = df["partido"]
st.dataframe(partidos)
partidos = df[["partido"]]
st.dataframe(partidos)
partidos_unicos = df["partido"].unique()
st.write(partidos_unicos)

