

CREATE TABLE plane (
    plane_id SERIAL PRIMARY KEY,
    model VARCHAR(255) NOT NULL,
    manufacturer VARCHAR(255) NOT NULL,
    capacity INTEGER NOT NULL,
    registration_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Active', 'Under Maintenance', 'Retired')) NOT NULL
);

CREATE TABLE airport (
    airport_code VARCHAR(10) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    timezone VARCHAR(50) NOT NULL
);

CREATE TABLE journey (
    flight_id VARCHAR(20) PRIMARY KEY,
    plane_id INTEGER NOT NULL,
    departure_airport VARCHAR(10) NOT NULL,
    arrival_airport VARCHAR(10) NOT NULL,
    scheduled_departure TIMESTAMP NOT NULL,
    scheduled_arrival TIMESTAMP NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Scheduled', 'On Time', 'Delayed', 'Cancelled')) NOT NULL,
    FOREIGN KEY (plane_id) REFERENCES plane(plane_id) ON DELETE CASCADE,
    FOREIGN KEY (departure_airport) REFERENCES airport(airport_code) ON DELETE CASCADE,
    FOREIGN KEY (arrival_airport) REFERENCES airport(airport_code) ON DELETE CASCADE
);

CREATE TABLE flight_status (
    status_id SERIAL PRIMARY KEY,
    flight_id VARCHAR(20) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('On Time', 'Delayed', 'Departed', 'Arrived', 'Cancelled')) NOT NULL,
    delay_reason VARCHAR(255),
    delay_duration INTEGER DEFAULT 0,
    FOREIGN KEY (flight_id) REFERENCES journey(flight_id) ON DELETE CASCADE
);

CREATE INDEX idx_journey_departure ON journey (departure_airport);
CREATE INDEX idx_journey_arrival ON journey (arrival_airport);
CREATE INDEX idx_flight_status_flight_id ON flight_status (flight_id);

