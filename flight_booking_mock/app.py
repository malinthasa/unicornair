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

def insert_bookings():
    insert_query = """
    INSERT INTO booking (passenger_id, flight_id)
    SELECT p.passenger_id, j.flight_id
    FROM journey j
    JOIN passenger p ON p.email = 'malinthasa@gmail.com'
    WHERE NOT EXISTS (
        SELECT 1
        FROM booking b
        WHERE b.passenger_id = p.passenger_id AND b.flight_id = j.flight_id
    );
    """
    
    cursor.execute(insert_query)
    conn.commit()

if __name__ == "__main__":
    time.sleep(90)
    insert_bookings()
    conn.close()

