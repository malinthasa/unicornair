import random
import time
from kafka import KafkaProducer
import json
from datetime import datetime

# Kafka setup
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'engine_temperature_data'

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Aircraft and Engine Details
aircrafts = [('A320-NEO-XY123', 'AA101'),
              ('A320-NEO-XY124', 'AA102'),
                ('A320-NEO-XY125', 'AA103'),
                  ('A320-NEO-XY126', 'AA104'),
                    ('A320-NEO-XY127', 'AA105')]

engine_ids = ["ENG1", "ENG2"]

# Simulated Normal Temperature Ranges
NORMAL_TEMP_RANGE = (850, 1000)  # Safe operational range in °C
ANOMALY_PROBABILITY = 0.05  # 5% chance of an anomaly

def generate_engine_temperature(aircraft_id, flight_number):
    """Generates a realistic temperature reading with natural fluctuations."""
    base_temp = random.uniform(*NORMAL_TEMP_RANGE)
    
    # Introduce occasional anomalies (spikes beyond normal range)
    if random.random() < ANOMALY_PROBABILITY:
        base_temp += random.uniform(50, 200)  # Anomalous spike

    status = "NORMAL"
    if base_temp > 1050:
        status = "WARNING"
    if base_temp > 1150:
        status = "CRITICAL"

    return {
        "temperature_celsius": round(base_temp, 2),
        "timestamp": datetime.utcnow().isoformat(),
        "aircraft_id": aircraft_id,
        "flight_number": flight_number,
        "altitude_ft": random.randint(30000, 40000),
        "status": status
    }


if __name__ == "__main__":
    while True:
        time.sleep(5)
        selected_aircraft = random.choice(aircrafts)
        payload = generate_engine_temperature(selected_aircraft[0], selected_aircraft[1])
        producer.send(TOPIC, payload)
