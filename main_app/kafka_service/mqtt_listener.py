# import paho.mqtt.client as mqtt
# from kafka import KafkaProducer
# import json
#
#
# class SensorKafkaSubscriber:
#     def __init__(self, mqtt_broker="localhost", mqtt_port=1883, kafka_broker="localhost:9092"):
#         # MQTT setup
#         self.client = mqtt.Client()
#         self.client.on_connect = self.on_connect
#         self.client.on_message = self.on_message
#
#         # Kafka setup
#         self.producer = KafkaProducer(
#             bootstrap_servers=[kafka_broker],
#             value_serializer=lambda x: json.dumps(x).encode('utf-8')
#         )
#
#         # Kafka topics mapping
#         self.kafka_topics = {
#             'thermal': 'thermal_sensor_data',
#             'radar': 'radar_sensor_data',
#             'sonar': 'sonar_sensor_data',
#             'weather': 'weather_sensor_data'
#         }
#
#     def on_connect(self, client, userdata, flags, rc):
#         print("Connected to MQTT broker with result code " + str(rc))
#         # Subscribe to all sensor topics
#         self.client.subscribe("sensors/#")
#
#     def on_message(self, client, userdata, msg):
#         try:
#             # Parse the JSON message
#             data = json.loads(msg.payload)
#             sensor_type = data['type']
#
#             # Get corresponding Kafka topic
#             kafka_topic = self.kafka_topics.get(sensor_type)
#
#             if kafka_topic:
#                 # Send to Kafka
#                 self.producer.send(kafka_topic, value=data)
#                 self.producer.flush()
#                 print(f"Sent {sensor_type} data to Kafka topic: {kafka_topic}")
#
#                 # Optional: Print the data for debugging
#                 print(f"Data: {json.dumps(data, indent=2)}")
#
#         except Exception as e:
#             print(f"Error processing message: {e}")
#
#     def start(self):
#         try:
#             print("Connecting to MQTT broker...")
#             self.client.connect("localhost", 1883, 60)
#             print("Starting subscriber loop...")
#             self.client.loop_forever()
#         except KeyboardInterrupt:
#             print("\nSubscriber stopped")
#             self.producer.close()
#         except Exception as e:
#             print(f"Error: {e}")
#             self.producer.close()
#
#
# if __name__ == "__main__":
#     # You can customize the Kafka broker address here
#     subscriber = SensorKafkaSubscriber(kafka_broker="localhost:9092")
#     subscriber.start()


from paho.mqtt import client as mqtt
from kafka import KafkaProducer
import json
from typing import Dict


class MQTTtoKafkaBridge:
    """Bridge for forwarding MQTT sensor messages to Kafka topics"""

    # Mapping of sensor types to Kafka topics
    TOPICS: Dict[str, str] = {
        'thermal': 'thermal_sensor_data',
        'radar': 'radar_sensor_data',
        'sonar': 'sonar_sensor_data',
        'weather': 'weather_sensor_data'
    }

    def __init__(self):
        # Initialize Kafka producer
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=self._serialize_json
        )

        # Initialize MQTT client
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self._on_mqtt_connect
        self.mqtt_client.on_message = self._on_mqtt_message

    @staticmethod
    def _serialize_json(data: dict) -> bytes:
        """Serialize data to JSON bytes"""
        return json.dumps(data).encode('utf-8')

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """Handle MQTT connection"""
        if rc == 0:
            print("Connected to MQTT broker")
            client.subscribe("sensors/#")
        else:
            print(f"Failed to connect to MQTT broker with code: {rc}")

    def _on_mqtt_message(self, client, userdata, msg):
        """Process incoming MQTT messages and forward to Kafka"""
        try:
            # Parse message
            data = json.loads(msg.payload)
            sensor_type = data['type']

            # Get corresponding Kafka topic
            kafka_topic = self.TOPICS.get(sensor_type)
            if kafka_topic:
                # Forward to Kafka
                self.producer.send(kafka_topic, data)
                print(f"Forwarded {sensor_type} data to Kafka topic: {kafka_topic}")

        except json.JSONDecodeError:
            print(f"Invalid JSON message received: {msg.payload}")
        except KeyError:
            print(f"Message missing sensor type: {data}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def run(self):
        """Start the bridge"""
        try:
            print("Starting MQTT to Kafka bridge...")
            self.mqtt_client.connect("localhost", 1883)
            self.mqtt_client.loop_forever()

        except KeyboardInterrupt:
            print("\nStopping bridge...")
        finally:
            self.producer.close()
            self.mqtt_client.disconnect()


if __name__ == "__main__":
    bridge = MQTTtoKafkaBridge()
    bridge.run()