from typing import List, Tuple
import auxiliar_functions as aux_fun

"""Función que dada una lista de mentionedUsers retorna una lista que contiene solo los username de los mencionados"""
def get_mentioned_users(mencioned_list):
    return [mencioned["username"] for mencioned in mencioned_list]

"""Solución al ejercicio 3 donde se optimiza la memoria"""
def q3_time(file_path: str) -> List[Tuple[str, int]]:
    # Creo un dataframe con todos los jsons
    df = aux_fun.read_json_file_pandas(file_path)
    # Elimino todas las filas que no mencionan usuarios
    df = df[df['mentionedUsers'].notnull()]
    # Sumo la columna mentioned_users comn las lista de usernames mencionados
    df['mentioned_users'] = df['mentionedUsers'].apply(lambda l: get_mentioned_users(l))
    # Me quedo solo con la columna que me importa, la que contiene la lista los usuarios mencionados en el tweet
    df = df[['mentioned_users']]
    # Con la función explode convierto cada usuario dentro de la lista de mencionados en una nueva fila del data frame
    explode_df = df.explode("mentioned_users")
    # Cuento por usuario mencionado la cantidad de menciones que tuvo en toda la historia
    counts = explode_df.groupby(['mentioned_users']).size().reset_index(name='count')
    # Ordeno en forma descendente por cantidad de menciones y me quedo con los diez primeros para tener el top 10
    result = counts.sort_values(by=['count'], ascending=False).head(10)
    # Convierto el dataframe en una lista de tuplas (mentioned_user, count)
    result_list = list(zip(*map(result.get, ('mentioned_users', 'count'))))
    # Retorno la lista resultante del paso anterior
    return result_list