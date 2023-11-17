from typing import List, Tuple
from pyspark.sql.functions import *
import emoji
import auxiliar_functions as aux_fun

"""Esta función retorna la lista de emojis que contiene el string que se pasa por parametro.
    S puede ser una o varias palabrass"""
def extract_emojis(s):
    # Creo una lista vacia para almacenar los elementos que voy a retornar
    emoji_list = []
    # Con emoji.emoji_list obtengo una lista de elementos {'match_start': N, 'match_end': M, 'emoji': '💚'} me quedo solo con la parte de emoji
    for e in emoji.emoji_list(s):
        emoji_list.append(e['emoji'])
    # Retorno la lista generada
    return emoji_list

"""Defino una UDF para poder utilizar la función para generar otra columna"""
udf_extract_emojis = udf(extract_emojis, ArrayType(StringType()))

"""Esta función retorna una lista de tuplas con dos componentes, el emoji y la cantidad de veces que se uso.
    La lista generada se retorna ordenada empezando con el emoji que más se uso y terminando con el que menos"""
def get_emoji_list(all_emoji_list):
    # Creo un diccionario vacio para trabajar dentro de la función
    emoji_dict = {}
    # Por cada lista de emojis dentro de all_emoji_list
    for emoji_list in all_emoji_list:
        # Por emoji dentro de emoji_list
        for em in emoji_list:
            # Si el emoji todavía no esta dentro del diccionario
            if emoji_dict.get(em) == None:
                # Sumo el nuevo emoji e inicializo su contador en 1
                emoji_dict[em] = 1
            else: # Si el emoji ya esta en el diccionario 
                # Obtengo la cantidad de veces que aparecio hasta ahora
                cant_em = emoji_dict[em]
                # Actualizo la cantidad de apariciones sumando 1 que corresponde a la actual
                emoji_dict[em] = cant_em + 1
    # Retorno la lista de tuplas (emoji, cantidad) ordenada por cantidad en modo descendente
    return sorted(emoji_dict.items(), key = lambda x:x[1], reverse=True)

"""Solución al ejercicio 2 donde se optimiza el tiempo de ejecución"""
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    # Leo el archivo json que se encuentra en la ruta compartida
    df_tweets = aux_fun.read_json_file_spark(file_path)
    # Me quedo solo con la columna del texto que es la que me interesa
    df_content = df_tweets.select(df_tweets.content)
    # Genero una nueva columna con el listado de emojis que se encontró en el texto
    df_content_new = df_content.withColumn("emojis", udf_extract_emojis(df_content["content"]))
    # Descarto las filas cuya columna emojis es una lista vacia
    df_content_filter = df_content_new.filter(size(df_content_new.emojis) > 0)
    # Ontengo con la funcion map una lista de listas de emoji
    all_emoji_list = df_content_filter.rdd.map(lambda x: x[1]).collect()
    # Invoco a la función get_emoji_list para obtener una lista de tuplas (emoji, cantidad)
    result_list = get_emoji_list(all_emoji_list)
    # Retorno solo los primeros 10 resultados que son el top 10 de emojis
    return result_list[:10]