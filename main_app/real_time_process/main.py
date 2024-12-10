from ingestion.kafka_consumer import KafkaConsumerService

def main():
    print("Kafka Consumer is starting... Listening for messages.\nPress CTRL+C to stop.")
    kafka_service = KafkaConsumerService()
    kafka_service.consume_messages()

if __name__ == "__main__":
    main()
