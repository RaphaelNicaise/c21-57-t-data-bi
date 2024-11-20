import streamlit as st
import pandas as pd
from datetime import datetime
from st_keyup import st_keyup
from matplotlib import pyplot as plt
from streamlit_option_menu import option_menu
import time
import numpy as np
import streamlit.components.v1 as components

st.set_page_config(page_title="Analisis de abandono de carrito", 
                   layout="centered",
                   page_icon="🛒"
                   )
                   

@st.cache_resource
def load_model():
    """

    Returns:
    """
    modelo = "path" # cargar modelo como .pkl o .joblib
    return modelo

model = load_model()

@st.cache_data(show_spinner=True)
def load_data()->tuple[pd.DataFrame]:
    """
    Cargamos los datos desde archivo parquet, y los dejamos en memoria
    Returns:
        Tuple[pd.DataFrame]: Devuelve un tuple con 3 dataframes
    """
    try:
        df_canceladas = pd.read_parquet('data/silver/transacciones_canceladas.parquet')
        df_concretadas = pd.read_parquet('data/silver/transacciones_concretadas.parquet')
        df_ambas = pd.concat([df_canceladas, df_concretadas])
    except FileNotFoundError:
        st.error("No se encontraron los archivos parquet en la carpeta data/silver")
        return None, None, None
    
    return df_canceladas, df_concretadas, df_ambas

df_canceladas, df_concretadas, df_ambas = load_data()

global paises
global opciones_paises
    
paises = df_ambas['Country'].unique()
opciones_paises = paises.tolist()
opciones_paises.insert(0, 'Todos')

