import os
import psycopg2
from datetime import datetime, timedelta
import random
import time
import pandas as pd
import math

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


def get_db_conn():
    conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
    return conn


current_time = datetime.now().replace(second=0, microsecond=0)

def get_different_airport(start_airport, airports_lists):
    while True:
        random_index_2 = random.randint(0, len(airports_lists) - 1)
        airport_2 = airports_lists[random_index_2]
        if start_airport != airport_2:
            return airport_2


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two GPS coordinates using the Haversine formula.
    """
    R = 6371  # Earth's radius in km

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c  # Distance in km

def flight_time(lat1, lon1, lat2, lon2, speed_kmh=900):
    """
    Estimate the flight time in hours given the coordinates of two airports.
    """
    distance = haversine(lat1, lon1, lat2, lon2)
    time_hours = distance / speed_kmh  # Time in hours
    time_minutes = time_hours * 60  # Convert to minutes
    return distance, round(time_hours, 2), round(time_minutes)

def check_trip_possible(airport_1, airport_2):
    _, _, time_minutes = flight_time(airport_1['location_lat'], airport_1['location_lon'], airport_2['location_lat'], airport_2['location_lon'])

    total_route_time = time_minutes * 2  + 180

    if total_route_time < 1440:
        return True
    else:    
        return False

def generate_possible_journeys(active_planes_lists, airports_lists):
    possible_journeys = []

    for plane in active_planes_lists:
        trip_plan_attempts = 0
        plane_id = plane['plane_id']
        plane_capacity = plane['capacity']

        random_index = random.randint(0, len(airports_lists) - 1)
        airport_1 = airports_lists[random_index]
        airport_2 = get_different_airport(airport_1, airports_lists)

        while trip_plan_attempts < 10:
            trip_possible = check_trip_possible(airport_1, airport_2)

            if trip_possible:
                break
            else:
                trip_plan_attempts += 1
                airport_2 = get_different_airport(airport_1, airports_lists)

        distance, time_hours, time_minutes = flight_time(airport_1['location_lat'], airport_1['location_lon'], airport_2['location_lat'], airport_2['location_lon'])


        possible_journeys.append({
                'plane_id': plane_id,
                'plane_capacity': plane_capacity,
                'airport_1': airport_1,
                'airport_2': airport_2,
                'distance': distance,
                'time_minutes': time_minutes,
        })
    return possible_journeys

def generate_flight_plan(possible_journeys):

    planned_journeys = []

    for journey in possible_journeys:
    
        # journey 1
        plane_id = journey['plane_id']
        capacity = journey['plane_capacity'] - 10
        departure_airport = journey['airport_1']['id']
        arrival_airport = journey['airport_2']['id']
        one_way_time = journey['time_minutes']
        journey_1_departure = current_time + timedelta(minutes=random.randint(60, 720))
        journey_1_arrival = journey_1_departure + timedelta(minutes=one_way_time)
        journey_1_refuel = journey_1_arrival + timedelta(minutes=180)

        planned_journeys.append({
            'plane_id': plane_id,
            'capacity': capacity,
            'departure_airport': departure_airport,
            'arrival_airport': arrival_airport,
            'one_way_time': one_way_time,
            'scheduled_departure': journey_1_departure,
            'scheduled_arrival': journey_1_arrival,
        })           

        # journey 2
        planned_journeys.append({
            'plane_id': plane_id,
            'capacity': capacity,
            'departure_airport': arrival_airport,
            'arrival_airport': departure_airport,
            'one_way_time': one_way_time,
            'scheduled_departure': journey_1_refuel,
            'scheduled_arrival': journey_1_refuel + timedelta(minutes=one_way_time),
        })
    return planned_journeys  


def generate_db_query(planned_journeys):

    query = "INSERT INTO flight (plane_id, departure_airport, arrival_airport, journey_time, scheduled_departure, scheduled_arrival) VALUES"

    for journey in planned_journeys:
        query += (f"\n({journey['plane_id']}, {journey['departure_airport']}, {journey['arrival_airport']}, {journey['one_way_time']}, '{journey['scheduled_departure']}', '{journey['scheduled_arrival']}'),")

    return query[:-1] + ";"

def write_to_db(query):
    db_conn_1 = get_db_conn()
    cur = db_conn_1.cursor()
    cur.execute(query)
    db_conn_1.commit()
    cur.close()
    db_conn_1.close()

if __name__ == "__main__":
    time.sleep(60)
    db_conn_1 = get_db_conn()
    active_planes = pd.read_sql("SELECT * FROM plane WHERE status = 'Active'", db_conn_1)
    active_planes_lists = active_planes.to_dict('records')

    airports = pd.read_sql("SELECT * FROM operational_airport", db_conn_1)
    airports_lists = airports.to_dict('records')

    possible_journeys = generate_possible_journeys(active_planes_lists, airports_lists)
    planned_flights = generate_flight_plan(possible_journeys)

    db_query = generate_db_query(planned_flights)

    write_to_db(db_query)
    print(f"✅ Inserted journeys into the PostgreSQL database.")
