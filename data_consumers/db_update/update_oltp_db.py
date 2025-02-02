import sqlite3
from kafka import KafkaConsumer
import json
import os

# Kafka Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'flight_status_updates'

# SQLite Database Configuration
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data/operations_db/flight.db')

# Initialize the OLTP Database
def initialize_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flight_status (
            flight_id TEXT PRIMARY KEY,
            status TEXT,
            timestamp TEXT,
            departure_airport TEXT,
            arrival_airport TEXT,
            delay_reason TEXT,
            delay_duration INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Upsert Logic: Insert or Update Flight Status
def upsert_flight_status(flight_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flight_status (flight_id, status, timestamp, departure_airport, arrival_airport, delay_reason, delay_duration)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(flight_id) DO UPDATE SET
            status=excluded.status,
            timestamp=excluded.timestamp,
            departure_airport=excluded.departure_airport,
            arrival_airport=excluded.arrival_airport,
            delay_reason=excluded.delay_reason,
            delay_duration=excluded.delay_duration
    ''', (
        flight_data['flight_id'],
        flight_data['status'],
        flight_data['timestamp'],
        flight_data['departure_airport'],
        flight_data['arrival_airport'],
        flight_data.get('delay_reason', ''),
        flight_data.get('delay_duration', 0)
    ))
    conn.commit()
    conn.close()

# Kafka Consumer Setup
def consume_and_update():
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
        print(f"📥 Received Update: {flight_data}")
        upsert_flight_status(flight_data)
        print(f"✅ Database Updated for Flight ID: {flight_data['flight_id']}")

if __name__ == '__main__':
    initialize_db()
    consume_and_update()
