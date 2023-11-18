from typing import List, Tuple
import auxiliar_functions as aux_fun

"""Solución al ejercicio 2 donde se optimiza la memoria"""
def q2_time(file_path: str) -> List[Tuple[str, int]]:
    # Creo un dataframe con todos los jsons
    df = aux_fun.read_json_file_pandas(file_path)
    if df.empty:
        return []
    else:
        # Me quedo solo con la columna de content que es la que me interesa
        df = df[['content']]
        # Genero una nueva columna con el listado de emojis que se encontró en el texto
        df['emojis'] = df['content'].apply(lambda s: aux_fun.extract_emojis(s))
        # Descarto las filas cuya columna emojis es una lista vacia
        df = df[df['emojis'].str.len() > 0]
        # Obtengo una lista de listas de emoji
        all_emoji_list = []
        # Recorro cada fila del dataframe
        for _, row in df.iterrows():
            all_emoji_list.append(row['emojis'])
        # Invoco a la función get_emoji_list para obtener una lista de tuplas (emoji, cantidad)
        result_list = aux_fun.get_emoji_list(all_emoji_list)
        # Retorno solo los primeros 10 resultados que son el top 10 de emojis
        return result_list[:10]