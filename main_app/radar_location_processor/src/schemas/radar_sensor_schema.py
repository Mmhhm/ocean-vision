from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, ArrayType


radar_sensor_schema = StructType([
    StructField("radar_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("detected_objects", ArrayType(
        StructType([
            StructField("distance_km", FloatType(), True),
            StructField("bearing_degrees", FloatType(), True),
            StructField("object_size", IntegerType(), True)
        ])
    ), True)
])
