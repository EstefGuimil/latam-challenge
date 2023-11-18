from typing import List, Tuple
from pyspark.sql.functions import *
import auxiliar_functions as aux_fun

"""Defino una UDF para poder utilizar la función para generar otra columna"""
udf_extract_emojis = udf(aux_fun.extract_emojis, ArrayType(StringType()))

"""Solución al ejercicio 2 donde se optimiza el tiempo de ejecución"""
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    # Leo el archivo json que se encuentra en la ruta compartida
    df_tweets = aux_fun.read_json_file_spark(file_path)
    if (df_tweets.count() == 0):
        return []
    else:
        try:
            # Me quedo solo con la columna del texto que es la que me interesa
            df_content = df_tweets.select(df_tweets.content)
            # Genero una nueva columna con el listado de emojis que se encontró en el texto
            df_content_new = df_content.withColumn("emojis", udf_extract_emojis(df_content["content"]))
            # Descarto las filas cuya columna emojis es una lista vacia
            df_content_filter = df_content_new.filter(size(df_content_new.emojis) > 0)
            # Ontengo con la funcion map una lista de listas de emoji
            all_emoji_list = df_content_filter.rdd.map(lambda x: x[1]).collect()
            # Invoco a la función get_emoji_list para obtener una lista de tuplas (emoji, cantidad)
            result_list = aux_fun.get_emoji_alist(all_emoji_list)
            # Retorno solo los primeros 10 resultados que son el top 10 de emojis
            return result_list[:10]
        except AttributeError:
            return []  # Casos en que no existe en el archivo que leí ningun registro con content