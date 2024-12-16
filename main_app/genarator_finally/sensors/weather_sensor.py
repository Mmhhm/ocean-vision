from datetime import datetime, timedelta
import random
from typing import Dict, Any, Optional
from .base_sensor import BaseSensor


class WeatherSensor(BaseSensor):
    def __init__(self):
        super().__init__(
            sensor_id="WEATHER-001",
            kafka_topic="sensor.weather"
        )

    def generate_data(self, observer_lat: float, observer_lon: float, ships: dict, submarines: Optional[dict] = None) -> \
    Dict[str, Any]:
        temp_kelvin = random.uniform(290, 300)
        timestamp = datetime.utcnow()

        data = {
            "coord": {
                "lon": round(observer_lon),
                "lat": round(observer_lat)
            },
            "weather": [{
                "id": random.choice([800, 801, 802, 803, 804]),
                "main": "Clouds",
                "description": "overcast clouds",
                "icon": "04d"
            }],
            "base": "stations",
            "main": {
                "temp": round(temp_kelvin, 2),
                "feels_like": round(temp_kelvin + random.uniform(-1, 1), 2),
                "temp_min": round(temp_kelvin - random.uniform(0, 2), 2),
                "temp_max": round(temp_kelvin + random.uniform(0, 2), 2),
                "pressure": round(random.uniform(1000, 1020)),
                "humidity": round(random.uniform(60, 90)),
                "sea_level": round(random.uniform(1000, 1020)),
                "grnd_level": round(random.uniform(1000, 1020))
            },
            "visibility": round(random.uniform(5000, 10000)),
            "wind": {
                "speed": round(random.uniform(5, 15), 2),
                "deg": round(random.uniform(0, 360)),
                "gust": round(random.uniform(8, 20), 2)
            },
            "clouds": {
                "all": round(random.uniform(0, 100))
            },
            "dt": int(timestamp.timestamp()),
            "sys": {
                "sunrise": int((timestamp - timedelta(hours=6)).timestamp()),
                "sunset": int((timestamp + timedelta(hours=6)).timestamp())
            },
            "timezone": -32400,
            "sensor_id": self.sensor_id
        }

        return data