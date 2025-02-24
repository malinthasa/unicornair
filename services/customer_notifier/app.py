import os
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

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USER = 'your_email@example.com'
SMTP_PASSWORD = 'your_password'


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


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn


def get_delayed_flight_bookings():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
                    select b.booking_id, b.flight_id, p."name" , p.email 
                    from booking b
                    inner join flight_status fs2 
                    on b.flight_id = fs2.flight_id
                    inner join passenger p 
                    on b.passenger_id = p.passenger_id
                    where fs2.status != 'Ontime';
    """)
    bookings = cursor.fetchall()
    conn.close()
    return bookings


def has_notification_been_sent(booking_id, flight_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 1 FROM notification
        WHERE booking_id = %s AND flight_id = %s
    """, (booking_id, flight_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

#
def log_notification(booking_id, flight_id, status, message):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notification (booking_id, flight_id, status, message)
        VALUES (%s, %s, %s, %s)
    """, (booking_id, flight_id, status, message))
    conn.commit()
    conn.close()


def notification_service():
    while True:
        bookings = get_delayed_flight_bookings()
        logging.debug(f"Found {len(bookings)} bookings")

        for booking in bookings:
            booking_id, flight_id, customer_name, email = booking
            logging.debug(f"Checking for notifications for {email} - Flight {flight_id}")

            try:
                if not has_notification_been_sent(booking_id, flight_id):
                    subject = f"Flight {flight_id} Status Update: Delayed"
                    message = f"""Dear {customer_name.split(" ")[0]},\n\n
                                  Your flight {flight_id} is now delayed.\n\n
                                  We apologize for the inconvinience occurred.
                               """
                    # send_email(email, subject, message)  # Uncomment to send emails
                    log_notification(booking_id, flight_id, 'delayed', message)
                    print(f"Logged notification for {email} - Flight {flight_id}: delayed")

            except requests.exceptions.RequestException as e:
                print(f"Error fetching status for flight {flight_id}: {e}")

        time.sleep(300)

if __name__ == '__main__':
    logging.info("Starting Notification Service")
    notification_service()
