from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'all.messages',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    group_id='emails',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    msg = message.value
    # inserted_email = insert_email(msg)
    print(f"Stored email message: {msg}")
    # consumer.commit()