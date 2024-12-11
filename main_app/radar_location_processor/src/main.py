# from src.ingestion.sensors_consumer import KafkaConsumerService
# from main_app.radar_location_processor.processing.message_processor import SparkProcessor
# from schemas.radar_sensor_schema import radar_sensor_schema
# from spark_connection import get_spark_session


# def process_kafka_message(spark_processor, message):
#     spark_processor.process_message(message)

# def main():
#     spark = get_spark_session()
#     spark_processor = SparkProcessor(spark, radar_sensor_schema)  

#     kafka_service = KafkaConsumerService(lambda message: process_kafka_message(spark_processor, message))
    

#     kafka_service.consume_messages()

# if __name__ == "__main__":
#     main()



from ingestion.sensors_consumer import KafkaConsumerService  
from processing.message_processor import MessageProcessor  
from schemas.radar_sensor_schema import radar_sensor_schema     
from spark_connection import get_spark_session                    

def process_kafka_message(spark_processor, message):
    """
    Callback function to process each Kafka message.
    This function will be called whenever a new message is consumed from Kafka.
    """
    spark_processor.process_message(message)

def main():
    spark = get_spark_session()

    spark_processor = MessageProcessor(spark, radar_sensor_schema)

    kafka_service = KafkaConsumerService(lambda message: process_kafka_message(spark_processor, message))

    kafka_service.consume_messages()

if __name__ == "__main__":
   
    main()
