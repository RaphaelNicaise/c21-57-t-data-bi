import streamlit as st
import pandas as pd
from datetime import datetime
import io
import xlsxwriter
from st_keyup import st_keyup


st.title('Analisis de abandono de carrito')
opcion = st.selectbox('Selecciona un tipo de compra', ['Canceladas', 'Concretadas'])

df = pd.read_parquet(f'data/silver/transacciones_{opcion.lower()}.parquet')

df_paises = df['Country'].unique()

df_paises = df_paises.tolist()
df_paises.insert(0, 'Todos')

pais = st.selectbox('Selecciona un país', df_paises, index=0)

if pais in df_paises and pais != 'Todos':
    df = df[df['Country'] == pais]

# Buscar transaccion especifica
transaccion = st_keyup('Buscar Numero de transaccion',value='',debounce=500,key="1",placeholder='Buscar transaccion')

if transaccion not in ['', None]:
    df = df[df['TransactionNo'].str.contains(transaccion.upper())]
    
st.dataframe(df)

# Boton para descargar el dataframe resultante
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.download_button(label='Descargar CSV', data=df.to_csv(index=False), file_name='transacciones.csv', mime='text/csv',icon='⬇️')

with col2:
    st.download_button(label='Descargar JSON', data=df.to_json(orient='records'), file_name='transacciones.json', mime='application/json', icon='⬇️')

with col3:
    towrite = io.BytesIO()
    df.to_excel(towrite, index=False, engine='xlsxwriter')
    towrite.seek(0)
    st.download_button(label='Descargar Excel', data=towrite, file_name='transacciones.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',icon='⬇️')

st.write('Desarrollado por: [Raphael Nicaise](https://www.linkedin.com/in/rapha%C3%ABl-nicaise-68025b27a/)')