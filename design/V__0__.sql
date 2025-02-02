CREATE TABLE plane (
    plane_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    registration_number TEXT UNIQUE NOT NULL,
    status TEXT CHECK (status IN ('Active', 'Under Maintenance', 'Retired')) NOT NULL
);

CREATE TABLE airport (
    airport_code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    timezone TEXT NOT NULL
);

CREATE TABLE journey (
    flight_id TEXT PRIMARY KEY,
    plane_id INTEGER NOT NULL,
    departure_airport TEXT NOT NULL,
    arrival_airport TEXT NOT NULL,
    scheduled_departure DATETIME NOT NULL,
    scheduled_arrival DATETIME NOT NULL,
    status TEXT CHECK (status IN ('Scheduled', 'On Time', 'Delayed', 'Cancelled')) NOT NULL,
    FOREIGN KEY (plane_id) REFERENCES plane(plane_id),
    FOREIGN KEY (departure_airport) REFERENCES airport(airport_code),
    FOREIGN KEY (arrival_airport) REFERENCES airport(airport_code)
);

CREATE TABLE flight_status (
    status_id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT CHECK (status IN ('On Time', 'Delayed', 'Departed', 'Arrived', 'Cancelled')) NOT NULL,
    delay_reason TEXT,
    delay_duration INTEGER DEFAULT 0,
    FOREIGN KEY (flight_id) REFERENCES journey(flight_id)
);

CREATE INDEX idx_journey_departure ON journey (departure_airport);
CREATE INDEX idx_journey_arrival ON journey (arrival_airport);
CREATE INDEX idx_flight_status_flight_id ON flight_status (flight_id);
