from pyspark.sql import SparkSession

# def get_spark_session():
#     return SparkSession.builder \
#         .appName("OceanVisionApp")\
#          .master("spark://localhost:7077")\
#         .config("spark.executor.memory", "2g") \
#         .config("spark.driver.memory", "2g") \
#         .getOrCreate()


# Initialize Spark session
spark = SparkSession.builder \
    .appName("RealTimeHeatSensorProcessing") \
    .getOrCreate()

# Set log level to WARN to avoid unnecessary logs
spark.sparkContext.setLogLevel("WARN")