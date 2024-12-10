# from abc import ABC, abstractmethod
# from datetime import datetime
# from typing import Dict, Any
# import json
#
# class BaseSensor(ABC):
#     def __init__(self, sensor_id: str, kafka_topic: str):
#         self.sensor_id = sensor_id
#         self.kafka_topic = kafka_topic
#
#     @abstractmethod
#     def generate_data(self, observer_lat: float, observer_lon: float, ships: dict) -> Dict[str, Any]:
#         pass
#
#     def send_to_kafka(self, data: Dict[str, Any]):
#         # Instead of sending to Kafka, we'll just print the topic and data
#         print(f"\nWould send to Kafka topic '{self.kafka_topic}':")
#         print(json.dumps(data, indent=2))
#
#     def calculate_distance_bearing(self, lat1: float, lon1: float, lat2: float, lon2: float) -> tuple:
#         import math
#         lat1, lon1 = math.radians(lat1), math.radians(lon1)
#         lat2, lon2 = math.radians(lat2), math.radians(lon2)
#
#         d_lon = lon2 - lon1
#         y = math.sin(d_lon) * math.cos(lat2)
#         x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
#         bearing = math.degrees(math.atan2(y, x)) % 360
#
#         d_lat = lat2 - lat1
#         a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
#         c = 2 * math.asin(math.sqrt(a))
#         distance = 6371 * c  # Earth's radius * c = distance in km
#
#         return distance, bearing



from abc import ABC, abstractmethod
from datetime import datetime, UTC
from typing import Dict, Any, Optional
import json

class BaseSensor(ABC):
    def __init__(self, sensor_id: str, kafka_topic: str):
        self.sensor_id = sensor_id
        self.kafka_topic = kafka_topic

    @abstractmethod
    @abstractmethod
    def generate_data(self, observer_lat: float, observer_lon: float, ships: dict, submarines: Optional[dict] = None) -> \
    Dict[str, Any]:
        pass

    def send_to_kafka(self, data: Dict[str, Any]):
        # This method will be implemented when Kafka is connected
        pass

    def calculate_distance_bearing(self, lat1: float, lon1: float, lat2: float, lon2: float) -> tuple:
        import math
        lat1, lon1 = math.radians(lat1), math.radians(lon1)
        lat2, lon2 = math.radians(lat2), math.radians(lon2)

        d_lon = lon2 - lon1
        y = math.sin(d_lon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)
        bearing = math.degrees(math.atan2(y, x)) % 360

        d_lat = lat2 - lat1
        a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        distance = 6371 * c  # Earth's radius * c = distance in km

        return distance, bearing