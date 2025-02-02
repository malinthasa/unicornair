import os
import csv
import time
from kafka import KafkaProducer
import json

# Kafka setup
KAFKA_BROKER = 'localhost:9092'  # Change this if using a remote broker
TOPIC = 'flight_status_updates'

# Directory to watch
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WATCH_DIRECTORY = os.path.join(ROOT_DIR, '../../data/flight_status')

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Process CSV file and send data to Kafka
def process_csv_file(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Prepare the message
            message = {
                'flight_id': row['flight_number'],
                'status': row['flight_status'],
                'timestamp': row['reported_at'],
                'departure_airport': row['departure_airport'],
                'arrival_airport': row['arrival_airport'],
                'delay_code': row['delay_code'],
                'delay_reason': row['delay_reason'],
                'delay_duration': int(row['delay_duration']) if row['delay_duration'] else 0
            }

            # Send message to Kafka
            producer.send(TOPIC, value=message)
            print(f"Sent to Kafka: {message}")

    print(f"Processed and sent data from {file_path}")

# Watch for new CSV files and process them
def watch_directory(interval_seconds=10):
    processed_files = set()

    while True:
        for filename in os.listdir(WATCH_DIRECTORY):
            if filename.endswith(".csv") and filename not in processed_files:
                file_path = os.path.join(WATCH_DIRECTORY, filename)
                process_csv_file(file_path)
                processed_files.add(filename)
                print(f"Processed file: {filename}")

        time.sleep(interval_seconds)

if __name__ == "__main__":
    if not os.path.exists(WATCH_DIRECTORY):
        os.makedirs(WATCH_DIRECTORY)

    watch_directory()
