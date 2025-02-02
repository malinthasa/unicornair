from flask import Flask, jsonify, request
import sqlite3
import time
import os

app = Flask(__name__)

ROOT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DB_DIRECTORY = os.path.join(ROOT_DIRECTORY, '../../data/operations_db')
DB_FILE = os.path.join(DB_DIRECTORY, "unicornair_flight_status.db")

# Simulated delay to mimic legacy system (in seconds)
SIMULATED_DELAY = 5

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# API endpoint to fetch all flight statuses
@app.route('/flights', methods=['GET'])
def get_flights():
    # Simulate delay
    time.sleep(SIMULATED_DELAY)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Optional filters
    status = request.args.get('status')
    departure_airport = request.args.get('departure_airport')
    arrival_airport = request.args.get('arrival_airport')

    query = "SELECT * FROM flight_status WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)
    if departure_airport:
        query += " AND departure_airport = ?"
        params.append(departure_airport)
    if arrival_airport:
        query += " AND arrival_airport = ?"
        params.append(arrival_airport)

    cursor.execute(query, params)
    flights = cursor.fetchall()
    conn.close()

    return jsonify([dict(flight) for flight in flights])

# API endpoint to fetch specific flight details
@app.route('/flights/<flight_id>', methods=['GET'])
def get_flight_by_id(flight_id):
    # Simulate delay
    time.sleep(SIMULATED_DELAY)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flight_status WHERE flight_id = ?", (flight_id,))
    flight = cursor.fetchone()
    conn.close()

    if flight:
        return jsonify(dict(flight))
    else:
        return jsonify({"error": "Flight not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
