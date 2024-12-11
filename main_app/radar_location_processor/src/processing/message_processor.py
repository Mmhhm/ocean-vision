from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, unix_timestamp, lag
from pyspark.sql.window import Window
import json

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

    def process_message(self, message):
        """
        Processes an incoming message by applying transformations to the data.
        """
        try:
            # Parse the JSON message
            data = json.loads(message)
            detected_objects = data.get("detected_objects", [])

            # Expand and process detected objects
            radar_df = self.spark.read.json(self.spark.sparkContext.parallelize([data]), schema=self.schema)
            expanded_df = self.expand_objects(radar_df)

            for obj in detected_objects:
                distance_value = obj.get("distance_km")
                bearing_value = obj.get("bearing_degrees")

                if distance_value is not None and bearing_value is not None:
                    # Apply location calculation
                    lat2, lon2 = calculate_location(
                        lat1=34.0522,
                        lon1=-118.2437,
                        distance_km=distance_value,
                        bearing_degrees=bearing_value
                    )
                    print(f"Calculated location: Latitude {lat2}, Longitude {lon2}")


            processed_df = calculate_velocity(expanded_df)
            processed_df.show()

        except Exception as e:
            print(f"Error processing message: {e}")

    def expand_objects(self, df):
        """
        Expands detected objects into individual rows.
        """
        return df.select(
            col("radar_id"),
            col("timestamp"),
            explode(col("detected_objects")).alias("object")
        ).select(
            col("radar_id"),
            col("timestamp"),
            col("object.distance_km").alias("distance_km"),
            col("object.bearing_degrees").alias("bearing_degrees")
        )