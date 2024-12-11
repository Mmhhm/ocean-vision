import json
import time

import paho.mqtt.client as mqtt

# הגדרות
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "test/mqtt"

client = mqtt.Client()

# התחברות ל-broker
client.connect(BROKER, PORT, 60)
# יצירת הודעה
try:
    while True:
        # יצירת הודעה
        message = {
          "type": "thermal",
          "timestamp": "2024-12-10T14:54:31.636787+00:00",
          "data": {
            "sensor_id": "THERMAL-001",
            "timestamp": "2024-12-10T14:54:31Z",
            "detected_objects": [
              {
                "mmsi": "987650002",
                "distance_km": 6.9,
                "bearing_degrees": 280,
                "heat_temperature_celsius": 41.1,
                "latitude": 34.0629,
                "longitude": -118.3173,
                "status": "Moving"
              }
            ]
          }
        }
        # המרה ל-JSON
        payload = json.dumps(message)

        # שליחה
        client.publish(TOPIC, payload)
        print(f"Message sent: {payload}")

        # המתנה קטנה לדמות Real-time (שנה לפי הצורך)
        time.sleep(0.1)  # 10 הודעות בשנייה
except KeyboardInterrupt:
    print("Stopped by user")

# שליחת הודעה
client.publish(TOPIC, message)
print(f"Message sent: {message}")

client.disconnect()
