import paho.mqtt.client as mqtt
from kafka import KafkaProducer
import json


class SensorKafkaSubscriber:
    def __init__(self, mqtt_broker="localhost", mqtt_port=1883, kafka_broker="localhost:9092"):
        # MQTT setup
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Kafka setup
        self.producer = KafkaProducer(
            bootstrap_servers=[kafka_broker],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

        # Kafka topics mapping
        self.kafka_topics = {
            'thermal': 'thermal_sensor_data',
            'radar': 'radar_sensor_data',
            'sonar': 'sonar_sensor_data',
            'weather': 'weather_sensor_data'
        }

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code " + str(rc))
        # Subscribe to all sensor topics
        self.client.subscribe("sensors/#")

    def on_message(self, client, userdata, msg):
        try:
            # Parse the JSON message
            data = json.loads(msg.payload)
            sensor_type = data['type']

            # Get corresponding Kafka topic
            kafka_topic = self.kafka_topics.get(sensor_type)

            if kafka_topic:
                # Send to Kafka
                self.producer.send(kafka_topic, value=data)
                self.producer.flush()
                print(f"Sent {sensor_type} data to Kafka topic: {kafka_topic}")

                # Optional: Print the data for debugging
                print(f"Data: {json.dumps(data, indent=2)}")

        except Exception as e:
            print(f"Error processing message: {e}")

    def start(self):
        try:
            print("Connecting to MQTT broker...")
            self.client.connect("localhost", 1883, 60)
            print("Starting subscriber loop...")
            self.client.loop_forever()
        except KeyboardInterrupt:
            print("\nSubscriber stopped")
            self.producer.close()
        except Exception as e:
            print(f"Error: {e}")
            self.producer.close()


if __name__ == "__main__":
    # You can customize the Kafka broker address here
    subscriber = SensorKafkaSubscriber(kafka_broker="localhost:9092")
    subscriber.start()