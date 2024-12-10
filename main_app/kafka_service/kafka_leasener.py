from confluent_kafka import Consumer, KafkaException, KafkaError
import json
import socket


class SensorDataConsumer:
    def __init__(self, broker="localhost:9092", group_id="sensor_group"):
        self.config = {
            'bootstrap.servers': broker,
            'group.id': group_id,
            'auto.offset.reset': 'latest',
            'enable.auto.commit': True
        }
        self.running = True

    def test_connection(self):
        """Test if Kafka broker is accessible"""
        try:
            host = "localhost"
            port = 9092
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                print("Kafka port is open")
                return True
            else:
                print(f"Kafka port is closed (error: {result})")
                return False
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def start_consuming(self):
        if not self.test_connection():
            print("Cannot connect to Kafka broker")
            return

        topics = [
            'thermal_sensor_data',
            'radar_sensor_data',
            'sonar_sensor_data',
            'weather_sensor_data'
        ]

        try:
            # Create Consumer instance
            consumer = Consumer(self.config)

            # Subscribe to topics
            consumer.subscribe(topics)
            print(f"Subscribed to topics: {topics}")

            # Process messages
            try:
                while self.running:
                    msg = consumer.poll(1.0)
                    if msg is None:
                        continue
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            print(f"Reached end of partition: {msg.topic()} [{msg.partition()}]")
                        else:
                            print(f"Error: {msg.error()}")
                    else:
                        try:
                            value = json.loads(msg.value().decode('utf-8'))
                            print("\n--- New Sensor Data ---")
                            print(f"Topic: {msg.topic()}")
                            print(f"Partition: {msg.partition()}")
                            print(f"Offset: {msg.offset()}")
                            print(f"Sensor Type: {value.get('type', 'unknown')}")
                            print(f"Timestamp: {value.get('timestamp', 'unknown')}")
                            print("Data:")
                            print(json.dumps(value.get('data', {}), indent=2))
                            print("---------------------")
                        except json.JSONDecodeError as e:
                            print(f"Failed to decode message: {e}")

            except KeyboardInterrupt:
                print("Stopped by user")
            finally:
                # Close down consumer to commit final offsets.
                consumer.close()

        except KafkaException as e:
            print(f"Kafka error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


def main():
    print("Starting Confluent Kafka consumer...")
    consumer = SensorDataConsumer()
    consumer.start_consuming()


if __name__ == "__main__":
    main()