from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import pandas as pd
import json
import emoji

"""Esta función retorna un dataframe que contiene el archivo json que corresponde al file_path.
    Función en la que se utiliza spark"""
def read_json_file_spark(file_path):
    # Inicializo spark
    spark = SparkSession.builder.master("local[1]") \
                    .appName('SparkApp') \
                    .getOrCreate()
    # Establezco que el nivel de log que quiero es error, para que solo muestre mensajes en caso de que ocurra un error
    spark.sparkContext.setLogLevel("ERROR")
    # Leo el archivo json que se encuentra en la ruta compartida
    df = spark.read.json(file_path)
    # Retorno el datafame resultante del punto anterior
    return df

"""Esta función retorna un dataframe que contiene el archivo json que corresponde al file_path.
    Función en la que se utiliza Pandas"""
def read_json_file_pandas(file_path):
    # Abro el archivo json que se encuentra en la ruta compartida
    with open(file_path) as json_file:
        # Leo todas las lineas del archivo
        data = json_file.readlines()
        # Convierto todas las lineas en json
        data = list(map(json.loads, data)) 
    # Creo un dataframe con todos los jsons
    df = pd.DataFrame(data)
    # Retorno el datafame resultante del punto anterior
    return df

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
