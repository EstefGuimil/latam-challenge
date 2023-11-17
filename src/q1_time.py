from typing import List, Tuple
from datetime import datetime
import auxiliar_functions as aux_fun

"""Esta función retorna un dataframe con el usuario que mas publicaciones realizo por fecha
    Ordenado por fecha"""
def get_top_user_by_date(df):
    # Creo una columna nueva con el username
    df['username'] = [d.get('username') for d in df.user]
    # Me quedo con las columnas created_date y username que son las que me interesan
    df_new = df[['created_date', 'username']]
    # Cuento por día y usuario cuantas publicaciones se hicieron
    counts = df_new.groupby(['created_date', 'username']).size().reset_index(name='counts')
    # Ordeno los valores resultantes del paso anterior por fecha y cantidad de forma descendente
    counts = counts.sort_values(by=['created_date', 'counts'], ascending=False)
    # Creo una nueva columna con un numero secuencial que por fecha le asigna mayor valor al usuario con mayor cantidad de publicaciones
    counts['row_number'] = counts.groupby(['created_date'])['counts'].cumcount()
    # Me quedo con el usuario con mayor numero de publicaciones
    top_user_by_date = counts[counts.row_number == 0]
    # Selecciono solo las columnas que quiero mantener en el dataframe que voy a retornar
    top_user_by_date = top_user_by_date[['created_date', 'username']]
    # Retorno el dataframe resultante
    return top_user_by_date

"""Solución al ejercicio 1 donde se optimiza el tiempo de ejecución"""
def q1_time(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Creo un dataframe con todos los jsons
    df = aux_fun.read_json_file_pandas(file_path)
    # Convierto en datetime la fecha del tweet
    df['created_date'] = df['date'].str[:10]
    # Genero un dataframe con la cantidad de tweets por fecha
    count_by_date = df.groupby(['created_date']).size().reset_index(name='count')
    # Genero un dataframe con los mejores usuarios en cantidad de tweets por fecha
    top_user_by_date = get_top_user_by_date(df)
    # Hago un join entre el dataframe count_by_date y top_user_by_date para tener la información en un mismo dataframe, uso created_date como key
    result = count_by_date.join(top_user_by_date.set_index(["created_date"]),on=["created_date"],how="inner",lsuffix="_x",rsuffix="_y",)
    # Ordeno por fecha de mayor cantidad de tweets y me quedo con los primeros 10 resultados
    result = result.sort_values(by=['count'], ascending=False).head(10)
    # Creo la lista vacia que almacenara el resultado final
    result_list = []
    # Recorro cada fila del dataframe result
    for _, row in result.iterrows():
        # Convierto la fecha que estaba en string a date
        str_to_date = datetime.strptime(row['created_date'], "%Y-%m-%d").date()
        # Agrego la tupla (fecha, username) en la lista a retornar
        result_list.append((str_to_date, row['username']))
    # Retorno la lista resultante del paso anterior
    return result_list