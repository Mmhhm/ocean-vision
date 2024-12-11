from kafka import KafkaConsumer
from typing import List, Dict, Tuple
import json


from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StringType, FloatType
import json


# Initialize Spark session for Structured Streaming
spark = SparkSession.builder \
    .appName("Real-Time Ship/Submarine Analysis") \
    .getOrCreate()

# UDF to calculate hostility (example)
@udf(FloatType())
def calculate_hostility(speed, heat_temp, distance, size):
    # A simplistic formula to calculate hostility based on the given data points
    hostility = (speed * 0.5 + heat_temp * 0.3) - (distance * 0.1) + (size * 0.05)
    return max(0, min(hostility, 100))


# UDF to calculate danger (example)
@udf(FloatType())
def calculate_danger(size, depth, speed, temp):
    # A simplistic formula to calculate danger based on the given data points
    danger = (size * 0.4 + depth * 0.2 + speed * 0.3) - (temp * 0.1)
    return max(0, min(danger, 100))


# Define Kafka consumer stream
kafka_stream_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "thermal_sensor_data,radar_sensor_data,sonar_sensor_data,weather_sensor_data") \
    .load()

# Deserialize JSON data
heat_sensor_schema = "sensor_id STRING, timestamp STRING, detected_objects ARRAY<STRUCT<" \
                     "mmsi: STRING, distance_km: FLOAT, bearing_degrees: INT, " \
                     "heat_temperature_celsius: FLOAT, lat: FLOAT, lon: FLOAT, status: STRING>>"

radar_sensor_schema = "sensor_id STRING, timestamp STRING, detected_objects ARRAY<STRUCT<" \
                      "mmsi: STRING, object_type: STRING, distance_km: FLOAT, bearing_degrees: INT, " \
                      "latitude: FLOAT, longitude: FLOAT, speed_knots: FLOAT, object_size: INT, status: STRING>>"

sonar_sensor_schema = "sonar_id STRING, timestamp STRING, detected_objects ARRAY<STRUCT<" \
                      "submarine_id: STRING, object_type: STRING, depth_meters: FLOAT, " \
                      "distance_km: FLOAT, latitude: FLOAT, longitude: FLOAT, speed_knots: FLOAT, " \
                      "object_shape: STRING, bearing_degrees: INT, object_material: STRING, " \
                      "object_size: INT, status: STRING>>"

weather_sensor_schema = "coord STRUCT<lon: FLOAT, lat: FLOAT>, weather ARRAY<STRUCT<id: INT, " \
                        "main: STRING, description: STRING, icon: STRING>>, base: STRING, main STRUCT<" \
                        "temp: FLOAT, feels_like: FLOAT, temp_min: FLOAT, temp_max: FLOAT, pressure: INT, " \
                        "humidity: INT, sea_level: INT, grnd_level: INT>, visibility: INT, " \
                        "wind STRUCT<speed: FLOAT, deg: INT, gust: FLOAT>, clouds STRUCT<all: INT>, " \
                        "dt: INT, sys STRUCT<sunrise: INT, sunset: INT>, timezone: INT, id: INT, " \
                        "name: STRING, cod: INT"

# Transform the Kafka data to JSON and apply the appropriate schema
json_df = kafka_stream_df.selectExpr("CAST(value AS STRING) AS json_data")

heat_sensor_df = json_df.select(from_json(col("json_data"), heat_sensor_schema).alias("data"))
radar_sensor_df = json_df.select(from_json(col("json_data"), radar_sensor_schema).alias("data"))
sonar_sensor_df = json_df.select(from_json(col("json_data"), sonar_sensor_schema).alias("data"))
weather_sensor_df = json_df.select(from_json(col("json_data"), weather_sensor_schema).alias("data"))

# Example of adding hostility and danger columns
heat_sensor_with_analysis = heat_sensor_df.select(
    "*",
    calculate_hostility(col("data.detected_objects.speed_knots"),
                        col("data.detected_objects.heat_temperature_celsius"),
                        col("data.detected_objects.distance_km"),
                        col("data.detected_objects.object_size")).alias("hostility")
)

radar_sensor_with_analysis = radar_sensor_df.select(
    "*",
    calculate_hostility(col("data.detected_objects.speed_knots"),
                        col("data.detected_objects.heat_temperature_celsius"),
                        col("data.detected_objects.distance_km"),
                        col("data.detected_objects.object_size")).alias("hostility"),
    calculate_danger(col("data.detected_objects.object_size"),
                     col("data.detected_objects.depth_meters"),
                     col("data.detected_objects.speed_knots"),
                     col("data.detected_objects.temp")).alias("danger")
)

sonar_sensor_with_analysis = sonar_sensor_df.select(
    "*",
    calculate_hostility(col("data.detected_objects.speed_knots"),
                        col("data.detected_objects.heat_temperature_celsius"),
                        col("data.detected_objects.distance_km"),
                        col("data.detected_objects.object_size")).alias("hostility"),
    calculate_danger(col("data.detected_objects.object_size"),
                     col("data.detected_objects.depth_meters"),
                     col("data.detected_objects.speed_knots"),
                     col("data.detected_objects.temp")).alias("danger")
)

weather_sensor_with_analysis = weather_sensor_df.select(
    "*"
)

# Output the results (this could be saved to another Kafka topic, file, etc.)
query_heat_sensor = heat_sensor_with_analysis.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query_radar_sensor = radar_sensor_with_analysis.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query_sonar_sensor = sonar_sensor_with_analysis.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query_weather_sensor = weather_sensor_with_analysis.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Await termination to keep the stream active
query_heat_sensor.awaitTermination()
query_radar_sensor.awaitTermination()
query_sonar_sensor.awaitTermination()
query_weather_sensor.awaitTermination()
