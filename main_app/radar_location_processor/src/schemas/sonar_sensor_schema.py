from pyspark.sql.types import StructType, StructField, StringType, FloatType, ArrayType


sonar_sensor_schema = StructType([
    StructField("sonar_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("detected_objects", ArrayType(
        StructType([
            StructField("depth_meters", FloatType(), True),
            StructField("distance_km", FloatType(), True),
            StructField("bearing_degrees", FloatType(), True),
            StructField("object_material", StringType(), True),
            StructField("object_size", IntegerType(), True)
        ])
    ), True)
])
