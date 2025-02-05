import psycopg2
from datetime import datetime, timedelta
import random
import time

DB_HOST = 'db'
DB_PORT = '5432'
DB_NAME = 'operations'
DB_USER = 'unicorn_admin'
DB_PASSWORD = 'unicorn_password'

max_retries = 10
retry_delay = 5


conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

cursor = conn.cursor()

# Fetch active planes
cursor.execute("SELECT plane_id FROM plane WHERE status = 'Active'")
active_planes = [row[0] for row in cursor.fetchall()]

# Fetch German airports
cursor.execute("SELECT airport_code FROM airport WHERE country = 'Germany'")
german_airports = [row[0] for row in cursor.fetchall()]

# Fetch non-German airports
cursor.execute("SELECT airport_code FROM airport WHERE country != 'Germany'")
non_german_airports = [row[0] for row in cursor.fetchall()]


def flush_existing_journeys():
    cursor.execute("DELETE FROM journey")
    conn.commit()


# Function to generate flight schedules
def generate_flight_schedules():
    journeys = []
    flight_counter = 1
    today = datetime.now().date()

    for plane_id in active_planes:
        current_time = datetime.combine(today, datetime.min.time())  # Start from midnight

        while current_time < datetime.combine(today, datetime.max.time()):
            departure_airport = random.choice(german_airports)
            arrival_airport = random.choice([airport for airport in non_german_airports if airport != departure_airport])

            scheduled_departure = current_time
            scheduled_arrival = scheduled_departure + timedelta(hours=2)  # 2-hour flight duration

            # Ensure the arrival time is within today
            if scheduled_arrival.date() != today:
                break

            flight_id = f"UAF{flight_counter:03d}"
            journeys.append((flight_id, plane_id, departure_airport, arrival_airport, scheduled_departure, scheduled_arrival, 'Scheduled'))

            # Increment counters and apply 3-hour ground time
            flight_counter += 1
            current_time = scheduled_arrival + timedelta(hours=3)

    return journeys

# Insert journeys into the PostgreSQL database
def insert_journeys(journeys):
    insert_query = """
    INSERT INTO journey (flight_id, plane_id, departure_airport, arrival_airport, scheduled_departure, scheduled_arrival, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, journeys)
    conn.commit()

if __name__ == "__main__":
    time.sleep(10)
    flush_existing_journeys()
    journeys = generate_flight_schedules()
    insert_journeys(journeys)
    print(f"✅ Inserted {len(journeys)} journeys into the PostgreSQL database.")
