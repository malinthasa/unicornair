# Description: This script generates flight status data for German airports and writes them to CSV files.

import os
import psycopg2
import random
from datetime import datetime
import time
import pytz
import logging
import sys
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


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


def initiate_all_flights():
    conn = get_db_conn()
    cursor = conn.cursor()
    scheduled_flight_update = """INSERT INTO flight_status (flight_id, status, timestamp)
                                 SELECT id, 'Ontime', NOW()
                                 FROM flight"""
    cursor.execute(scheduled_flight_update)
    conn.commit()
    conn.close()

def get_flights_by_airport():
    conn = get_db_conn()

    all_flights_query = """
                        SELECT fs.flight_id, fs.status, f.departure_airport, f.scheduled_departure 
                        FROM flight_status fs 
                        INNER JOIN flight f on f.id=fs.flight_id;
                        """
    all_flights = pd.read_sql(all_flights_query, conn)
    airport_flight_groups = all_flights.groupby("departure_airport")


def make_delayed_flight():
    conn = get_db_conn()
    all_flights_query = """
                    SELECT fs.flight_id, fs.status, fs.timestamp, fs.delay_reason, fs.delay_duration, f.scheduled_departure, da.iata_code as departure_airport, aa.iata_code as arrival_airport 
                    FROM flight_status fs 
                    INNER JOIN flight f on f.id=fs.flight_id
                    INNER JOIN airport da on da.id=f.departure_airport
                    INNER JOIN airport aa on aa.id=f.arrival_airport;
                    """

    all_flights = pd.read_sql(all_flights_query, conn)
    on_time_flights = list(all_flights[all_flights['status'] == 'Ontime']['flight_id'])
    conn.close()

    DELAY_REASONS = ["Weather", "Technical Issue", "Air Traffic", "Crew Unavailability"]
    DELAY_TIMES = [30, 45, 60, 75, 90, 120, 150, 180]

    selected_flight = random.choice(on_time_flights)

    delayed_reason = random.choice(DELAY_REASONS)
    delayed_time = random.choice(DELAY_TIMES)

    all_flights.loc[all_flights['flight_id']==selected_flight, ['status', 'delay_duration', 'delay_reason']]=['Delayed', delayed_time, delayed_reason]

    return all_flights

def upload_to_airline(all_flight_status):

    DATA_DIRECTORY = "/shared_data"

    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)

    airport_flight_groups = all_flight_status.groupby("departure_airport")

    for  airport, flight_group in airport_flight_groups:
        cet_timezone = pytz.timezone('CET')
        timestamp_cet = datetime.now(cet_timezone).strftime("%Y%m%d_%H%M%S")
        csv_file_name = f"{DATA_DIRECTORY}/flight_status_{airport}_{timestamp_cet}.csv"
        # print(flight_group.columns)
        flight_group.to_csv(csv_file_name, index=False)

if __name__ == "__main__":
    time.sleep(60)
    initiate_all_flights()
    while True:
        time.sleep(60)
        manipulated_flight_status_df = make_delayed_flight()
        upload_to_airline(manipulated_flight_status_df)
        print("✅ Uploaded to airline")
