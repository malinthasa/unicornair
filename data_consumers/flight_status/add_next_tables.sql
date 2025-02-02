-- SQLite
-- 📋 SQL Script to Design Notification System Tables

-- 1️⃣ Passengers Table
CREATE TABLE passenger (
    passenger_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- 2️⃣ Bookings Table (Linking Passengers to Flights)
CREATE TABLE booking (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_id INTEGER NOT NULL,
    flight_id TEXT NOT NULL,
    FOREIGN KEY (passenger_id) REFERENCES passenger(passenger_id),
    FOREIGN KEY (flight_id) REFERENCES journey(flight_id)
);

-- 3️⃣ Notifications Table (Track Sent Notifications)
CREATE TABLE notification (
    notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id INTEGER NOT NULL,
    flight_id TEXT NOT NULL,
    status TEXT CHECK (status IN ('ON_TIME', 'DELAYED', 'CANCELLED', 'DEPARTED', 'ARRIVED')) NOT NULL,
    message TEXT NOT NULL,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id),
    FOREIGN KEY (flight_id) REFERENCES journey(flight_id)
);

-- 🔑 Indexes for Performance
CREATE INDEX idx_booking_flight_id ON booking (flight_id);
CREATE INDEX idx_notification_flight_id ON notification (flight_id);

-- 🚀 Sample Data Insertion for Testing

-- Sample Passengers
INSERT INTO passenger (name, email) VALUES
('Alice Smith', 'alice@example.com'),
('Bob Johnson', 'bob@example.com'),
('Charlie Brown', 'charlie@example.com');

-- Sample Bookings (Assuming flights UAF001, UAF002, UAF003 exist)
INSERT INTO booking (passenger_id, flight_id) VALUES
(1, 'UAF001'),
(2, 'UAF002'),
(3, 'UAF003');
