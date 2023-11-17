from typing import List, Tuple
from pyspark.sql.functions import *
import auxiliar_functions as aux_fun

"""Solución al ejercicio 3 donde se optimiza el tiempo de ejecución"""
def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    # Leo el archivo json que se encuentra en la ruta compartida
    df_tweets = aux_fun.read_json_file_spark(file_path)
    # Me quedo solo con la informacion relevante: los username mencionados en los tweets (username dentro del nodo mentionedUsers)
    df_users = df_tweets.select(df_tweets.mentionedUsers.username.alias("mentioned_users"))
    # Filtro las filas donde el arreglo de usuarios mecionados esta vacio
    df_users_filter = df_users.filter(size(df_users.mentioned_users) > 0)
    # Con la función explode convierto cada usuario dentro de la lista de mencionados en una nueva fila del data frame
    explode_df = df_users_filter.select("*", explode("mentioned_users").alias("mentioned_user"))
    # Elimino la columna que tiene el arreglo de mencionados que ya no es necesaria
    explode_df = explode_df.drop(explode_df.mentioned_users)
    # Cuento por usuario mencionado la cantidad de menciones que tuvo en toda la historia
    counts = explode_df.groupBy("mentioned_user").count()
    # Ordeno en forma descendente por cantidad de menciones y me quedo con los diez primeros para tener el top 10
    top_ten_mentioned_user = counts.orderBy(col("count").desc()).limit(10)
    # Convierto el dataframe en una lista de tuplas (mentioned_user, count)
    result_list = top_ten_mentioned_user.rdd.map(lambda x: (x[0], x[1])).collect()
    # Retorno la lista resultante del paso anterior
    return(result_list)