col1, col2 = st.columns([4, 1])
with col1:

    st.markdown(
        body="""<h1 style="text-align: center; color: #1c95cd;">Análisis de abandono de carrito</h1>""",
        unsafe_allow_html=True,
        
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


        # Filtro de pais, DEFAULT: Todos
        with col2:
            pais = st.selectbox('Selecciona un país', opciones_paises, index=0)

        if pais in opciones_paises and pais != 'Todos':
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
            with st.expander("Codigo"):
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
            with st.expander("Codigo"):
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
        st.write("Los 10 productos con mas £ Totales recaudadas en un país seleccionado")

        # Filtro de país
        pais_seleccionado = st.selectbox('Selecciona un país para ver los productos que mas generaron ganancias', opciones_paises)

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
            ax.set_title(f'Precio £ x Cantidad: Productos que mas recaudaron de {pais_seleccionado}')
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
       
        st.divider()
        
        # GRAFICO 4
        st.write("""
                 El gráfico muestra la cantidad de transacciones realizadas cada mes. Cada punto en la línea indica cuántas transacciones ocurrieron en un mes específico, 
                 y la línea conecta estos puntos para mostrar cómo cambian las transacciones con el tiempo. """)
        
        df_ambas['Date'] = pd.to_datetime(df_ambas['Date'])
        df_ambas['Month'] = df_ambas['Date'].dt.to_period('M')

        # Contar transacciones por mes
        transactions_per_month = df_ambas['Month'].value_counts().sort_index()

        # Crear el gráfico
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(transactions_per_month.index.astype(str), transactions_per_month, marker='o', color='orange')
        ax.set_title("Transacciones por Mes")
        ax.set_xlabel("Mes")
        ax.set_ylabel("Cantidad de Transacciones")
        ax.tick_params(axis='x', rotation=45)  # Rotar etiquetas del eje x
        plt.tight_layout()  # Ajustar el layout

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
        with st.expander("Codigo"):
            code = """
                    df_ambas['Date'] = pd.to_datetime(df_ambas['Date'])
                    df_ambas['Month'] = df_ambas['Date'].dt.to_period('M')

                    transactions_per_month = df_ambas['Month'].value_counts().sort_index()

                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.plot(transactions_per_month.index.astype(str), transactions_per_month, marker='o', color='orange')
                    ax.set_title("Transacciones por Mes")
                    ax.set_xlabel("Mes")
                    ax.set_ylabel("Cantidad de Transacciones")
                    ax.tick_params(axis='x', rotation=45)
                    plt.tight_layout()
                    st.pyplot(fig)"""
            st.code(code, language='python')
        st.divider()
        
        # Grafico 5
        
        col1, col2 = st.columns([1, 1])
        with col1:
            
            df_ambas['Status'] = df_ambas['TransactionNo'].apply(lambda x: 'Cancelado' if str(x).startswith('C') else 'Concretado')            
            transaction_counts = df_ambas['Status'].value_counts()

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(transaction_counts.index, transaction_counts.values, color=['green', 'red'])            
            ax.set_title("Cantidad de Transacciones: Concretadas vs. Canceladas")
            ax.set_xlabel("Estado de la Transacción")
            ax.set_ylabel("Cantidad de Transacciones")
            ax.set_xticks(transaction_counts.index)  

            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.write("Este gráfico muestra la cantidad de transacciones concretadas y canceladas.")
            with st.expander("Codigo"):
                code = """
            
                    df_ambas['Status'] = df_ambas['TransactionNo'].apply(lambda x: 'Cancelado' if str(x).startswith('C') else 'Concretado')
                    transaction_counts = df_ambas['Status'].value_counts()
                    
                    fig, ax = plt.subplots(figsize=(8, 6))

                    ax.bar(transaction_counts.index, transaction_counts.values, color=['green', 'red'])
                    ax.set_title("Cantidad de Transacciones: Concretadas vs. Canceladas")
                    ax.set_xlabel("Estado de la Transacción")
                    ax.set_ylabel("Cantidad de Transacciones")
                    ax.set_xticks(transaction_counts.index) 

                    plt.tight_layout()

                    st.pyplot(fig)
                """
                st.code(code, language='python')
        
        st.divider()
        
        
        col1,col2 = st.columns([2,1])
        # GRAFICO 6
        with col1:
            producto_seleccionado = st.selectbox("Producto", df_ambas['ProductName'].unique())

            df_producto = df_ambas[df_ambas['ProductName'] == producto_seleccionado]
            
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df_producto['Price'], bins=20, color='skyblue', edgecolor='black')
            ax.set_title(f'Histograma de Precios: {producto_seleccionado}')
            ax.set_xlabel('Precio')
            ax.set_ylabel('Frecuencia')
            ax.grid(axis='y', alpha=0.75)
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.write("Este gráfico muestra la distribución de precios para un producto seleccionado. Osea la cantidad de veces que se vendió un producto a un precio determinado.")
            with st.expander("Codigo"):
                code = """
                producto_seleccionado = st.selectbox("Producto", df_ambas['ProductName'].unique())

                df_producto = df_ambas[df_ambas['ProductName'] == producto_seleccionado]
                
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.hist(df_producto['Price'], bins=20, color='skyblue', edgecolor='black')
                ax.set_title(f'Histograma de Precios: {producto_seleccionado}')
                ax.set_xlabel('Precio')
                ax.set_ylabel('Frecuencia')
                ax.grid(axis='y', alpha=0.75)
                plt.tight_layout()
                st.pyplot(fig)
                """
                st.code(code, language='python')
        
        st.divider()
        
        # Grafico 7
        df_canceladas['Date'] = pd.to_datetime(df_canceladas['Date'])

        df_canceladas['Month'] = df_canceladas['Date'].dt.to_period('M')
        transacciones_por_mes_canceladas = df_canceladas.groupby('Month').size()

        fig, ax = plt.subplots(figsize=(12, 6))
        transacciones_por_mes_canceladas.plot(kind='bar', ax=ax, color='red')

        ax.set_title('Cantidad de Transacciones Canceladas por Mes')
        ax.set_xlabel('Mes')
        ax.set_ylabel('Cantidad de Transacciones Canceladas')
        ax.set_xticklabels(transacciones_por_mes_canceladas.index.astype(str), rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        
        with st.expander("Codigo"):
            code = """
                df_canceladas['Date'] = pd.to_datetime(df_canceladas['Date'])

                df_canceladas['Month'] = df_canceladas['Date'].dt.to_period('M')
                transacciones_por_mes_canceladas = df_canceladas.groupby('Month').size()

                fig, ax = plt.subplots(figsize=(12, 6))
                transacciones_por_mes_canceladas.plot(kind='bar', ax=ax, color='red')

                ax.set_title('Cantidad de Transacciones Canceladas por Mes')
                ax.set_xlabel('Mes')
                ax.set_ylabel('Cantidad de Transacciones Canceladas')
                ax.set_xticklabels(transacciones_por_mes_canceladas.index.astype(str), rotation=45)
                plt.tight_layout()
                st.pyplot(fig)
            """
            st.code(code, language='python')
         
        st.divider()   
        st.write(""" Basado en el análisis, la tasa de cancelación es muy mínima, en comparación con las concretadas. 
                Se podría decir como recomendación que la empresa ficticia que vende los productos en los distintos lugares del mundo, envíe correos de recordatorios de los carros abandonados para que el usuario siga con la compra. 
            También puede ser implementar encuestas cortas en el sitio para obtener feedback de los usuarios que abandonan su carrito. Preguntar directamente por las razones de su abandono.""")
    
    case "Resultados del Modelo":
            
        # st.cache_resource is the recommended way to cache global resources like ML models or database connections. 
        # Use st.cache_resource when your function returns unserializable objects that you don’t want to load multiple times. 
        # It returns the cached object itself, which is shared across all reruns and sessions without copying or duplication. 
        # If you mutate an object that is cached using st.cache_resource, that mutation will exist across all reruns and sessions.
        st.markdown(
            """
            <style>
            .streamlit-expanderHeader {
                font-size: 24px; /* Cambia a tu tamaño deseado */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.write("El modelo busca predecir si un carrito de compras será concretado o abandonado. Para ello, se han utilizado las siguientes características:")
        
        # Graficos del modelo
        with st.expander("Matriz de Confusion"):
            st.markdown("""
                El modelo ha acertado en:
                - 3798 transacciones completadas (predicciones correctas).
                - 423 transacciones abandonadas (predicciones correctas).
                
                Sin embargo, también cometió algunos errores:

                - 170 transacciones completadas fueron incorrectamente clasificadas como abandonadas.
                - 243 transacciones abandonadas fueron incorrectamente clasificadas como completadas.""")
            
            st.image(
             "ml_developers/images/matrizconfusion.png"
            )
            
        with st.expander("Curva ROC"):
            st.markdown("""
            La curva ROC es una herramienta que ayuda a evaluar el rendimiento de un modelo de clasificación. Un valor de 0.93 indica que el modelo tiene un buen desempeño, ya que se acerca a 1.0, lo que significa que es muy efectivo para distinguir entre las dos clases.                """
            )
            st.image(
                "ml_developers/images/curva_roc.png"
            )
        with st.expander("Precision-Recall"):
            st.markdown("""
                        El gráfico de precisión-recall muestra que, a medida que se utilizan más datos para entrenar el modelo, su precisión disminuye. Actualmente, el modelo tiene una precisión de 0.72, lo que significa que acierta en un 72% de los casos.
                        """)
            st.image(
                "ml_developers/images/precision_recall.png"
            )
        
        with st.expander("Importancia de las caracteristicas"):   
            st.write("El modelo ha determinado que las características más importantes para predecir si un carrito será concretado son:")
            dict_importancia = {
                'Cantidad': 0.20512278629968306,
                'Precio': 0.08292900821104994,
                'Pais': 0.07379439499368336,
                'Precio Promedio': 0.027731145485730177
                }
            
            fig, ax = plt.subplots()
            ax.bar(dict_importancia.keys(), dict_importancia.values())
            ax.set_title('Peso de las caracteristicas a la hora de predecir')
            ax.set_xlabel('Features')
            ax.set_ylabel('Importancia')
            st.pyplot(fig)
        
        
        st.divider()
        # Carrito para predecir
        st.html(
            "<h3 style='text-align: center; color: #1c95cd;'>Simulacion de carrito de compras</h3>"
        )
        class Carrito:
            """
                Clase que representa un carrito de compras, con metodos para agregar, eliminar y obtener los items del carrito
            """
            def __init__(self):
                self.__carrito = []

            def vaciar_carrito(self):
                self.__carrito = []
                
            def agregar_item(self, item: 'ItemCarrito'):
                if not isinstance(item, ItemCarrito):
                    raise ValueError("El item debe ser una instancia de la clase ItemCarrito")
                self.__carrito.append(item)
            
            def eliminar_item(self, item: 'ItemCarrito'):
                if not isinstance(item, ItemCarrito):
                    raise ValueError("El item debe ser una instancia de la clase ItemCarrito")
                if item in self.__carrito:
                    self.__carrito.remove(item)
            
            def obtener_carrito(self):
                return self.__carrito

            def calcular_total_precio(self):
                total = 0
                for item in self.__carrito:
                    total += item.calcular_total()
                return total 
            
            def calcular_cantidad_total(self):
                total = 0
                for item in self.__carrito:
                    total += item.cantidad
                return total
            
            def predecir_carrito(self):
                """
                Simula un modelo de ML para predecir si el carrito va a ser concretado
                """
                # TODO - Implementar modelo de ML para predecir si el carrito va a ser concretado
                cantidad_total = self.calcular_cantidad_total()
                precio_total = self.calcular_total_precio()
                
                st.write(f"Total de productos: {cantidad_total}")
                st.write(f"Total de precio: £{precio_total:,.2f}")
                
                # Simulación de predicción basada en la importancia de las características
                importancia_cantidad = dict_importancia['Cantidad']
                importancia_precio = dict_importancia['Precio']
                importancia_pais = dict_importancia['Pais']
                importancia_precio_promedio = dict_importancia['Precio Promedio']

                # Calcular el precio promedio
                precio_promedio = precio_total / cantidad_total if cantidad_total > 0 else 0

                # Simulación de un umbral de decisión
                umbral = 0.5

                
                puntuacion = (
                    (cantidad_total * importancia_cantidad) +
                    (precio_total * importancia_precio) +
                    (importancia_pais) +  # Asumimos que el país tiene un valor constante
                    (precio_promedio * importancia_precio_promedio)
                )

                
                puntuacion_normalizada = puntuacion / (importancia_cantidad + importancia_precio + importancia_pais + importancia_precio_promedio)

                # Comparar la puntuación normalizada con el umbral
                if puntuacion_normalizada > umbral:
                    return False
                
                return True
            
        class ItemCarrito:
            """
            Clase que representa un item en el carrito de compras
            """
            def __init__(self, producto,cantidad, precio_unitario, pais):
                self.producto = producto
                self.cantidad = cantidad
                self.precio_unitario = precio_unitario
                self.pais = pais
                
            def __str__(self):
                total = self.precio_unitario * self.cantidad
                return f"{self.producto} ({self.pais}) - {self.cantidad} unidades x £{self.precio_unitario:,.2f}/u = £{total:,.2f}"
                
            def calcular_total(self):
                return item.cantidad * item.precio_unitario
        
            
        if not 'carrito' in st.session_state:
            st.session_state.carrito = Carrito()
            
        col1,col2 = st.columns([4,3])
        
        with col1:
            with st.form("formulario-predic"):
                st.html(
                    "<h4 style='text-align: center; color: #1c95cd;'>Agregar producto al carrito</h4>"
                )
                
                producto_seleccionado = st.selectbox("Producto", df_ambas['ProductName'].unique())
                cantidad_productos = st.number_input("Cantidad de Productos", min_value=1, max_value=10000)
                precio_unitario = st.number_input("Precio x Unidad", min_value=1, max_value=10000)
                pais_seleccionado = st.selectbox("Pais", df_ambas['Country'].unique())
                
                item = ItemCarrito(producto_seleccionado,cantidad_productos, precio_unitario, pais_seleccionado)
                
                if st.form_submit_button("Agregar al carrito",icon='🛒',):
                    st.session_state.carrito.agregar_item(item)
            
            if st.button("Predecir carrito", key="predict",type='primary'):
                if len(st.session_state.carrito.obtener_carrito()) == 0:
                    st.error("No hay productos en el carrito")
                else:   
                    
                    if st.session_state.carrito.predecir_carrito():
                        st.success("El carrito va a ser concretado")
                    else:
                        st.error("El carrito no va a ser concretado")
                        
                    st.session_state.carrito.vaciar_carrito()
                       
        with col2:
            with st.container(height=480,border=None):
                st.markdown("""
                            <style>
                            .texto-blanco {
                                color: white;
                            }
                            </style>
                            """, unsafe_allow_html=True)
                
                st.html(
                    "<h4 style='text-align: center; color: #1c95cd;'>Carrito de compras </h4>"
                )
                
                if st.session_state.carrito.obtener_carrito():
                    carrito = st.session_state.carrito.obtener_carrito()
                        
                            
                    for index, item in enumerate(carrito, start=1):
                        st.write(f'<div class="texto-blanco">{index}. {item}</div>', unsafe_allow_html=True)
                            
                    st.divider()   
                        
                    df = pd.DataFrame(carrito)
            if st.button("Limpiar Carrito", key="limpiar",icon='🗑️'):
                        st.session_state.carrito.vaciar_carrito()           
            