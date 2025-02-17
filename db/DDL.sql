

DROP TABLE IF EXISTS passenger;
DROP TABLE IF EXISTS booking;
DROP TABLE IF EXISTS notification;
DROP TABLE IF EXISTS operational_airport;
DROP TABLE IF EXISTS flight;

CREATE TABLE plane (
    plane_id SERIAL PRIMARY KEY,
    model VARCHAR(255) NOT NULL,
    manufacturer VARCHAR(255) NOT NULL,
    capacity INTEGER NOT NULL,
    registration_number VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Active', 'Under Maintenance', 'Retired')) NOT NULL
);

CREATE TABLE airport (
    id SERIAL PRIMARY KEY,
    ident VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    elevation FLOAT NULL,
    continent VARCHAR(10) NOT NULL,
    country_code CHAR(2) NOT NULL,
    region_code VARCHAR(10) NOT NULL,
    city VARCHAR(100) NOT NULL,
    gps_code VARCHAR(20) NULL,
    iata_code VARCHAR(10) NULL UNIQUE,
    location_lat DECIMAL(9,6) NOT NULL,
    location_lon DECIMAL(9,6) NOT NULL
);

CREATE TABLE operational_airport (
    id SERIAL PRIMARY KEY,
    ident VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    elevation FLOAT NULL,
    continent VARCHAR(10) NOT NULL,
    country_code CHAR(2) NOT NULL,
    region_code VARCHAR(10) NOT NULL,
    city VARCHAR(100) NOT NULL,
    gps_code VARCHAR(20) NULL,
    iata_code VARCHAR(10) NULL UNIQUE,
    location_lat DECIMAL(9,6) NOT NULL,
    location_lon DECIMAL(9,6) NOT NULL
);

CREATE TABLE flight (
    id SERIAL PRIMARY KEY,
    plane_id INTEGER NOT NULL,
    departure_airport INT NOT NULL,
    arrival_airport INT NOT NULL,
    journey_time INT NOT NULL,
    scheduled_departure TIMESTAMP NOT NULL,
    scheduled_arrival TIMESTAMP NOT NULL,
    FOREIGN KEY (plane_id) REFERENCES plane(plane_id) ON DELETE CASCADE,
    FOREIGN KEY (departure_airport) REFERENCES operational_airport(id) ON DELETE CASCADE,
    FOREIGN KEY (arrival_airport) REFERENCES operational_airport(id) ON DELETE CASCADE
);

 CREATE TABLE flight_status (
    id SERIAL PRIMARY KEY,
    flight_id INT NOT NULL,
    status TEXT,
    timestamp TIMESTAMP,
    delay_reason TEXT,
    delay_duration INTEGER,
    FOREIGN KEY (flight_id) REFERENCES flight(id) ON DELETE CASCADE
);

ALTER TABLE flight_status
ADD CONSTRAINT unique_flight_id UNIQUE (flight_id);


CREATE TABLE passenger (
    passenger_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    passport_number TEXT UNIQUE NOT NULL,
    phone_number VARCHAR(30),
    address VARCHAR(100),
    country VARCHAR(100),
    city VARCHAR(100),
    postal_code VARCHAR(50)
);

CREATE TABLE booking (
    booking_id SERIAL PRIMARY KEY,
    passenger_id INTEGER NOT NULL,
    flight_id INT NOT NULL,
    FOREIGN KEY (passenger_id) REFERENCES passenger(passenger_id) ON DELETE CASCADE,
    FOREIGN KEY (flight_id) REFERENCES flight(id) ON DELETE CASCADE
);

CREATE TABLE notification (
    notification_id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL,
    flight_id INT NOT NULL,
    status TEXT CHECK (status IN ('ON_TIME', 'DELAYED', 'CANCELLED', 'DEPARTED', 'ARRIVED')) NOT NULL,
    message TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (flight_id) REFERENCES flight(id) ON DELETE CASCADE
);


