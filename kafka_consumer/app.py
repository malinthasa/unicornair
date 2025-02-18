import sqlite3
from kafka import KafkaConsumer
import json
import os

# Kafka Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'engine_temperature_data'


# Kafka Consumer Setup
def consume():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='oltp_db_updater_group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print("✅ Listening for flight status updates...")

    for message in consumer:
        flight_data = message.value
        print(flight_data)

if __name__ == '__main__':
    consume()
