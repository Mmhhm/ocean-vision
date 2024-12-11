from pyspark.sql.functions import explode, col, unix_timestamp, lag
from pyspark.sql.window import Window

def expand_objects(df):
    """
    Expand detected objects into individual rows.
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

def calculate_velocity(df):
    """
    Calculate velocity based on distance and time difference.
    """
    window_spec = Window.partitionBy("radar_id", "bearing_degrees").orderBy("timestamp")

    return df.withColumn("prev_distance", lag("distance_km").over(window_spec)) \
        .withColumn("prev_timestamp", lag("timestamp").over(window_spec)) \
        .withColumn("time_diff_sec", unix_timestamp("timestamp") - unix_timestamp("prev_timestamp")) \
        .withColumn("velocity_kmh", 
            (col("distance_km") - col("prev_distance")) / (col("time_diff_sec") / 3600)
        )
