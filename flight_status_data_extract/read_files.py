import psycopg2
import csv
import os
import time
import logging
import sys

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )

# # Directory inside the Docker volume
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
                if row['delay_duration']=='':
                    row['delay_duration']=0
                cursor.execute('SELECT id FROM flight_status WHERE flight_id = %s', (row['flight_id'],))
                result = cursor.fetchone()

                if result:
                    cursor.execute('''
                        UPDATE flight_status
                        SET status = %s,
                            timestamp = %s,
                            delay_reason = %s,
                            delay_duration = %s
                        WHERE flight_id = %s
                    ''', (
                        row['status'],
                        row['timestamp'],
                        row['delay_reason'],
                        row['delay_duration'],
                        row['flight_id']
                    ))

        conn.commit()
        conn.close()


def watch_directory():
        print("✅ Watching directory")
        for filename in os.listdir(WATCH_DIRECTORY):
            if filename.endswith(".csv") and filename not in processed_files:
                file_path = os.path.join(WATCH_DIRECTORY, filename)
                process_csv_file(file_path)
                processed_files.add(filename)

if __name__ == "__main__":
    print("✅ Started watching directory")
    while True:
        time.sleep(300)
        if os.path.exists(WATCH_DIRECTORY):
            print("✅ Directory exists")
            watch_directory()
        else:
            print("❌ Directory does not exist")