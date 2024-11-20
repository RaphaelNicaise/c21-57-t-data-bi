## c21-57-t-data-bi
# Proyecto: Análisis de Carrito Abandonado
Objetivo: Analizar el comportamiento de los usuarios que
abandonan el carrito de compras en un sitio web de e-commerce para identificar
posibles razones y proponer estrategias de retención.

Streamlit web app: [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=fff)](https://c21-57-t-data-bi-carritoabandonado.streamlit.app/)

Dataset: [![Dataset](https://img.shields.io/badge/Dataset%20Kaggle-00599C?logo=kaggle&logoColor=fff)](https://www.kaggle.com/datasets/gabrielramos87/an-online-shop-business)
## Tabla de Contenidos

- [Colaboradores y Stack del Proyecto](#colaboradores)
- [Instalación y Ejecución](#instalación-y-ejecución)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Streamlit Web App Docs](#streamlit-web-app-docs)

## Colaboradores
- Raphael Nicaise: Data Engineer & Project Manager  [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/RaphaelNicaise) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rapha%C3%ABl-nicaise-68025b27a/)
- Ruth Estefania Puyo: Data Analyst & BI Analyst  [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/ruthpuyo) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ruth-estefania-puyo-929572b0)
- Pamela Cardozo: Data Analyst  [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/PamelaCardozo) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/npamelacardozo)
- Leando Matias Luna: ML Developer  [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/s4phulkx) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/leandromluna)
- Yalideth Sánchez: Data Analyst [![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/yssanchez) [![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yalideth-sanchez-0478a819b?)

## Stack Tech
 ![Trello](https://img.shields.io/badge/Trello-0052CC?logo=trello&logoColor=fff) ![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?logo=github&logoColor=white) ![Slack](https://img.shields.io/badge/Slack-4A154B?logo=slack&logoColor=fff) ![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff) ![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=fff) 
 ![Visual Studio Code](https://custom-icon-badges.demolab.com/badge/Visual%20Studio%20Code-0078d7.svg?logo=vsc&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=fff) ![Numpy](https://img.shields.io/badge/Numpy-013243?logo=numpy&logoColor=fff) ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?logo=matplotlib&logoColor=fff) ![Prefect](https://img.shields.io/badge/Prefect-11557C?logo=Prefect&logoColor=fff) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=Streamlit&logoColor=fff)  ![Seaborn](https://img.shields.io/badge/Seaborn-005377?logo=Seaborn&logoColor=fff) ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?logo=power-bi&logoColor=white)

## Instalación y Ejecución
1. **Clonar el repositorio**
```bash
git clone https://github.com/No-Country-simulation/c21-57-t-data-bi
```
2. **Crear un entorno virtual en la carpeta raiz del proyecto**
```bash
pip install virtualenv                               
```
```bash
python -m venv venv
```
```bash
./venv/Scripts/activate
```
```bash
pip install -r requirements.txt
```
3. **(Local) Ejecutar la aplicación Streamlit**
- (Aunque la pagina este deployada en la nube, se puede ejecutar localmente)
```bash
streamlit run app.py
```
4. **(Cloud) Ejecutar el ETL**
- Crear cuenta en [Prefect Cloud](https://www.prefect.io/) y crear un proyecto.
- Copiar el API Key y ejecutar el siguiente comando:
```bash
prefect cloud login -k <API_KEY>
```
- Ejecutar el flujo de trabajo:
```bash
py data_engineer/main.py
```

## Estructura del Proyecto
```
c21-57-t-data-bi
    ├───/data
    │   ├───/bronze
    │   ├───/gold
    │   └───/silver
    ├───/data_analysts_bi
    ├───/data_engineer
    ├───/ml_developers
    ├──app.py
    └──requirements.txt
```
El proyecto se divide en 4 carpetas principales:
- **/data**: Data Lake con los datos en diferentes niveles de procesamiento. (Medallion Methodology):
    - **🔸/bronze**: Datos en bruto.
    - **🔹/silver**: Datos procesados y limpios.
    - **🌟/gold**: Datos finales extras y/o de analisis.
- **/data_analysts_bi**: Contiene los notebooks de los analistas de datos y BI.
- **/data_engineer**: Contiene el flujo de trabajo del ETL.
- **/ml_developers**: Contiene los notebooks de los desarrolladores de ML.

Ademas, el proyecto cuenta con: 
- Un archivo **app.py** que contiene la aplicación web de Streamlit
- Un archivo **requirements.txt** con las dependencias del proyecto.

## Streamlit Web App Docs

En la aplicación web de Streamlit se pueden encontrar las siguientes secciones:
- **Informacion**: Donde se encuentra este mismo README.MD.
- **Consultas**: Seccion donde tenemos algunos filtros para consultar datos.
- **Visualizaciones**: Seccion donde se encuentran las visualizaciones de los datos.
- **Resultados del Modelo**: Seccion donde se encuentran los resultados del modelo de ML. Se encuentran tanto graficos, como un carrito simulado en el que podemos predecir si, el carrito va a ser concretado o cancelado.
