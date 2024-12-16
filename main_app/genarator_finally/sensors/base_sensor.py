from abc import ABC, abstractmethod
from datetime import datetime, UTC
from typing import Dict, Any, Optional
import json

class BaseSensor(ABC):
    def __init__(self, sensor_id: str, kafka_topic: str):
        self.sensor_id = sensor_id
        self.kafka_topic = kafka_topic

    @abstractmethod
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