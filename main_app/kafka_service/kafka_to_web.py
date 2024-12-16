from kafka import KafkaConsumer
import json
from typing import List, Dict
import socketio
import logging
import eventlet


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MaritimeDetector:
    def __init__(self, topics: List[str], bootstrap_servers: str = 'localhost:9092',
                 socket_url: str = 'http://localhost:5000'):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        # Socket.IO
        self.sio = socketio.Client(
            logger=True,
            engineio_logger=True,
            reconnection=True,
            reconnection_attempts=5,
            reconnection_delay=1,
            reconnection_delay_max=5
        )

        self.socket_url = socket_url
        self.is_connected = False

        # Socket.IO event handlers
        self.setup_socketio_handlers()

        # Initial connection
        self.connect_socket()

        logger.info(f"Subscribed to Kafka topics: {topics}")

    def setup_socketio_handlers(self):
        @self.sio.event
        def connect():
            logger.info("Connected to Socket.IO server")
            self.is_connected = True

        @self.sio.event
        def disconnect():
            logger.info("Disconnected from Socket.IO server")
            self.is_connected = False

        @self.sio.event
        def connect_error(data):
            logger.error(f"Connection error: {data}")
            self.is_connected = False

    def connect_socket(self):
        if not self.is_connected:
            try:
                logger.info("Attempting to connect to Socket.IO server...")
                self.sio.connect(
                    self.socket_url,
                    transports=['websocket'],
                    wait=True
                )
                eventlet.sleep(1)
            except Exception as e:
                logger.error(f"Failed to connect: {e}")

    def send_to_socket(self, message_data: Dict):
        # Send data to Socket.IO
        if not self.is_connected:
            self.connect_socket()

        if self.is_connected:
            try:
                logger.debug(f"Sending data: {message_data}")
                self.sio.emit('sensor_update', message_data)
                logger.info(f"Successfully sent {message_data['data']['type']} data")
            except Exception as e:
                logger.error(f"Error sending data: {e}")
                self.is_connected = False
        else:
            logger.warning("Not connected to Socket.IO server")

    def process_sensor_data(self, sensor_type: str, data: Dict, timestamp: str):
        # Process sensor data and send updates
        detected_objects = data.get('detected_objects', [])

        for obj in detected_objects:
            try:
                if sensor_type == 'radar' and obj.get('object_type') == 'Ship':
                    mmsi = obj.get('mmsi')
                    if mmsi:
                        logger.debug(f"Processing ship data for MMSI: {mmsi}")
                        danger, is_hostile = 50, False
                        message_data = {
                            "data": {
                                "type": "ship",
                                "timestamp": timestamp,
                                "detected_object": {
                                    "mmsi": mmsi,
                                    "object_type": "Ship",
                                    "latitude": obj.get('latitude'),
                                    "longitude": obj.get('longitude'),
                                    "speed_knots": obj.get('speed_knots'),
                                    "status": "Active",
                                    "object_size": obj.get('object_size', 100),
                                    "danger": danger,
                                    "is_hostile": is_hostile
                                }
                            }
                        }
                        self.send_to_socket(message_data)

                elif sensor_type == 'sonar':
                    submarine_id = obj.get('submarine_id')
                    if submarine_id:
                        logger.debug(f"Processing submarine data for ID: {submarine_id}")
                        danger, is_hostile = 70, True
                        message_data = {
                            "data": {
                                "type": "submarine",
                                "timestamp": timestamp,
                                "detected_object": {
                                    "submarine_id": submarine_id,
                                    "object_type": "Submarine",
                                    "latitude": obj.get('latitude'),
                                    "longitude": obj.get('longitude'),
                                    "speed_knots": obj.get('speed_knots'),
                                    "status": "Moving",
                                    "object_size": obj.get('object_size', 200),
                                    "danger": danger,
                                    "is_hostile": is_hostile
                                }
                            }
                        }
                        self.send_to_socket(message_data)

            except Exception as e:
                logger.error(f"Error processing object: {e}")


def main():
    topics = [
        'thermal_sensor_data',
        'radar_sensor_data',
        'sonar_sensor_data'
    ]

    logger.info("Starting Maritime Detector...")
    detector = MaritimeDetector(topics)

    try:
        for message in detector.consumer:
            try:
                sensor_type = message.value.get('type')
                data = message.value.get('data', {})
                timestamp = message.value.get('timestamp')

                detector.process_sensor_data(sensor_type, data, timestamp)
                eventlet.sleep(0)

            except Exception as e:
                logger.error(f"Error processing message: {e}")
                continue

    except KeyboardInterrupt:
        logger.info("Stopping detector...")
    finally:
        detector.consumer.close()
        if detector.is_connected:
            detector.sio.disconnect()


if __name__ == "__main__":
    main()