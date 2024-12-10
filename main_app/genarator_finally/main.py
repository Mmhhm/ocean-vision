# import asyncio
# import random
# from datetime import datetime, UTC
# from typing import Dict
# import json
# from models.ship import Ship
# from models.submarine import Submarine
# from sensors.thermal_sensor import ThermalSensor
# from sensors.radar_sensor import RadarSensor
# from sensors.sonar_sensor import SonarSensor
# from sensors.weather_sensor import WeatherSensor
#
#
# class SensorDataManager:
#     def __init__(self):
#         self.ships: Dict[str, Ship] = {}
#         self.submarines: Dict[str, Submarine] = {}
#         self.last_mmsi = 0
#         self.last_submarine_id = 0
#
#         # Initialize initial ships
#         for _ in range(3):
#             self._create_new_ship()
#
#         # Initialize first submarine
#         self._create_new_submarine()
#
#         # Initialize sensors
#         self.sensors = {
#             'thermal': ThermalSensor(),
#             'radar': RadarSensor(),
#             'sonar': SonarSensor(),
#             'weather': WeatherSensor()
#         }
#
#     def _create_new_ship(self):
#         """Create a new ship with random parameters"""
#         self.last_mmsi += 1
#         mmsi = f"98765{self.last_mmsi:04d}"
#
#         base_lat, base_lon = 34.0522, -118.2437
#         lat = base_lat + random.uniform(-0.1, 0.1)
#         lon = base_lon + random.uniform(-0.1, 0.1)
#
#         self.ships[mmsi] = Ship(
#             mmsi=mmsi,
#             latitude=lat,
#             longitude=lon
#         )
#         print(f"New ship created - MMSI: {mmsi} at position: {lat:.4f}, {lon:.4f}")
#
#     def _create_new_submarine(self):
#         """Create a new submarine with random parameters"""
#         self.last_submarine_id += 1
#         submarine_id = f"SUB{self.last_submarine_id:04d}"
#
#         base_lat, base_lon = 34.0522, -118.2437
#         lat = base_lat + random.uniform(-0.1, 0.1)
#         lon = base_lon + random.uniform(-0.1, 0.1)
#
#         self.submarines[submarine_id] = Submarine(
#             submarine_id=submarine_id,
#             latitude=lat,
#             longitude=lon
#         )
#         print(f"New submarine created - ID: {submarine_id} at position: {lat:.4f}, {lon:.4f}")
#
#     def _maybe_add_new_ship(self):
#         """Randomly decide whether to add a new ship"""
#         if random.random() < 0.1:  # 10% chance every update
#             self._create_new_ship()
#
#     def _maybe_add_new_submarine(self):
#         """Randomly decide whether to add a new submarine"""
#         if len(self.submarines) < 3 and random.random() < 0.2:  # 5% chance, max 3 submarines
#             self._create_new_submarine()
#
#     def _remove_old_ships(self, max_age_seconds: int = 300):
#         """Remove ships that have been in the system too long"""
#         current_time = datetime.now(UTC)
#         ships_to_remove = []
#
#         for mmsi, ship in self.ships.items():
#             age = (current_time - ship.creation_time).total_seconds()
#             if age > max_age_seconds:
#                 ships_to_remove.append(mmsi)
#
#         for mmsi in ships_to_remove:
#             del self.ships[mmsi]
#             print(f"Ship removed - MMSI: {mmsi} (aged out)")
#
#     def _remove_old_submarines(self, max_age_seconds: int = 200):
#         """Remove submarines that have been in the system too long"""
#         current_time = datetime.now(UTC)
#         subs_to_remove = []
#
#         for sub_id, submarine in self.submarines.items():
#             age = (current_time - submarine.creation_time).total_seconds()
#             if age > max_age_seconds:
#                 subs_to_remove.append(sub_id)
#
#         for sub_id in subs_to_remove:
#             del self.submarines[sub_id]
#             print(f"Submarine removed - ID: {sub_id} (aged out)")
#
#     def update_vehicles(self, seconds_elapsed: float):
#         """Update all vehicles positions and maybe add/remove vehicles"""
#         # Update existing vehicles
#         for ship in self.ships.values():
#             ship.move(seconds_elapsed)
#
#         for submarine in self.submarines.values():
#             submarine.move(seconds_elapsed)
#
#         # Maybe add new vehicles
#         self._maybe_add_new_ship()
#         self._maybe_add_new_submarine()
#
#         # Remove old vehicles
#         self._remove_old_ships()
#         self._remove_old_submarines()
#
#     def get_all_sensor_data(self, observer_lat: float, observer_lon: float) -> dict:
#         """Get data from all sensors"""
#         return {
#             sensor_name: sensor.generate_data(
#                 observer_lat,
#                 observer_lon,
#                 self.ships,
#                 self.submarines if sensor_name == 'sonar' else None
#             )
#             for sensor_name, sensor in self.sensors.items()
#         }
#
#
# async def main():
#     manager = SensorDataManager()
#
#     try:
#         while True:
#             data = manager.get_all_sensor_data(34.0522, -118.2437)
#
#             # Print sensor data in a nice format
#             print(json.dumps(data, indent=2))
#
#             # Update and wait
#             manager.update_vehicles(5)
#             await asyncio.sleep(5)
#
#     except KeyboardInterrupt:
#         print("\nStopping data generation...")
#     except Exception as e:
#         print(f"\nError occurred: {e}")
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
#


