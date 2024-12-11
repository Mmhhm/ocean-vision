# # import threading

# import paho.mqtt.client as mqtt
# # from flask import Flask
# from kafka import KafkaProducer
# import json
# import time

# # app = Flask(__name__)

# # MQTT Configuration
# MQTT_BROKER = "broker.hivemq.com"    # כתובת ה-Broker
# MQTT_PORT = 1883  # הפורט של ה-MQTT Broker
# MQTT_TOPIC = 'kafka_service/topic'  # הנושא להאזנה

# mqtt_client = mqtt.Client()

# # Kafka Configuration
# KAFKA_BROKER = 'localhost:9092'  # כתובת Kafka Broker
# KAFKA_TOPIC = 'kafka_topic'  # הנושא ב-Kafka

# # Kafka Producer
# producer = KafkaProducer(
#     bootstrap_servers=KAFKA_BROKER,
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )


# def on_connect(client, userdata, flags, rc):
#     """Callback on MQTT connection."""
#     print(f"Connected to MQTT broker with result code {rc}")
#     client.subscribe(MQTT_TOPIC)  # נרשמים לנושא
#
# def on_message(client, userdata, msg):
#     """Callback for received MQTT messages."""
#     message = msg.payload.decode()
#     print(f"Message received on topic {msg.topic}: {message}")
#
#     try:
#         # Parse the MQTT message as JSON
#         message_data = json.loads(message)
#
#         # Send the message to Kafka
#         producer.send(KAFKA_TOPIC, message_data)
#         print(f"Message sent to Kafka topic {KAFKA_TOPIC}: {message_data}")
#     except json.JSONDecodeError:
#         print("Received message is not a valid JSON.")
#
# def hello_world():
#     return 'Welcome to Kafka Service!'
#
# def send_mqtt():
#     """Route to simulate sending an MQTT message."""
#     message =
#
#     mqtt_client.publish(MQTT_TOPIC, json.dumps(message))
#     print(message)
#     return f"Message sent to MQTT topic {MQTT_TOPIC}: {message}", 200
#
#
#
#
# if __name__ == '__main__':
#     # Setup MQTT client
#
#
#     # Connect to MQTT Broker
#     mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
#
#     # Start MQTT loop in a separate thread
#
#     mqtt_client.on_connect = on_connect
#     mqtt_client.on_message = on_message
#     send_mqtt()
#
#     mqtt_client.loop_start()
#
#     # def mqtt_loop():
#     #     mqtt_client.loop_forever()
#     # mqtt_thread = threading.Thread(target=mqtt_loop)
#     # mqtt_thread.start()
#
#     # Start Flask server
#     # app.run(host='0.0.0.0',
#     #         debug=True,
#     #         port=5000)




