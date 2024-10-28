import streamlit as st
import pandas as pd
from datetime import datetime
from st_keyup import st_keyup
from matplotlib import pyplot as plt
from streamlit_option_menu import option_menu
import time

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

    st.markdown(
        body="""<h1 style="text-align: center; color: #1c95cd;">Análisis de abandono de carrito</h1>""",
        unsafe_allow_html=True
    )
    
with col2:    
    st.markdown(
        body="""
        <a href="https://github.com/No-Country-simulation/c21-57-t-data-bi" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" alt="Repositorio" style="width: 50px; height: 50px; filter: invert(1); ">
        </a>
        """,
        unsafe_allow_html=True
        )

# Sidebar para seleccionar pagina
# page = st.sidebar.selectbox("Seleccione una página", ["Informacion","Consultas a df", "Visualizaciones","Resultados del Modelo"])
# Menu de opciones
if 'selected_menu' not in st.session_state:
    st.session_state.selected_menu = "Informacion"

menu = option_menu(menu_title=None,
                   options=["Informacion","Consultas", "Visualizaciones","Resultados del Modelo"],
                   orientation='horizontal',
                   icons=['info-circle','search','file-bar-graph-fill','robot'],
                   menu_icon='cast',
                   default_index=0,
                   styles={
                    "container": {
                        "padding": "0!important",
                        "background-color": "#f0f2f6",  # Fondo del contenedor
                        "border-radius": "5px",
                        "border": "1px solid #dcdcdc",
                    },
                    "icon": {
                        "color": "black",  # Color de icono normal
                        "font-size": "24px",
                        "display": "block",
                        "margin-bottom": "5px"
                    },
                    "nav-link": {
                        "display": "flex",
                        "flex-direction": "column",
                        "align-items": "center",
                        "justify-content": "center",
                        "color": "#3a3a3a",  # Color de texto de los links no seleccionados
                        "font-size": "15px",
                        "padding": "12px 15px",
                        "border-radius": "5px",
                        "--hover-color": "#e0e7f3",
                        "height": "80px"
                    },
                    "nav-link-selected": {
                        "background-color": "#1c95cd",  # Fondo del link seleccionado
                        "color": "#ffffff",  # Color de texto e icono del link seleccionado
                        "border-radius": "5px",
                        "transition": "background-color 0.3s ease",
                    }
        })

st.session_state.selected_menu = menu


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
        col1,col2 = st.columns([1,1])
        with col1:
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
        with col2:
            pais = st.selectbox('Selecciona un país', df_paises, index=0)

        if pais in df_paises and pais != 'Todos':
            df = df[df['Country'] == pais]

        # Buscar transaccion especifica
        transaccion = st_keyup('Buscar Numero de transaccion',value='',debounce=500,key="1",placeholder='Buscar transaccion')

        if transaccion not in ['', None]:
            df = df[df['TransactionNo'].str.contains(transaccion.upper())]
    
        
        # Mostramos el df resultante
        with st.spinner('Cargando...'):
            st.dataframe(df)
        
        # Boton para descargar el dataframe resultante
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.download_button(label='Descargar CSV', data=df.to_csv(index=False), file_name='transacciones.csv', mime='text/csv',icon='⬇️')

        with col2:
            st.download_button(label='Descargar JSON', data=df.to_json(orient='records'), file_name='transacciones.json', mime='application/json', icon='⬇️')

    case "Visualizaciones":
        
        # MUESTRA 1 (GRAFICO 1)
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
                
            st.write("Este grafico muestra la cantidad de transacciones canceladas por país")
            with st.expander("Codigo",expanded=True):
                code = """
                        fig, ax = plt.subplots()
                        df_canceladas['Country'].value_counts().plot(kind='bar', ax=ax)
                        ax.set_title('Transacciones Canceladas por país')
                        ax.set_xlabel('Paises')
                    """
                st.code(code, language='python')
        
        st.divider()
        
        # MUESTRA 2 (GRAFICO 2)
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write("Este grafico muestra la cantidad de transacciones concretadas por país")
            with st.expander("Codigo", expanded=True):
                code = """
                        fig, ax = plt.subplots()
                        df_concretadas['Country'].value_counts().plot(kind='bar', ax=ax)
                        ax.set_title('Transacciones Concretadas por país')
                        ax.set_xlabel('Paises')
                        st.pyplot(fig)
                        """
                st.code(code, language='python')
            
        with col2:
            # Grafico de barras
            fig, ax = plt.subplots()
            df_concretadas['Country'].value_counts().plot(kind='bar', ax=ax)
            ax.set_title('Transacciones Concretadas por país')
            ax.set_xlabel('Paises')
            # mostrar el grafico
            st.pyplot(fig)
        
        st.divider()       
        
        # GRAFICO 3
        # Precio x Cantidad de los productos mas comprados en un pais seleccionado
        st.write("Los 10 productos con mas $ Total recaudado en un país seleccionado")

        df_paises = df_ambas['Country'].unique()
        df_paises = df_paises.tolist()
        # Insertamos un valor para mostrar todos los paises
        df_paises.insert(0, 'Todos')

        # Filtro de país
        pais_seleccionado = st.selectbox('Selecciona un país para ver los productos que mas generaron ganancias', df_paises)

        # Filtrar el dataframe por el país seleccionado
        if pais_seleccionado != 'Todos':
            df = df_ambas[df_ambas['Country'] == pais_seleccionado]
        else:
            df = df_ambas
        # Agrupar por producto y calcular la cantidad total comprada y el precio total
        df_productos = df.groupby('ProductName').agg({'Quantity': 'sum', 'Price': 'sum'}).reset_index()

        # Crear una nueva columna para el total recaudado (Cantidad * Precio)
        df_productos['TotalRecaudado'] = df_productos['Quantity'] * df_productos['Price']

        # Ordenar por TotalRecaudado y agarra los primeros 10
        df_productos = df_productos.sort_values(by='TotalRecaudado', ascending=False).head(10)

        with st.spinner('Cargando...'):
            fig, ax = plt.subplots()
            df_productos_sorted = df_productos.sort_values(by='TotalRecaudado', ascending=True)
            ax.barh(df_productos_sorted['ProductName'], df_productos_sorted['TotalRecaudado']) 
            ax.set_title(f'Precio x Cantidad: Productos que mas recaudaron de {pais_seleccionado}')
            ax.set_xlabel('$ total recaudado')
            ax.set_ylabel('Producto')       
            st.pyplot(fig)
        
        with st.expander("Codigo"):
                code = """
                        fig, ax = plt.subplots()
                        df_productos_sorted = df_productos.sort_values(by='TotalRecaudado', ascending=True)
                        ax.barh(df_productos_sorted['ProductName'], df_productos_sorted['TotalRecaudado']) 
                        ax.set_title(f'Precio x Cantidad de los productos más comprados en {pais_seleccionado}')
                        ax.set_xlabel('$ total recaudado')
                        ax.set_ylabel('Producto')       
                        st.pyplot(fig)
                        """
                st.code(code, language='python')
        
        
                            
    case "Resultados del Modelo":
        
        # st.cache_resource is the recommended way to cache global resources like ML models or database connections. 
        # Use st.cache_resource when your function returns unserializable objects that you don’t want to load multiple times. 
        # It returns the cached object itself, which is shared across all reruns and sessions without copying or duplication. 
        # If you mutate an object that is cached using st.cache_resource, that mutation will exist across all reruns and sessions.
        
        st.write('Resultados del Modelo')  
          
st.write('Desarrollado por: [Raphael Nicaise](https://www.linkedin.com/in/rapha%C3%ABl-nicaise-68025b27a/)')