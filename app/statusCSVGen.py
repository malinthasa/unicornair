import csv
import random
from datetime import datetime
import time
import pytz
import os
import uuid
import psycopg2  # PostgreSQL library

print("****************************************#")

DB_HOST = 'db'
DB_PORT = '5432'
DB_NAME = 'operations'
DB_USER = 'unicorn_admin'
DB_PASSWORD = 'unicorn_password'

# Status options with probabilities
STATUS_OPTIONS = ["ON_TIME"] * 60 + ["DELAYED"] * 20 + ["DEPARTED"] * 15 + ["ARRIVED"] * 4 + ["CANCELLED"] * 1
DELAY_REASONS = ["Weather", "Technical Issue", "Air Traffic", "Crew Unavailability", ""]
IATA_DELAY_CODES = {
        "Weather": "86",
        "Technical Issue": "31",
        "Air Traffic": "93",
        "Crew Unavailability": "64",
        "": "00"
    }

def init_operations():
    max_retries = 10
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        print(f"🔄 Attempt {attempt + 1}/{max_retries}: Connecting to PostgreSQL...")
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("✅ Connected to PostgreSQL")
            break
        except psycopg2.OperationalError as e:
            print(f"⏳ Attempt {attempt + 1}/{max_retries}: Database not ready. Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)

    cursor = conn.cursor()
    

# Function to generate random flight status data
def generate_flight_status(flight):
    message_id = str(uuid.uuid4())
    flight_id, departure_airport, arrival_airport, scheduled_departure, scheduled_arrival = flight
    current_time = datetime.utcnow()

    if current_time < scheduled_departure:
        status = "ON_TIME"
    elif scheduled_departure <= current_time < scheduled_arrival:
        status = random.choices(["DEPARTED", "DELAYED", "ON_TIME"], [70, 20, 10])[0]
    else:
        status = random.choices(["ARRIVED", "DELAYED", "CANCELLED"], [85, 10, 5])[0]

    delay_reason = random.choice(DELAY_REASONS) if status == "DELAYED" else ""
    delay_code = IATA_DELAY_CODES.get(delay_reason, "00")
    delay_duration = random.randint(15, 180) if status == "DELAYED" else 0
    reported_by = random.choice(["AODB", "Ops Staff"])
    reported_at = current_time.isoformat()
    remarks = delay_reason if delay_reason else "N/A"

    return [
        message_id,
        flight_id,
        departure_airport,
        arrival_airport,
        scheduled_departure,
        scheduled_arrival,
        status,
        delay_code,
        delay_reason,
        delay_duration,
        reported_by,
        reported_at,
        remarks
    ]

# Generate a new CSV file for each German airport
def generate_new_csv(cursor):
    cet_timezone = pytz.timezone('CET')
    timestamp_cet = datetime.now(cet_timezone).strftime("%Y%m%d_%H%M%S")

    cursor.execute("SELECT airport_code FROM airport WHERE country = 'Germany'")
    GERMAN_AIRPORTS = [row[0] for row in cursor.fetchall()]

    # Fetch all flights scheduled for today
    cursor.execute("""
        SELECT flight_id, departure_airport, arrival_airport, scheduled_departure, scheduled_arrival
        FROM journey
        WHERE DATE(scheduled_departure) = CURRENT_DATE
    """)
    FLIGHTS = cursor.fetchall()

    # Directory to save CSV files
    # ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # DATA_DIRECTORY = os.path.join(ROOT_DIR, "../../data/flight_status")

    DATA_DIRECTORY = "/shared_data"

    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)


    # Ensure the directory exists
    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)

    for airport_code in GERMAN_AIRPORTS:
        csv_file = os.path.join(DATA_DIRECTORY, f"flight_status_{airport_code}_{timestamp_cet}.csv")

        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "message_id", "flight_number", "departure_airport", "arrival_airport",
                "scheduled_departure", "scheduled_arrival", "flight_status",
                "delay_code", "delay_reason", "delay_duration", "reported_by", "reported_at", "remarks"
            ])

            flights_from_airport = [f for f in FLIGHTS if f[1] == airport_code]

            for flight in random.sample(flights_from_airport, min(5, len(flights_from_airport))):
                flight_data = generate_flight_status(flight)
                writer.writerow(flight_data)
                print(f"New data added to {csv_file}")

# Generate new CSV files periodically with random intervals
def generate_files_periodically():
    while True:
        print("Generating new CSV files...")
        # generate_new_csv()
        time.sleep(random.randint(60, 300))  # Random delay between 1 to 5 minutes

if __name__ == "__main__":
    print("****************************************")
    generate_files_periodically()
