from pyspark.sql import SparkSession
from pyspark.sql.functions import *

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

