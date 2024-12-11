import time
import paho.mqtt.client as mqtt
from kafka import KafkaProducer
import json

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # המרה לפורמט UTF-8
)

# הגדרות MQTT
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "test/mqtt"

# פונקציה שתופעל כאשר מתקבלת הודעה
def on_message(client, userdata, msg):
    try:
        # המרת ה-Payload לטקסט
        message = msg.payload.decode('utf-8')
        print(f"Received message: {message} from topic: {msg.topic}")

        # המרה מ-string ל-JSON (dict)
        message_data = json.loads(message)
        print(f"Message as dict: {message_data}")

        # שליחה ל-Kafka לפי סוג ההודעה
        producer.send('all.messages', json.dumps(message_data).encode('utf-8'))

        if message_data.get('type') == 'thermal':
            producer.send('thermal', json.dumps(message_data).encode('utf-8'))
        elif message_data.get('type') == 'radar':
            producer.send('radar', json.dumps(message_data).encode('utf-8'))
        elif message_data.get('type') == 'sonar':
            producer.send('sonar', json.dumps(message_data).encode('utf-8'))
        elif message_data.get('type') == 'weather':
            producer.send('weather', json.dumps(message_data).encode('utf-8'))

    except json.JSONDecodeError:
        print("Received message is not a valid JSON.")
    except Exception as e:
        print(f"Error processing message: {e}")

# פונקציה שמטפלת באירוע התחברות
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe(TOPIC)  # הרשמה לנושא
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Failed to connect with code {rc}")

# יצירת לקוח MQTT
client = mqtt.Client()

# הגדרת callback
client.on_connect = on_connect
client.on_message = on_message

# התחברות ל-broker
client.connect(BROKER, PORT, 60)

# הפעלת לולאת MQTT בצורה אסינכרונית (לא חוסם)
client.loop_start()

try:
    while True:
        time.sleep(1)  # שינה בין כל איטרציה של הלולאה כדי לא לתפוס משאבים מיותרים
except KeyboardInterrupt:
    print("Shutting down...")
    client.loop_stop()  # עצירת הלולאה של MQTT באופן מסודר
