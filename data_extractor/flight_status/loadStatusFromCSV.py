import sqlite3
import csv
import os
import time

# SQLite DB setup
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
WATCH_DIRECTORY = os.path.join(ROOT_DIR, '../../data/flight_delay')

ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DB_DIRECTORY = os.path.join(ROOT_DIRECTORY, '../../data/operations_db')
DB_FILE = os.path.join(DB_DIRECTORY, "flight.db")


# Initialize the database
def initialize_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flight_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_id TEXT,
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

# Process CSV file and insert data into the database
def process_csv_file(file_path):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute('''
                INSERT INTO flight_status (flight_id, status, timestamp, departure_airport, arrival_airport, delay_reason, delay_duration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                row['flight_id'],
                row['status'],
                row['timestamp'],
                row['departure_airport'],
                row['arrival_airport'],
                row['delay_reason'],
                int(row['delay_duration']) if row['delay_duration'] else 0
            ))

    conn.commit()
    conn.close()
    print(f"Processed and inserted data from {file_path}")

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
    
    initialize_database()
    watch_directory()
