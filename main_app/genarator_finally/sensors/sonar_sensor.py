from datetime import datetime, UTC
from typing import Dict, Any, Optional
from .base_sensor import BaseSensor


class SonarSensor(BaseSensor):
    def __init__(self):
        super().__init__(
            sensor_id="SONAR-001",
            kafka_topic="sensor.sonar"
        )

    def generate_data(self, observer_lat: float, observer_lon: float, ships: dict, submarines: Optional[dict] = None) -> \
    Dict[str, Any]:
        detected_objects = []

        if submarines:
            for submarine in submarines.values():
                distance, bearing = self.calculate_distance_bearing(
                    observer_lat, observer_lon,
                    submarine.latitude, submarine.longitude
                )

                if distance <= 15:  # Only detect if within 15km range
                    detected_objects.append({
                        "submarine_id": submarine.submarine_id,  # הוספת ה-ID
                        "object_type": "Submarine",
                        "depth_meters": round(submarine.depth, 1),
                        "distance_km": round(distance, 1),
                        "bearing_degrees": round(bearing),
                        "latitude": round(submarine.latitude, 4),
                        "longitude": round(submarine.longitude, 4),
                        "speed_knots": round(submarine.speed, 1),
                        "object_shape": "Cylindrical",
                        "object_material": "Metal",
                        "object_size": round(submarine.size),
                        "status": submarine.status
                    })

        data = {
            "sensor_id": self.sensor_id,
            "timestamp": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "detected_objects": detected_objects
        }

        self.send_to_kafka(data)
        return data