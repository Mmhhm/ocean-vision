from pyspark.sql.types import StructType, StructField, StringType, FloatType, ArrayType, IntegerType

heat_sensor_schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("detected_objects", ArrayType(
        StructType([
            StructField("mmsi", StringType(), True),
            StructField("distance_km", FloatType(), True),
            StructField("bearing_degrees", IntegerType(), True),
            StructField("heat_temperature_celsius", FloatType(), True),
            StructField("lat", FloatType(), True),
            StructField("lon", FloatType(), True),
            StructField("status", StringType(), True)
        ])
    ), True)
])
