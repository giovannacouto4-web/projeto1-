import pandas as pd 
df = pd.read_csv('deputados_2022.csv')

partidos = df["partido"].unique
st.title("Consulta aos deputados de 2022")

st.dataframe(deputados_filtrados)

partidos = st.text_input('Digite o partido que você queira ver os deputados:')
uf = st.text_input('Digite a UF')

if partidos:
  df_filtrado = df[df['partido'] == partidos.upper()]
else: 
  df_filtrado = df

if uf: 
  df_filtrado = df_filtrado[df_filtrado['uf'] == uf.upper()]

st.dataframe(df_filtrado)
