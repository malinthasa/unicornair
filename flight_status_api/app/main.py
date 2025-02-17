import os
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import psycopg2
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Function to get database connection
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

class FlightStatus(BaseModel):
    flight_id: int
    status: str
    timestamp: datetime   # Change from str to datetime
    departure_airport: str
    arrival_airport: str
    delay_reason: Optional[str] = None
    delay_duration: Optional[int] = 0


# API endpoint to fetch all flight statuses
@app.get('/flights', response_model=List[FlightStatus])
def get_flights(
    status: Optional[str] = Query(None),
    departure_airport: Optional[str] = Query(None),
    arrival_airport: Optional[str] = Query(None)
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """select f.id,fs.status, fs."timestamp", da.name, aa.name, fs.delay_reason, fs.delay_duration 
                from flight_status fs
                inner join flight f 
                on f.id = fs.flight_id
                inner join airport da 
                on da.id = f.departure_airport
                inner join airport aa
                on aa.id = f.arrival_airport;
            """
    params = []

    if status:
        query += " AND status = %s"
        params.append(status)
    if departure_airport:
        query += " AND departure_airport = %s"
        params.append(departure_airport)
    if arrival_airport:
        query += " AND arrival_airport = %s"
        params.append(arrival_airport)

    cursor.execute(query, params)
    flights = cursor.fetchall()
    conn.close()

    return [
        FlightStatus(
            flight_id=row[0],
            status=row[1],
            timestamp=row[2],
            departure_airport=row[3],
            arrival_airport=row[4],
            delay_reason=row[5],
            delay_duration=row[6]
        ) for row in flights
    ]

# API endpoint to fetch specific flight details
@app.get('/flights/{flight_id}', response_model=FlightStatus)
def get_flight_by_id(flight_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT flight_id, status, timestamp, departure_airport, arrival_airport, delay_reason, delay_duration FROM flight_status WHERE flight_id = %s", (flight_id,))
    flight = cursor.fetchone()
    conn.close()

    if flight:
        return FlightStatus(
            flight_id=flight[0],
            status=flight[1],
            timestamp=flight[2],
            departure_airport=flight[3],
            arrival_airport=flight[4],
            delay_reason=flight[5],
            delay_duration=flight[6]
        )
    else:
        raise HTTPException(status_code=404, detail="Flight not found")
    
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
