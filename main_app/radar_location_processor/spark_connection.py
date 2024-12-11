from pyspark.sql import SparkSession

def get_spark_session():
    return SparkSession.builder \
        .appName("OceanVisionApp")\
         .master("spark://localhost:7077")\
        .config("spark.executor.memory", "2g") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()



