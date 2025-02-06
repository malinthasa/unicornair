import psycopg2
import csv
import os
import time
import logging
import sys

DB_HOST = 'db'
DB_PORT = '5432'
DB_NAME = 'operations'
DB_USER = 'unicorn_admin'
DB_PASSWORD = 'unicorn_password'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

# Directory inside the Docker volume
WATCH_DIRECTORY = '/shared_data'

def get_db_conn():
    connection = None
    try:
            connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            logging.info("✅ Connected to PostgreSQL")
    except psycopg2.OperationalError as e:
        logging.error("Error while getting the DB connection")
    return connection

# Initialize the database
def initialize_database():
    logging.info("Initializing database")
    conn = get_db_conn()
    cursor = conn.cursor()
    
    cursor.execute('''
        DROP TABLE IF EXISTS flight_status;
        CREATE TABLE flight_status (
            id SERIAL PRIMARY KEY,
            flight_id TEXT,
            status TEXT,
            timestamp TIMESTAMP,
            departure_airport TEXT,
            arrival_airport TEXT,
            delay_reason TEXT,
            delay_duration INTEGER
        )
    ''')

    conn.commit()
    conn.close()
    logging.info("✅ Database initialized")

# Process CSV file and insert data into the database
def process_csv_file(file_path):
    conn = get_db_conn()
    cursor = conn.cursor()

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            logging.info(f"Processing row: {row}")
            cursor.execute('''
                INSERT INTO flight_status (flight_id, status, timestamp, departure_airport, arrival_airport, delay_reason, delay_duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', (
                row['flight_number'],
                row['flight_status'],
                row['reported_at'],
                row['departure_airport'],
                row['arrival_airport'],
                row['delay_reason'],
                int(row['delay_duration']) if row['delay_duration'] else 0
            ))

# {'message_id': 'efc5f36f-9780-4b06-92ff-b03b5fbd0428',
#  'flight_number': 'UAF082',
#  'departure_airport': 'FDH',
#  'arrival_airport': 'TPE',
#  'scheduled_departure': '2025-02-06 05:00:00',
#  'scheduled_arrival': '2025-02-06 07:00:00',
#  'flight_status': 'ARRIVED', 'delay_code': '00',
#  'delay_reason': '',
#  'delay_duration': '0',
#  'reported_by': 'Ops Staff',
#  'reported_at': '2025-02-06T20:42:02.735557',
#  'remarks': 'N/A'}

    conn.commit()
    conn.close()
    print(f"Processed and inserted data from {file_path}")

# Watch for new CSV files and process them
def watch_directory(interval_seconds=10):
    logging.info(f"Watching directory {WATCH_DIRECTORY}")
    logging.info(f"Files found {os.listdir(WATCH_DIRECTORY)}")
    processed_files = set()

    while True:
        for filename in os.listdir(WATCH_DIRECTORY):
            # logging.info(f"Found file: {filename}")
            if filename.endswith(".csv") and filename not in processed_files:
                file_path = os.path.join(WATCH_DIRECTORY, filename)
                process_csv_file(file_path)
                processed_files.add(filename)
                # print(f"Processed file: {filename}")
        logging.info(f"Sleeping for {interval_seconds}")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    time.sleep(60)
    logging.info("Starting Data reading")
    if not os.path.exists(WATCH_DIRECTORY):
        os.makedirs(WATCH_DIRECTORY)
    else:
        logging.info(f"Directory {WATCH_DIRECTORY} already exists.")

    initialize_database()
    watch_directory()
