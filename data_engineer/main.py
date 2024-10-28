from prefect import task, flow, get_run_logger
from prefect.runtime import flow_run
import pandas as pd
import os
import configparser


config = configparser.ConfigParser()
config.read('pipeline.conf')

try:
    os.environ['KAGGLE_USERNAME'] = config['kaggle-credentials']['username']
    os.environ['KAGGLE_KEY'] = config['kaggle-credentials']['key']
except KeyError as e:
    logger = get_run_logger()
    logger.error(f'Error al leer las credenciales de kaggle: {e}')
    raise e

from  kaggle.api.kaggle_api_extended import KaggleApi
from kaggle.rest import ApiException


@task(
    retries=3,
    retry_delay_seconds=60,
    name='get_dataset_from_kaggle',
    description='Obtenemos los datos desde kaggle.com'
)
def get_dataset_from_kaggle(path:str, dataset:str, new_name: str='data.csv'):
    """
    Obtenemos los datos desde kaggle.com

    Args:
        path (_type_): path donde queremos guardar los datos
        dataset (_type_): dataset que queremos descargar de kaggle
        new_name (str, optional): Nombre del archivo que queremos guardar. Defaults to 'data.csv'.

    Returns:
        path+'/'+new_name: Retorno el path completo del archivo descargado para tenerlo disponible en la siguiente task
    """
    logger = get_run_logger()
    api = KaggleApi()
    api.authenticate()
    try:
        api.dataset_download_files(dataset, path, unzip=True)
    except ApiException as e:
        logger.error(f'Error al descargar el dataset: {e}')
        raise e
    
    file_path = os.path.join(path, new_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    
    os.rename(os.path.join(path, os.listdir(path)[0]), os.path.join(path, new_name))
    
    return path+'/'+new_name

@task(
    name='get_data_from_csv',
    description='Cargamos los datos desde un archivo csv'
)
def get_data_from_csv(path:str)->pd.DataFrame:
    """
    Cargamos los datos desde un archivo csv

    Args:
        path (str): path donde se encuentra el archivo csv
    Returns:
        pd.DataFrame: Retornamos un dataframe con los datos cargados
    """
    logger = get_run_logger()
    df = pd.read_csv(path)
    
    if df is None:
        raise ValueError('No data found')
    
    logger.info(f'Obteniendo {len(df)} registros en el dataframe')
    
    return df  

@task(
    name='transform_df',
    description='Transformamos el dataframe para que sea más fácil de trabajar'
)
def transform_df(df: pd.DataFrame)->pd.DataFrame:
    """
    Transformamos el dataframe para que sea más fácil de trabajar
    Args:
        df (pd.DataFrame): Dataframe que queremos transformar

    Returns:
        pd.DataFrame: Retornamos el dataframe transformado
    """
    logger = get_run_logger()
    if not isinstance(df, pd.DataFrame):
        raise ValueError('El input no es un dataframe')
        
    columnas_necesarias = ['TransactionNo', 'CustomerNo']
    for col in columnas_necesarias:
        if col not in df.columns:
            raise ValueError(f'La columna {col} no está en el dataframe')
        
    df = df.dropna(subset=['TransactionNo']) # Dropeamos los registros que no tienen TransactionNo
    df = df.dropna(subset=['CustomerNo']) # Dropeamos los registros que no tienen CustomerNo
    df = df.astype({'CustomerNo': 'int'}) # Convertimos CustomerNo a int
    
    logger.info(f'Dataframe transformado')
    
    return df

@task(
    name='divide_df_in_canceladas_y_concretadas',
    description='Dividimos el dataframe en dos, uno con las transacciones canceladas, y otro con las transacciones concretadas'
)
def divide_df_in_canceladas_y_concretadas(df: pd.DataFrame)->tuple:
    """
    Dividimos el dataframe en dos, uno con las transacciones canceladas, y otro con las transacciones concretadas
    Args:
        df (pd.DataFrame): Dataframe que queremos dividir por canceladas y concretadas
    Returns:
        tuple (pd.DataFrame): Devuelve una tupla de dos dataframes
    """
    logger = get_run_logger()
    if not isinstance(df, pd.DataFrame):
        raise ValueError('El input no es un dataframe')
    
    df_canceladas = df[df['TransactionNo'].str.contains('C')] # Filtramos las transacciones canceladas
    df_concretadas = df.drop(df_canceladas.index) # Eliminamos las transacciones canceladas del df original
    
    logger.info(f'Dividiendo el dataframe')
    return df_canceladas, df_concretadas

@task(
    name=f'transform_df_to_parquet',
    description='Transformamos un dataframe en un archivo parquet'
)
def transform_df_to_parquet(df: pd.DataFrame, path: str):
    """
    Transformamos un dataframe en un archivo parquet, en la ruta especificada

    Args:
        df (pd.DataFrame): Dataframe a guardar
        path (str): path donde quermos guardar el archivo .parquet
    """
    logger = get_run_logger()
    if not isinstance(df, pd.DataFrame):
        raise ValueError('El input no es un dataframe')
    
    df.to_parquet(path)
    
    logger.info(f'Guardado archivo en {path}')
    

@flow(
    name='etl-flow',
    description='Pipeline para extraer, transformar y cargar datos de un dataset de kaggle'
)
def etl():
    logger = get_run_logger()
    path = get_dataset_from_kaggle('../data/bronze','gabrielramos87/an-online-shop-business','transactions.csv')
    df = get_data_from_csv(path)
    df = transform_df(df)
    df_canceladas, df_concretadas = divide_df_in_canceladas_y_concretadas(df)
    
    transform_df_to_parquet(df_canceladas, '../data/silver/transacciones_canceladas.parquet')
    transform_df_to_parquet(df_concretadas, '../data/silver/transacciones_concretadas.parquet')
    logger.info('Pipeline finalizado y completado')
    
if __name__ == '__main__':
    etl.serve(name="etl-flow")