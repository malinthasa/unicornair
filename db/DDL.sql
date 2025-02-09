

DROP TABLE IF EXISTS passenger;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS notification;

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
    id SERIAL PRIMARY KEY,
    flight_id TEXT,
    status TEXT,
    timestamp TIMESTAMP,
    departure_airport TEXT,
    arrival_airport TEXT,
    delay_reason TEXT,
    delay_duration INTEGER,
    FOREIGN KEY (flight_id) REFERENCES journey(flight_id) ON DELETE CASCADE
);

ALTER TABLE flight_status
ADD CONSTRAINT unique_flight_id UNIQUE (flight_id);

CREATE INDEX idx_journey_departure ON journey (departure_airport);
CREATE INDEX idx_journey_arrival ON journey (arrival_airport);
CREATE INDEX idx_flight_status_flight_id ON flight_status (flight_id);

CREATE TABLE passenger (
    passenger_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    passport_number TEXT UNIQUE NOT NULL,
    phone_number VARCHAR(15),
    address VARCHAR(100),
    country VARCHAR(50),
    city VARCHAR(50),
    postal_code VARCHAR(20)
);

CREATE TABLE booking (
    booking_id SERIAL PRIMARY KEY,
    passenger_id INTEGER NOT NULL,
    flight_id VARCHAR(10) NOT NULL,
    FOREIGN KEY (passenger_id) REFERENCES passenger(passenger_id) ON DELETE CASCADE,
    FOREIGN KEY (flight_id) REFERENCES journey(flight_id) ON DELETE CASCADE
);

CREATE TABLE notification (
    notification_id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL,
    flight_id VARCHAR(10) NOT NULL,
    status TEXT CHECK (status IN ('ON_TIME', 'DELAYED', 'CANCELLED', 'DEPARTED', 'ARRIVED')) NOT NULL,
    message TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (flight_id) REFERENCES journey(flight_id) ON DELETE CASCADE
);

CREATE INDEX idx_booking_flight_id ON booking (flight_id);
CREATE INDEX idx_notification_flight_id ON notification (flight_id);
