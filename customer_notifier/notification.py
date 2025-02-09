import psycopg2
import requests
import smtplib
from email.mime.text import MIMEText
import time
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

# Database configuration
DB_HOST = 'db'
DB_PORT = '5432'
DB_NAME = 'operations'
DB_USER = 'unicorn_admin'
DB_PASSWORD = 'unicorn_password'

# Flight Status API URL
API_URL = 'http://api:8000/flights'

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

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"Email sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")

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
        WHERE booking_id = %s AND status = %s
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
        VALUES (%s, %s, %s, %s)
    """, (booking_id, flight_id, status, message))
    conn.commit()
    conn.close()

# Notification service loop
def notification_service():
    while True:
        bookings = get_bookings()
        logging.info(f"Found {len(bookings)} bookings")

        for booking in bookings:
            booking_id, flight_id, email = booking
            logging.info(f"Checking for notifications for {email} - Flight {flight_id}")

            # Fetch flight status from API
            try:
                response = requests.get(f"{API_URL}/{flight_id}")
                response.raise_for_status()  # Raise exception for HTTP errors
                flight_status = response.json()
                status = flight_status['status']

                # Send notification if it's a new status
                if not has_notification_been_sent(booking_id, status):
                    subject = f"Flight {flight_id} Status Update: {status}"
                    message = (
                        f"Dear Passenger,\n\n"
                        f"Your flight {flight_id} is now {status}.\n\n"
                        f"Details:\n"
                        f"Departure: {flight_status['departure_airport']}\n"
                        f"Arrival: {flight_status['arrival_airport']}\n"
                        f"Status: {status}\n\n"
                        f"Thank you for choosing UnicornAir."
                    )
                    # send_email(email, subject, message)  # Uncomment to send emails
                    log_notification(booking_id, flight_id, status, message)
                    print(f"Logged notification for {email} - Flight {flight_id}: {status}")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching status for flight {flight_id}: {e}")

        # Poll every 5 minutes
        time.sleep(300)

if __name__ == '__main__':
    logging.info("Starting Notification Service")
    notification_service()
