from datetime import datetime
from typing import Dict, Any, Optional
from .base_sensor import BaseSensor

class RadarSensor(BaseSensor):
    def __init__(self):
        super().__init__(
            sensor_id="RADAR-001",
            kafka_topic="sensor.radar"
        )

    def generate_data(self, observer_lat: float, observer_lon: float, ships: dict, submarines: Optional[dict] = None) -> \
    Dict[str, Any]:
        detected_objects = []

        for ship in ships.values():
            distance, bearing = self.calculate_distance_bearing(
                observer_lat, observer_lon, ship.latitude, ship.longitude
            )

            if distance <= 15:  # Radar can detect ships at longer range
                detected_objects.append({
                    "mmsi": ship.mmsi,
                    "object_type": "Ship",
                    "distance_km": round(distance, 1),
                    "bearing_degrees": round(bearing),
                    "latitude": round(ship.latitude, 4),
                    "longitude": round(ship.longitude, 4),
                    "speed_knots": round(ship.speed, 1),
                    "status": "Underway" if ship.speed > 2 else "Stationary",
                    "object_size": round(ship.size)
                })

        data = {
            "sensor_id": self.sensor_id,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "detected_objects": detected_objects
        }

        return data