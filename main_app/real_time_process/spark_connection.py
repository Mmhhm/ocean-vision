from pyspark.sql import SparkSession


spark = SparkSession.builder \
    .appName("OceanVisionApp")\
    .master("spark://localhost:7077")\
    .getOrCreate()

print("Connected to Spark Cluster.")

data = [("John", 28), ("Jane", 32), ("Joe", 40)]
df = spark.createDataFrame(data, ["Name", "Age"])

df.show()
