from pyspark.sql.types import *


heat_sensor_schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("detected_objects", ArrayType(
        StructType([
            StructField("distance_km", FloatType(), True),
            StructField("bearing_degrees", FloatType(), True),
            StructField("heat_temperature_celsius", FloatType(), True)
        ])
    ))
])


radar_sensor_schema = StructType([
    StructField("radar_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("detected_objects", ArrayType(
        StructType([
            StructField("distance_km", FloatType(), True),
            StructField("bearing_degrees", FloatType(), True),
            StructField("object_size", IntegerType(), True)
        ])
    ))
])

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
    ))
])

weather_data_schema = StructType([
    StructField("coord", StructType([
        StructField("lon", FloatType(), True),
        StructField("lat", FloatType(), True)
    ])),
    StructField("weather", ArrayType(
        StructType([
            StructField("id", IntegerType(), True),
            StructField("main", StringType(), True),
            StructField("description", StringType(), True),
            StructField("icon", StringType(), True)
        ])
    )),
    StructField("main", StructType([
        StructField("temp", FloatType(), True),
        StructField("pressure", IntegerType(), True),
        StructField("humidity", IntegerType(), True)
    ])),
    StructField("wind", StructType([
        StructField("speed", FloatType(), True),
        StructField("deg", IntegerType(), True)
    ])),
    StructField("timestamp", StringType(), True)
])