import asyncio
import random
from datetime import datetime, UTC
from typing import Dict
import json
from models.ship import Ship
from models.submarine import Submarine
from sensors.thermal_sensor import ThermalSensor
from sensors.radar_sensor import RadarSensor
from sensors.sonar_sensor import SonarSensor
from sensors.weather_sensor import WeatherSensor
import paho.mqtt.client as mqtt
import time


class SensorDataManager:
    def __init__(self, mqtt_client):
        self.ships: Dict[str, Ship] = {}
        self.submarines: Dict[str, Submarine] = {}
        self.last_mmsi = 0
        self.last_submarine_id = 0
        self.mqtt_client = mqtt_client

        # Initialize initial ships
        for _ in range(3):
            self._create_new_ship()

        # Initialize first submarine
        self._create_new_submarine()

        # Initialize sensors
        self.sensors = {
            'thermal': ThermalSensor(),
            'radar': RadarSensor(),
            'sonar': SonarSensor(),
            'weather': WeatherSensor()
        }

    def _create_new_ship(self):
        """Create a new ship with random parameters"""
        self.last_mmsi += 1
        mmsi = f"98765{self.last_mmsi:04d}"

        base_lat, base_lon = 34.0522, -118.2437
        lat = base_lat + random.uniform(-0.1, 0.1)
        lon = base_lon + random.uniform(-0.1, 0.1)

        self.ships[mmsi] = Ship(
            mmsi=mmsi,
            latitude=lat,
            longitude=lon
        )

    def _create_new_submarine(self):
        """Create a new submarine with random parameters"""
        self.last_submarine_id += 1
        submarine_id = f"SUB{self.last_submarine_id:04d}"

        base_lat, base_lon = 34.0522, -118.2437
        lat = base_lat + random.uniform(-0.1, 0.1)
        lon = base_lon + random.uniform(-0.1, 0.1)

        self.submarines[submarine_id] = Submarine(
            submarine_id=submarine_id,
            latitude=lat,
            longitude=lon
        )

    def _maybe_add_new_ship(self):
        """Randomly decide whether to add a new ship"""
        if random.random() < 0.1:  # 10% chance every update
            self._create_new_ship()

    def _maybe_add_new_submarine(self):
        """Randomly decide whether to add a new submarine"""
        if len(self.submarines) < 3 and random.random() < 0.2:  # 20% chance, max 3 submarines
            self._create_new_submarine()

    def _remove_old_ships(self, max_age_seconds: int = 300):
        """Remove ships that have been in the system too long"""
        current_time = datetime.now(UTC)
        ships_to_remove = []

        for mmsi, ship in self.ships.items():
            age = (current_time - ship.creation_time).total_seconds()
            if age > max_age_seconds:
                ships_to_remove.append(mmsi)

        for mmsi in ships_to_remove:
            del self.ships[mmsi]

    def _remove_old_submarines(self, max_age_seconds: int = 200):
        """Remove submarines that have been in the system too long"""
        current_time = datetime.now(UTC)
        subs_to_remove = []

        for sub_id, submarine in self.submarines.items():
            age = (current_time - submarine.creation_time).total_seconds()
            if age > max_age_seconds:
                subs_to_remove.append(sub_id)

        for sub_id in subs_to_remove:
            del self.submarines[sub_id]

    def update_vehicles(self, seconds_elapsed: float):
        """Update all vehicles positions and maybe add/remove vehicles"""
        # Update existing vehicles
        for ship in self.ships.values():
            ship.move(seconds_elapsed)

        for submarine in self.submarines.values():
            submarine.move(seconds_elapsed)

        # Maybe add new vehicles
        self._maybe_add_new_ship()
        self._maybe_add_new_submarine()

        # Remove old vehicles
        self._remove_old_ships()
        self._remove_old_submarines()

    def publish_sensor_data(self, observer_lat: float, observer_lon: float):
        """Get data from each sensor and publish to MQTT"""
        for sensor_name, sensor in self.sensors.items():
            # Get sensor data
            data = sensor.generate_data(
                observer_lat,
                observer_lon,
                self.ships,
                self.submarines if sensor_name == 'sonar' else None
            )

            # Create message with metadata
            message = {
                "type": sensor_name,
                "timestamp": datetime.now(UTC).isoformat(),
                "data": data
            }

            # Publish to MQTT
            topic = f"sensors/{sensor_name}/{data['sensor_id']}"
            self.mqtt_client.publish(topic, json.dumps(message), qos=1)


class MQTTManager:
    def __init__(self, broker="localhost", port=1883):
        # Initialize MQTT client
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port

        # Setup MQTT callbacks
        self.client.on_connect = self.on_connect

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
        else:
            print(f"Failed to connect to MQTT broker with code: {rc}")

    def start(self):
        """Connect to MQTT broker"""
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")
            raise

    def stop(self):
        """Stop MQTT client"""
        self.client.loop_stop()
        self.client.disconnect()


async def main():
    try:
        # Initialize MQTT
        mqtt_manager = MQTTManager()
        mqtt_manager.start()

        # Initialize sensor manager
        manager = SensorDataManager(mqtt_manager.client)

        while True:
            # Publish sensor data
            manager.publish_sensor_data(34.0522, -118.2437)

            # Update vehicles
            manager.update_vehicles(5)

            # Wait before next update
            await asyncio.sleep(5)

    except KeyboardInterrupt:
        print("\nStopping data generation...")
        mqtt_manager.stop()
    except Exception as e:
        print(f"\nError occurred: {e}")
        mqtt_manager.stop()


if __name__ == "__main__":
    asyncio.run(main())