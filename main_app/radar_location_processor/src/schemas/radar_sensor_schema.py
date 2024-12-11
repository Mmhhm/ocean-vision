from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, ArrayType


radar_sensor_schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("detected_objects", ArrayType(
        StructType([
            StructField("mmsi", StringType(), True),
            StructField("object_type", StringType(), True),
            StructField("distance_km", FloatType(), True),
            StructField("bearing_degrees", IntegerType(), True),
            StructField("latitude", FloatType(), True),
            StructField("longitude", FloatType(), True),
            StructField("speed_knots", FloatType(), True),
            StructField("object_size", IntegerType(), True),
            StructField("status", StringType(), True)
        ])
    ), True)
])
