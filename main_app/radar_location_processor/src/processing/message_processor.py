from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, unix_timestamp, lag
from pyspark.sql.window import Window
import json

from main_app.radar_location_processor.src.schemas import radar_sensor_schema, sonar_sensor_schema, heat_sensor_schema
from main_app.radar_location_processor.src.transformation.location_calculator import calculate_location
from main_app.radar_location_processor.src.transformation.velocity_calculation import calculate_velocity

class MessageProcessor:
    def __init__(self, spark: SparkSession, schema):
        self.spark = spark
        self.schema = schema

    # def process_message(self, message):
    #     """
    #     Processes an incoming message by applying transformations to the data.
    #     """
        
    #     radar_df = self.spark.read.json(self.spark.sparkContext.parallelize([message]), schema=self.schema)
        
        
    #     expanded_df = self.expand_objects(radar_df)
    #     expanded_df = calculate_location(lat1=34.0522, lon1=-118.2437, distance_km=message[''], bearing_degrees=bearing_value)
    #     processed_df = calculate_velocity(expanded_df)


    #     processed_df.show()

    # def process_message(self, message):
    #     """
    #     Processes an incoming message by applying transformations to the data.
    #     """
    #     try:
    #         # Parse the JSON message
    #         data = json.loads(message)
    #         detected_objects = data.get("detected_objects", [])
    #
    #         # Expand and process detected objects
    #         radar_df = self.spark.read.json(self.spark.sparkContext.parallelize([data]), schema=self.schema)
    #         expanded_df = self.expand_objects(radar_df)
    #
    #         for obj in detected_objects:
    #             distance_value = obj.get("distance_km")
    #             bearing_value = obj.get("bearing_degrees")
    #
    #             if distance_value is not None and bearing_value is not None:
    #                 # Apply location calculation
    #                 lat2, lon2 = calculate_location(
    #                     lat1=34.0522,
    #                     lon1=-118.2437,
    #                     distance_km=distance_value,
    #                     bearing_degrees=bearing_value
    #                 )
    #                 print(f"Calculated location: Latitude {lat2}, Longitude {lon2}")
    #
    #
    #         processed_df = calculate_velocity(expanded_df)
    #         processed_df.show()
    #
    #     except Exception as e:
    #         print(f"Error processing message: {e}")
    #
    # def expand_objects(self, df):
    #     """
    #     Expands detected objects into individual rows.
    #     """
    #     return df.select(
    #         col("radar_id"),
    #         col("timestamp"),
    #         explode(col("detected_objects")).alias("object")
    #     ).select(
    #         col("radar_id"),
    #         col("timestamp"),
    #         col("object.distance_km").alias("distance_km"),
    #         col("object.bearing_degrees").alias("bearing_degrees")
    #     )


from pyspark.sql.types import StructType, StructField, StringType, FloatType, IntegerType, ArrayType
from main_app.radar_location_processor.spark_connection import spark
from pyspark.sql.functions import from_json, col, lit, udf, when, array


from main_app.radar_location_processor.src.schemas.radar_sensor_schema import radar_sensor_schema
from main_app.radar_location_processor.src.schemas.heat_sensor_schema import heat_sensor_schema
from main_app.radar_location_processor.src.schemas.sonar_sensor_schema import sonar_sensor_schema
from main_app.radar_location_processor.src.schemas.weather_schema import weather_data_schema
from main_app.radar_location_processor.src.transformation.danger_analyze import calculate_danger
from main_app.radar_location_processor.src.transformation.danger_analyze import calculate_hostility

# Kafka reading streams (example for ships and submarines)
heat_sensor_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "heat_sensor_topic") \
    .load() \
    .selectExpr("CAST(value AS STRING)").select(from_json("value", heat_sensor_schema).alias("data"))

radar_sensor_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "radar_sensor_topic") \
    .load() \
    .selectExpr("CAST(value AS STRING)").select(from_json("value", radar_sensor_schema).alias("data"))

sonar_sensor_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "sonar_sensor_topic") \
    .load() \
    .selectExpr("CAST(value AS STRING)").select(from_json("value", sonar_sensor_schema).alias("data"))

weather_data_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "weather_data_topic") \
    .load() \
    .selectExpr("CAST(value AS STRING)").select(from_json("value", weather_data_schema).alias("data"))



# Combine the data and perform analysis

# Join the data (example: using mmsi as a key)
joined_df = heat_sensor_df \
    .join(radar_sensor_df, "mmsi") \
    .join(sonar_sensor_df, "mmsi") \
    .join(weather_data_df, "lat", "lat")

# Calculate hostility and danger
analysis_df = joined_df \
    .withColumn("detected_objects",
                when(col("data.object_type") == "ship",
                     array(
                         col("data.mmsi"),
                         col("data.distance_km"),
                         col("data.bearing_degrees"),
                         col("data.heat_temperature_celsius"),
                         col("data.lat"),
                         col("data.lon"),
                         col("data.status"),
                         calculate_hostility(col("data.speed_knots"), col("data.heat_temperature_celsius"), col("data.distance_km"), col("data.object_size")).alias("hostility"),
                         calculate_danger(col("data.object_size"), col("data.depth_meters"), col("data.speed_knots"), col("data.temp")).alias("danger")
                     )
                ).otherwise(
                     array(
                         col("data.submarine_id"),
                         col("data.distance_km"),
                         col("data.bearing_degrees"),
                         col("data.depth_meters"),
                         col("data.lat"),
                         col("data.lon"),
                         col("data.status"),
                         calculate_hostility(col("data.speed_knots"), col("data.heat_temperature_celsius"), col("data.distance_km"), col("data.object_size")).alias("hostility"),
                         calculate_danger(col("data.object_size"), col("data.depth_meters"), col("data.speed_knots"), col("data.temp")).alias("danger")
                     )
                )
            )

# Separate Ship and Submarine DataFrames
ships_df = analysis_df.filter(col("detected_objects.object_type") == "ship")
submarines_df = analysis_df.filter(col("detected_objects.object_type") == "submarine")

# Prepare final JSON output for Ships
ships_output_df = ships_df.select(
    "data.sensor_id", "data.timestamp", "detected_objects"
)

# Prepare final JSON output for Submarines
submarines_output_df = submarines_df.select(
    "data.sonar_id", "data.timestamp", "detected_objects"
)

# Output the results as JSON
query_ships = ships_output_df.writeStream \
    .outputMode("append") \
    .format("json") \
    .option("path", "/path/to/ships_output") \
    .option("checkpointLocation", "/path/to/ships_checkpoint") \
    .start()

query_submarines = submarines_output_df.writeStream \
    .outputMode("append") \
    .format("json") \
    .option("path", "/path/to/submarines_output") \
    .option("checkpointLocation", "/path/to/submarines_checkpoint") \
    .start()

# Wait for the termination of the streams
query_ships.awaitTermination()
query_submarines.awaitTermination()