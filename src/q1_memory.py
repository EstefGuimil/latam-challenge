from typing import List, Tuple
from datetime import datetime
from pyspark.sql.functions import *
from pyspark.sql.window import Window
import auxiliar_functions as aux_fun

"""Esta función retorna un dataframe con el usuario que mas publicaciones realizo por fecha
    Ordenado por fecha"""
def get_top_user_by_date(df_tweets):
    # Cuento los tweets por fecha y usuario
    counts = df_tweets.groupBy("created_date", "user.username").count()
    # Establezo las condiciones para la partición y orden de la información, necesito que genere particiones por fecha ordenadas por fecha de creacion asc y cantidad de tweets desc 
    window_spec  = Window.partitionBy("created_date").orderBy(col("created_date").asc(),col("count").desc())
    # Se crea una nueva columna donde a cada fila se le asigna un numero secuencial que depende de la ventana creada en la linea anterior
    counts_order = counts.withColumn("row_number", row_number().over(window_spec))
    # Por cada partición generada me quedo solo con el primer resultado
    top_user_by_date = counts_order.filter(col("row_number") == 1)
    # Elimino las columnas que no necesito
    top_user_by_date = top_user_by_date.drop("row_number").drop("count")
    # Retorno el dataframe resultante
    return top_user_by_date

"""Solución al ejercicio 1 donde se optimiza la memoria"""
def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    # Leo el archivo json que se encuentra en la ruta compartida
    df_tweets = aux_fun.read_json_file_spark(file_path)
    if (df_tweets.count() == 0):
        return []
    else:
        try:
            # Sumo una nueva columna que convierte en date el valor string allmacenado en la columna date
            df_tweets_new = df_tweets.withColumn("created_date", to_date(substring(df_tweets.date, 1,10),"yyyy-MM-dd"))
            # Genero un dataframe con la cantidad de tweets por fecha
            count_by_date = df_tweets_new.groupBy("created_date").count()
            # Genero un dataframe con los mejores usuarios en cantidad de tweets por fecha
            top_user_by_date = get_top_user_by_date(df_tweets_new)
            # Cruzo la informacion en count_by_date con la iformacion en top_user_by_date para obtener el resultado utilizando como key la fecha
            result = count_by_date.join(top_user_by_date, count_by_date.created_date == top_user_by_date.created_date, "inner")
            # Ordeno por fecha de mayor cantidad de tweets y me quedo con los primeros 10 resultados
            result =  result.orderBy(col("count").desc()).limit(10)
            # Convierto el dataframe en una lista de tuplas (fecha, username)
            result_list = result.rdd.map(lambda x: (x[0], x[3])).collect()
            # Retorno la lista resultante del paso anterior
            return(result_list)
        except AttributeError:
            return []  # Casos en que no existe en el archivo que leí ningun registro con date