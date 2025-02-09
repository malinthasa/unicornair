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
processed_files = set()

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
    logging.info("✅ Got connection from DB")
    return connection


# Process CSV file and insert data into the database
def process_csv_file(file_path):
    conn = get_db_conn()
    cursor = conn.cursor()

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursor.execute('SELECT id FROM flight_status WHERE flight_id = %s', (row['flight_number'],))
        
            result = cursor.fetchone()

            if result:
                cursor.execute('''
                    UPDATE flight_status
                    SET status = %s,
                        timestamp = %s,
                        departure_airport = %s,
                        arrival_airport = %s,
                        delay_reason = %s,
                        delay_duration = %s
                    WHERE flight_id = %s
                ''', (
                    row['flight_status'],
                    row['reported_at'],
                    row['departure_airport'],
                    row['arrival_airport'],
                    row['delay_reason'],
                    int(row['delay_duration']) if row['delay_duration'] else 0,
                    row['flight_number']
                ))
            else:
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

    conn.commit()
    conn.close()


def watch_directory():
    for filename in os.listdir(WATCH_DIRECTORY):
        if filename.endswith(".csv") and filename not in processed_files:
            file_path = os.path.join(WATCH_DIRECTORY, filename)
            process_csv_file(file_path)
            processed_files.add(filename)

if __name__ == "__main__":
    time.sleep(60)
    interval_seconds = 600
    while True:
        time.sleep(interval_seconds)
        if not os.path.exists(WATCH_DIRECTORY):
            os.makedirs(WATCH_DIRECTORY)
            logging.info(f"Directory {WATCH_DIRECTORY} created.")
        else:
            logging.info(f"Directory {WATCH_DIRECTORY} already exists.")

        watch_directory()
