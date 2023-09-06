# Importando bibliotecas
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
from lib.logger import Log4j

# Criando a sessão do spark
spark = SparkSession \
        .builder \
        .appName('Streaming using kafka') \
        .config('spark.streaming.stopGracefullyOnShutdown', 'true') \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0') \
        .master('local[4]') \
        .getOrCreate()

# Criando o logger
logger = Log4j(spark)

# Criando um schema para receber os dados
schema = StructType([
    StructField('user_id',   StringType()),
    StructField('name',      StringType()),
    StructField('level',     IntegerType()),
    StructField('campeao1',  StringType()),
    StructField('maestria1', IntegerType()),
    StructField('campeao2',  StringType()),
    StructField('maestria2', IntegerType()),
    StructField('campeao3',  StringType()),
    StructField('maestria3', IntegerType())
])

# Criando um dataframe através do kafka
kafka_df = spark.readStream \
                .format('kafka') \
                .option('kafka.bootstrap.servers', 'localhost:9092') \
                .option('startingOffsets', 'earliest') \
                .option('subscribe', 'League_of_Legends') \
                .load()

# .option('startingOffsets', 'earliest')  # --> Para começar a ler desde o inicio

value_df = kafka_df.select(F.from_json(F.col('value').cast('string'), schema).alias('value'))
# value_df.printSchema()

explode_df = value_df.withColumn('user_id', F.col('value.user_id')) \
                     .withColumn('name', F.col('value.name')) \
                     .withColumn('level', F.col('value.level')) \
                     .withColumn('campeao1', F.col('value.campeao1')) \
                     .withColumn('maestria1', F.col('value.maestria1')) \
                     .withColumn('campeao2', F.col('value.campeao2')) \
                     .withColumn('maestria2', F.col('value.maestria2')) \
                     .withColumn('campeao3', F.col('value.campeao3')) \
                     .withColumn('maestria3', F.col('value.maestria3')) \
                     .select('user_id', 'name', 'level', 'campeao1', 'maestria1', 'campeao2', 'maestria2', 'campeao3', 'maestria3')

# explode_df.printSchema()

# Executa o streaming
kafka_stream = explode_df.writeStream \
                         .format('json') \
                         .queryName('Stream league of legends') \
                         .outputMode('append') \
                         .option('path', 'output') \
                         .option('checkpointLocation', 'chk-point-dir') \
                         .trigger(processingTime='1 minute') \
                         .start()

# gera o log
logger.info('Criando o dataframe do kafka')

# Aguarda algo para terminar a execução
kafka_stream.awaitTermination()