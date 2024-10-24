import streamlit as st
import pandas as pd
from datetime import datetime
from st_keyup import st_keyup
from matplotlib import pyplot as plt
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Analisis de abandono de carrito", 
                   layout="centered",
                   page_icon="🛒")
                   
@st.cache_data
def load_data()->tuple[pd.DataFrame]:
    """
    Cargamos los datos desde archivo parquet, y los dejamos en memoria
    Returns:
        Tuple[pd.DataFrame]: Devuelve un tuple con 3 dataframes
    """
    df_canceladas = pd.read_parquet('data/silver/transacciones_canceladas.parquet')
    df_concretadas = pd.read_parquet('data/silver/transacciones_concretadas.parquet')
    df_ambas = pd.concat([df_canceladas, df_concretadas])
    return df_canceladas, df_concretadas, df_ambas

df_canceladas, df_concretadas, df_ambas = load_data()

col1, col2 = st.columns([4, 1])
with col1:
    st.title('Analisis de abandono de carrito')
with col2:    
    st.markdown(
        body="""
        <a href="https://github.com/RaphaelNicaise/c21-57-t-data-bi" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="Repositorio" style="width: 50px; height: 50px; filter: invert(1);">
        </a>
        """,
        unsafe_allow_html=True
        )

# Sidebar para seleccionar pagina
# page = st.sidebar.selectbox("Seleccione una página", ["Informacion","Consultas a df", "Visualizaciones","Resultados del Modelo"])
# Menu de opciones
menu = option_menu(menu_title=None,
                   options=["Informacion","Consultas", "Visualizaciones","Resultados del Modelo"],
                   orientation='horizontal',
                   icons=['info-circle','search','file-bar-graph-fill','robot'],
                   menu_icon='cast',
                   default_index=0)


match menu:
    case "Informacion":
        st.write('Informacion')
        with open('README.md', 'r', encoding='utf-8') as file:
            # Ignorar las primeras 2 lineas
            for _ in range(2):
                next(file)
            readme_content = file.read()
        st.markdown(readme_content)
        
    case "Consultas":
    #Filtro de tipo de compra
        opcion = st.selectbox('Selecciona un tipo de compra', ['Ambas','Canceladas','Concretadas'])
        match opcion:
            case 'Ambas':
                df = df_ambas
            case 'Canceladas':
                df = df_canceladas
            case 'Concretadas':
                df = df_concretadas

        df_paises = df['Country'].unique()
        df_paises = df_paises.tolist()
        # Insertamos un valor para mostrar todos los paises
        df_paises.insert(0, 'Todos')

        # Filtro de pais, DEFAULT: Todos
        pais = st.selectbox('Selecciona un país', df_paises, index=0)

        if pais in df_paises and pais != 'Todos':
            df = df[df['Country'] == pais]

        # Buscar transaccion especifica
        transaccion = st_keyup('Buscar Numero de transaccion',value='',debounce=500,key="1",placeholder='Buscar transaccion')

        if transaccion not in ['', None]:
            df = df[df['TransactionNo'].str.contains(transaccion.upper())]
            
        # Mostramos el df resultante
        st.dataframe(df)

        # Boton para descargar el dataframe resultante
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.download_button(label='Descargar CSV', data=df.to_csv(index=False), file_name='transacciones.csv', mime='text/csv',icon='⬇️')

        with col2:
            st.download_button(label='Descargar JSON', data=df.to_json(orient='records'), file_name='transacciones.json', mime='application/json', icon='⬇️')

    case "Visualizaciones":
        
        col1, col2 = st.columns([1, 1])
        with col1:   
            # Grafico de barras
            fig, ax = plt.subplots()
            df_canceladas['Country'].value_counts().plot(kind='bar', ax=ax)
            ax.set_title('Transacciones Canceladas por país')
            ax.set_xlabel('Paises')
            # mostrar el grafico
            st.pyplot(fig)
        with col2:
            pass
            
    case "Resultados del Modelo":
        
        # st.cache_resource is the recommended way to cache global resources like ML models or database connections. 
        # Use st.cache_resource when your function returns unserializable objects that you don’t want to load multiple times. 
        # It returns the cached object itself, which is shared across all reruns and sessions without copying or duplication. 
        # If you mutate an object that is cached using st.cache_resource, that mutation will exist across all reruns and sessions.
        
        st.write('Resultados del Modelo')  
          
st.write('Desarrollado por: [Raphael Nicaise](https://www.linkedin.com/in/rapha%C3%ABl-nicaise-68025b27a/)')