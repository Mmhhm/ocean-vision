import os
from dotenv import load_dotenv
from confluent_kafka import Consumer, KafkaError

load_dotenv()

class KafkaConsumerService:
    def __init__(self, message_handler):
        self.consumer = Consumer({
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
            'group.id': os.getenv('KAFKA_GROUP_ID'),
            'auto.offset.reset': os.getenv('KAFKA_AUTO_OFFSET_RESET')
        })
        topics = os.getenv('KAFKA_TOPICS').split(',')
        self.consumer.subscribe(topics)
        self.message_handler = message_handler
        print(f"Subscribed to topics: {topics}")

    def consume_messages(self):
        try:
            while True:
                msg = self.consumer.poll(1.0)  # Poll every second
                if msg is None:
                    print("No message received. Waiting...")
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    print(f"Error: {msg.error()}")
                    break
                print(f"Received message: {msg.value().decode('utf-8')}")
                self.message_handler(msg.value().decode('utf-8'))
        except KeyboardInterrupt:
            print("Consumption interrupted.")
        finally:
            self.consumer.close()