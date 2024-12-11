from pyspark.sql.types import StructType, StructField, StringType, FloatType, ArrayType

heat_sensor_schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("detected_objects", ArrayType(
        StructType([
            StructField("distance_km", FloatType(), True),
            StructField("bearing_degrees", FloatType(), True),
            StructField("heat_temperature_celsius", FloatType(), True)
        ])
    ), True)
])
