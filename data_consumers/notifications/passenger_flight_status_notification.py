import sqlite3
import requests
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import time

# Database configuration
DB_PATH = '../../data/operations_db/flight.db'

# Flight Status API URL
API_URL = 'http://localhost:5000/flights'

# Email configuration (using SMTP)
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USER = 'your_email@example.com'
SMTP_PASSWORD = 'your_password'

# Function to send email notifications
def send_email(recipient, subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = recipient

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
        print(f"Email sent to {recipient}")

# Function to get database connection
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Function to fetch bookings with passenger emails
def get_bookings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.booking_id, b.flight_id, p.email
        FROM booking b
        JOIN passenger p ON b.passenger_id = p.passenger_id
    """)
    bookings = cursor.fetchall()
    conn.close()
    return bookings

# Function to track notifications to prevent duplicates
def has_notification_been_sent(booking_id, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM notification
        WHERE booking_id = ? AND status = ?
    """, (booking_id, status))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to log sent notifications
def log_notification(booking_id, flight_id, status, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notification (booking_id, flight_id, status, message)
        VALUES (?, ?, ?, ?)
    """, (booking_id, flight_id, status, message))
    conn.commit()
    conn.close()

# Notification service loop
def notification_service():
    while True:
        bookings = get_bookings()

        for booking in bookings:
            flight_id = booking['flight_id']
            email = booking['email']

            # Fetch flight status from API
            response = requests.get(f"{API_URL}/{flight_id}")
            if response.status_code == 200:
                flight_status = response.json()
                status = flight_status['status']

                # Send notification if it's a new status
                if not has_notification_been_sent(booking['booking_id'], status):
                    subject = f"Flight {flight_id} Status Update: {status}"
                    message = f"Dear Passenger,\n\nYour flight {flight_id} is now {status}.\n\nDetails:\nDeparture: {flight_status['departure_airport']}\nArrival: {flight_status['arrival_airport']}\nStatus: {status}\n\nThank you for choosing UnicornAir."
                    # send_email(email, subject, message)
                    log_notification(booking['booking_id'], flight_id, status, message)

        # Poll every 5 minutes
        time.sleep(300)

if __name__ == '__main__':
    notification_service()
