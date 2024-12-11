from pyspark.sql.types import StructType, StructField, StringType, FloatType, ArrayType, IntegerType


sonar_sensor_schema = StructType([
    StructField("sonar_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("detected_objects", ArrayType(
        StructType([
            StructField("submarine_id", StringType(), True),
            StructField("object_type", StringType(), True),
            StructField("depth_meters", FloatType(), True),
            StructField("distance_km", FloatType(), True),
            StructField("longitude", FloatType(), True),
            StructField("latitude", FloatType(), True),
            StructField("speed_knots", FloatType(), True),
            StructField("object_shape", StringType(), True),
            StructField("bearing_degrees", IntegerType(), True),
            StructField("object_material", StringType(), True),
            StructField("object_size", IntegerType(), True),
            StructField("status", StringType(), True)
        ])
    ), True)
])
