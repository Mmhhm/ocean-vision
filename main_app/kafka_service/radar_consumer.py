import json
from kafka import KafkaConsumer, KafkaProducer

consumer = KafkaConsumer(
    'radar',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='emails',
    enable_auto_commit=False,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

for message in consumer:
    # producer.send("messages.all", value=message).get(timeout=5)
    danger_message = message.value
    # decoded_message = danger_message['sentences']
    for sentence in danger_message:
        # if 'explos' in sentence:
        #     print(f"Stored suspicious email: {danger_message}")
        #     producer.send('messages.explosive', value=sentence)
        print(f'explos message {sentence} sent')

        # if 'hostage' in sentence:
        #     print(f"Stored suspicious email: {danger_message}")
        #     producer.send('messages.hostage', value=sentence)
        print(f'hostage message {sentence} sent')

        # print(f'Email {sentence} is  sent!')
        # consumer.commit()

