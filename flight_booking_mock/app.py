import psycopg2
from datetime import datetime, timedelta
import random
import time
import pandas as pd

DB_HOST = 'db'
DB_PORT = '5432'
DB_NAME = 'operations'
DB_USER = 'unicorn_admin'
DB_PASSWORD = 'unicorn_password'


def get_db_conn():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

def get_all_passengers():
    conn = get_db_conn()
    all_passengers = pd.read_sql_query('SELECT passenger_id FROM passenger', conn)
    all_passengers_lists = all_passengers.to_dict('records')
    all_passenger_ids = [passenger['passenger_id'] for passenger in all_passengers_lists]
    conn.close()
    return all_passenger_ids


def select_random_numbers(num_list, count):
    if count > len(num_list):
        raise ValueError("Count exceeds the number of elements in the list.")
    return random.sample(num_list, count)


def get_all_flights():
    conn = get_db_conn()
    all_flights = pd.read_sql_query("""select f.id as flight_id, p.capacity - 10 as available_seats
                                    from flight f 
                                    inner join plane p 
                                    on f.plane_id = p.plane_id""", conn)
    all_flights_lists = all_flights.to_dict('records')
    conn.close()
    return all_flights_lists

# cursor = conn.cursor()

# def insert_bookings():
#     insert_query = """
#     INSERT INTO booking (passenger_id, flight_id)
#     SELECT p.passenger_id, j.flight_id
#     FROM journey j
#     JOIN passenger p ON p.email = 'malinthasa@gmail.com'
#     WHERE NOT EXISTS (
#         SELECT 1
#         FROM booking b
#         WHERE b.passenger_id = p.passenger_id AND b.flight_id = j.flight_id
#     );
#     """
    
#     cursor.execute(insert_query)
#     conn.commit()

if __name__ == "__main__":
    time.sleep(90)
    all_pasengers = get_all_passengers()
    all_flights = get_all_flights()

    conn = get_db_conn()
    cursor = conn.cursor()

    for flight in all_flights:
        seats = flight['available_seats']
        flight_id = flight['flight_id']

        booked_passengers = select_random_numbers(all_pasengers, seats//2)

        query = "INSERT INTO booking (passenger_id, flight_id) VALUES"

        for passenger_id in booked_passengers:
            query += (f"\n({passenger_id}, {flight_id}),")
        
        query = query[:-1] + ";"

        
        cursor.execute(query)

    conn.commit()
    conn.close()
