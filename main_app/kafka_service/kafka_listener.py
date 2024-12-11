from kafka import KafkaConsumer
import json
from typing import List, Dict, Tuple
from datetime import datetime
import math


class MaritimeDetector:
    def __init__(self, topics: List[str], bootstrap_servers: str = 'localhost:9092'):
        self.consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.ships_data = {}
        self.submarines_data = {}
        print(f"Subscribed to topics: {topics}")

    def calculate_threat_levels(self, obj_data: Dict) -> Tuple[float, bool]:
        """
        Calculate detailed threat level based on multiple parameters
        Returns: (danger_level, is_hostile)
        """
        danger_score = 0.0
        weights = {
            'temperature': 0.25,
            'distance': 0.20,
            'speed': 0.15,
            'size': 0.15,
            'bearing': 0.15,
            'status': 0.10
        }

        # Temperature analysis
        temp = obj_data.get('heat_temperature_celsius')
        if temp is not None:
            temp_score = min(100, max(0, (temp - 35) * 5))  # Scale from 35-55°C
            danger_score += temp_score * weights['temperature']

        # Distance analysis
        distance = obj_data.get('distance_km')
        if distance is not None:
            distance_score = min(100, max(0, (15 - distance) * 10))  # Inverse scale from 0-15km
            danger_score += distance_score * weights['distance']

        # Speed analysis
        speed = obj_data.get('speed_knots')
        if speed is not None:
            speed_score = min(100, max(0, (speed - 5) * 8))  # Scale from 5-17.5 knots
            danger_score += speed_score * weights['speed']

        # Size analysis
        size = obj_data.get('object_size')
        if size is not None:
            # Military ships typically 400-800
            size_factor = abs(600 - size) / 200  # Distance from ideal military size
            size_score = min(100, max(0, (1 - size_factor) * 100))
            danger_score += size_score * weights['size']

        # Bearing analysis
        bearing = obj_data.get('bearing_degrees')
        if bearing is not None:
            # Consider bearings outside commercial routes (120-240) more dangerous
            bearing_score = 0
            if bearing < 120 or bearing > 240:
                angle_diff = min(abs(bearing - 120), abs(bearing - 240))
                bearing_score = min(100, (angle_diff / 1.2))
            danger_score += bearing_score * weights['bearing']

        # Status analysis
        status = obj_data.get('status', '').lower()
        if status == 'stationary':
            danger_score += 100 * weights['status']
        elif status == 'unknown':
            danger_score += 50 * weights['status']

        # Round to 3 decimal places
        danger_score = round(danger_score, 3)

        # Determine hostility (true if multiple high-risk factors)
        high_risk_count = sum([
            1 for score in [temp_score if temp is not None else 0,
                            distance_score if distance is not None else 0,
                            speed_score if speed is not None else 0,
                            size_score if size is not None else 0,
                            bearing_score if bearing is not None else 0]
            if score > 70
        ])

        return danger_score, high_risk_count >= 3

    def calculate_submarine_threat(self, sub_data: Dict) -> Tuple[float, bool]:
        """
        Calculate detailed submarine threat level
        Returns: (danger_level, is_hostile)
        """
        danger_score = 0.0
        weights = {
            'depth': 0.30,
            'distance': 0.25,
            'speed': 0.20,
            'size': 0.15,
            'bearing': 0.10
        }

        # Depth analysis
        depth = sub_data.get('depth_meters')
        if depth is not None:
            if depth < 50:  # Very shallow
                depth_score = 100
            elif depth < 100:  # Periscope depth
                depth_score = 80
            else:
                depth_score = max(0, 100 - (depth - 100) * 0.5)
            danger_score += depth_score * weights['depth']

        # Distance analysis
        distance = sub_data.get('distance_km')
        if distance is not None:
            distance_score = min(100, max(0, (12 - distance) * 10))
            danger_score += distance_score * weights['distance']

        # Speed analysis
        speed = sub_data.get('speed_knots')
        if speed is not None:
            if speed < 1:  # Stationary
                speed_score = 90
            else:
                speed_score = min(100, max(0, speed * 15))
            danger_score += speed_score * weights['speed']

        # Size analysis
        size = sub_data.get('object_size')
        if size is not None:
            # Typical military submarine size range
            size_factor = abs(550 - size) / 150
            size_score = min(100, max(0, (1 - size_factor) * 100))
            danger_score += size_score * weights['size']

        # Bearing analysis
        bearing = sub_data.get('bearing_degrees')
        if bearing is not None:
            # Consider unusual approach angles more dangerous
            bearing_score = min(100, abs(math.sin(math.radians(bearing))) * 100)
            danger_score += bearing_score * weights['bearing']

        # Round to 3 decimal places
        danger_score = round(danger_score, 3)

        # Determine hostility
        high_risk_count = sum([
            1 for score in [depth_score if depth is not None else 0,
                            distance_score if distance is not None else 0,
                            speed_score if speed is not None else 0,
                            size_score if size is not None else 0,
                            bearing_score if bearing is not None else 0]
            if score > 70
        ])

        return danger_score, high_risk_count >= 3

    def update_object_data(self, sensor_type: str, data: Dict, timestamp: str):
        """Update object data from different sensors"""
        detected_objects = data.get('detected_objects', [])

        for obj in detected_objects:
            if sensor_type == 'radar' and obj.get('object_type') == 'Ship':
                mmsi = obj.get('mmsi')
                if mmsi:
                    danger, is_hostile = self.calculate_threat_levels(obj)
                    self.ships_data[mmsi] = {
                        "data": {
                            "type": "ship",
                            "timestamp": timestamp,
                            "detected_object": {
                                "mmsi": mmsi,
                                "distance_km": obj.get('distance_km'),
                                "bearing_degrees": obj.get('bearing_degrees'),
                                "latitude": obj.get('latitude'),
                                "longitude": obj.get('longitude'),
                                "status": obj.get('status'),
                                "speed_knots": obj.get('speed_knots'),
                                "object_size": obj.get('object_size'),
                                "heat_temperature_celsius": None,
                                "danger": danger,
                                "is_hostile": is_hostile
                            }
                        }
                    }

            elif sensor_type == 'thermal':
                mmsi = obj.get('mmsi')
                if mmsi and mmsi in self.ships_data:
                    self.ships_data[mmsi]["data"]["detected_object"]["heat_temperature_celsius"] = obj.get(
                        'heat_temperature_celsius')
                    # Recalculate with new temperature data
                    danger, is_hostile = self.calculate_threat_levels(self.ships_data[mmsi]["data"]["detected_object"])
                    self.ships_data[mmsi]["data"]["detected_object"].update({
                        "danger": danger,
                        "is_hostile": is_hostile
                    })

            elif sensor_type == 'sonar':
                submarine_id = obj.get('submarine_id')
                if submarine_id:
                    danger, is_hostile = self.calculate_submarine_threat(obj)
                    self.submarines_data[submarine_id] = {
                        "data": {
                            "type": "submarine",
                            "timestamp": timestamp,
                            "detected_object": {
                                "submarine_id": submarine_id,
                                "object_type": "Submarine",
                                "depth_meters": obj.get('depth_meters'),
                                "distance_km": obj.get('distance_km'),
                                "bearing_degrees": obj.get('bearing_degrees'),
                                "latitude": obj.get('latitude'),
                                "longitude": obj.get('longitude'),
                                "speed_knots": obj.get('speed_knots'),
                                "object_shape": obj.get('object_shape', "Cylindrical"),
                                "object_material": obj.get('object_material', "Metal"),
                                "object_size": obj.get('object_size'),
                                "status": obj.get('status', "Moving"),
                                "danger": danger,
                                "is_hostile": is_hostile
                            }
                        }
                    }


def main():
    topics = [
        'thermal_sensor_data',
        'radar_sensor_data',
        'sonar_sensor_data'
    ]

    print("Starting Maritime Detector...")
    detector = MaritimeDetector(topics)

    try:
        for message in detector.consumer:
            sensor_type = message.value.get('type', message.topic.split('_')[0])
            data = message.value.get('data', {})
            timestamp = message.value.get('timestamp')

            detector.update_object_data(sensor_type, data, timestamp)

            print("\n=== Current Maritime Status ===")
            if detector.ships_data:
                print("\nShips:")
                for ship_data in detector.ships_data.values():
                    print(json.dumps(ship_data, indent=2))

            if detector.submarines_data:
                print("\nSubmarines:")
                for sub_data in detector.submarines_data.values():
                    print(json.dumps(sub_data, indent=2))

    except KeyboardInterrupt:
        print("\nStopping detector...")
    finally:
        detector.consumer.close()


if __name__ == "__main__":
    main()