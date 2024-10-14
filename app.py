import streamlit as st
import pandas as pd
from datetime import datetime

st.title('Analisis de abandono de carrito')
opcion = st.selectbox('Selecciona un tipo de compra', ['Canceladas', 'Concretadas'])

df = pd.read_parquet(f'data/silver/transacciones_{opcion.lower()}.parquet')
df_fechas = df['Date'].unique()
df_paises = df['Country'].unique()

df_paises = df_paises.tolist()
df_paises.insert(0, 'Todos')

pais = st.selectbox('Selecciona un país', df_paises, index=0)

if pais == 'Todos':
    st.dataframe(df)
elif pais in df_paises:
    st.dataframe(df[df['Country'] == pais])
