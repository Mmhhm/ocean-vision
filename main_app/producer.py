from confluent_kafka import Producer
import json
import random
import time
from datetime import datetime

producer = Producer({
    'bootstrap.servers': 'localhost:9092',  
    'client.id': 'python-producer'
})

def generate_heat_sensor_data():
    return {
        "sensor_id": "THERMAL-001",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "detected_objects": [
            {
            
                "distance_km": round(random.uniform(1.0, 10.0), 2),  
                "bearing_degrees": random.randint(0, 360), 
                "heat_temperature_celsius": round(random.uniform(30.0, 45.0), 2),  
                # "latitude": round(random.uniform(-90, 90), 4), 
                # "mmsi": str(random.randint(100000000, 999999999)),
                # "longitude": round(random.uniform(-180, 180), 4), 
                # "status": random.choice(["Moving", "Stationary"])

            }
        ]
    }


def generate_radar_sensor_data():
    return {
        "radar_id": "Radar-01",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "detected_objects": [
            {
       
                "distance_km": round(random.uniform(1.0, 10.0), 2),  
                "bearing_degrees": random.randint(0, 360),  
                # "latitude": round(random.uniform(-90, 90), 4), 
                # "longitude": round(random.uniform(-180, 180), 4),  
                # "speed_knots": round(random.uniform(0, 20), 2),  
                # "status": random.choice(["Underway", "Docked"]),  
                # "mmsi": str(random.randint(100000000, 999999999)), 
                # "object_type": random.choice(["Ship", "Boat", "Aircraft"]),  
                "object_size": random.randint(100, 1000)  
            }
        ]
    }

def generate_sonar_data():
    return {
        "sonar_id": "Sonar-01",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "detected_objects": [
            {
            
                "depth_meters": round(random.uniform(100, 1000), 2),
                "distance_km": round(random.uniform(5.0, 20.0), 2),
                "bearing_degrees": random.randint(0, 360),
                # "object_type": random.choice(["Submarine", "Fish", "Debris"]),
                # "latitude": round(random.uniform(-90, 90), 4),
                # "longitude": round(random.uniform(-180, 180), 4),
                # "speed_knots": random.randint(0, 10),
                # "object_shape": random.choice(["Cylindrical", "Spherical", "Irregular"]),
                "object_material": random.choice(["Metal", "Wood", "Plastic"]),
                "object_size": random.randint(100, 1000),  # in square meters
                # "status": random.choice(["Stationary", "Moving"])
            }
        ]
    }


def generate_weather_data():
    return {
        "coord": {
            "lon": round(random.uniform(-180, 180), 2),
            "lat": round(random.uniform(-90, 90), 2)
        },
        "weather": [
            {
                "id": random.randint(800, 804),
                "main": random.choice(["Clear", "Clouds", "Rain", "Snow"]),
                "description": random.choice(["clear sky", "few clouds", "overcast clouds", "light rain", "heavy snow"]),
                "icon": random.choice(["01d", "02d", "03d", "04d", "10d"])
            }
        ],
        "base": "stations",
        "main": {
            "temp": round(random.uniform(280, 300), 2),  
            "feels_like": round(random.uniform(280, 300), 2),
            "temp_min": round(random.uniform(280, 290), 2),
            "temp_max": round(random.uniform(290, 300), 2),
            "pressure": random.randint(1000, 1020),
            "humidity": random.randint(60, 90),
            "sea_level": random.randint(1000, 1020),
            "grnd_level": random.randint(1000, 1020)
        },
        "visibility": random.choice([10000, 5000, 2000]),
        "wind": {
            "speed": round(random.uniform(0, 20), 2),
            "deg": random.randint(0, 360),
            "gust": round(random.uniform(0, 20), 2)
        },
        "clouds": {
            "all": random.randint(0, 100)
        },
        "dt": int(time.time()),
        "sys": {
            "sunrise": int(time.time()) - 10000,
            "sunset": int(time.time()) + 10000
        },
        "timezone": random.randint(-43200, 43200),
        "id": 0,
        "name": "Random Location",
        "cod": 200
    }

def send_message(topic, message):
    try:
        message_str = json.dumps(message)
        producer.produce(topic, value=message_str)
        producer.flush()
        print(f"Message sent to topic '{topic}': {message_str}")
    except Exception as e:
        print(f"Error producing message: {e}")

try:
    i=0
    while i == 0:
        send_message('heat_sensor_topic', generate_heat_sensor_data())
        time.sleep(1)

        send_message('radar_sensor_topic', generate_radar_sensor_data())
        time.sleep(1)

        send_message('sonar_sensor_topic', generate_sonar_data())
        time.sleep(1)

        send_message('weather_data_topic', generate_weather_data())
        time.sleep(5)  
        i +=1
except KeyboardInterrupt:
    print("Exiting the loop.")
