from datetime import datetime
from typing import Dict, Any, Optional
from .base_sensor import BaseSensor

class ThermalSensor(BaseSensor):
    def __init__(self):
        super().__init__(
            sensor_id="THERMAL-001",
            kafka_topic="sensor.thermal"
        )

    def generate_data(self, observer_lat: float, observer_lon: float, ships: dict, submarines: Optional[dict] = None) -> \
    Dict[str, Any]:
        detected_objects = []

        for ship in ships.values():
            distance, bearing = self.calculate_distance_bearing(
                observer_lat, observer_lon, ship.latitude, ship.longitude
            )

            if distance <= 10:  # Only ships within 10 km
                detected_objects.append({
                    "mmsi": ship.mmsi,
                    "distance_km": round(distance, 1),
                    "bearing_degrees": round(bearing),
                    "heat_temperature_celsius": round(ship.heat_signature, 1),
                    "latitude": round(ship.latitude, 4),
                    "longitude": round(ship.longitude, 4),
                    "status": "Moving" if ship.speed > 2 else "Stationary"
                })

        data = {
            "sensor_id": self.sensor_id,
            "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "detected_objects": detected_objects
        }

        self.send_to_kafka(data)
        return data