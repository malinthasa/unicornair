import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)

# API Endpoint
API_URL = "http://api:8000/flights"

# Streamlit Configuration
st.set_page_config(page_title="UnicornAir Flight Info Display", layout="wide")
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: #FFFFFF;
        }
        .big-font {
            font-size: 40px !important;
            font-weight: bold;
            color: #ffffff;
            text-align: center;
            padding: 10px 0;
        }
        .status-on-time {
            background-color: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
        }
        .status-delayed {
            background-color: #dc3545;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
        }
        .status-departed, .status-arrived {
            background-color: #007bff;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
        }
        .status-cancelled {
            background-color: #6c757d;
            color: white;
            padding: 5px 10px;
            border-radius: 5px;
        }
        .flight-table {
            background-color: #000;
            color: #fff;
            border-collapse: collapse;
            width: 100%;
            text-align: center;
        }
        .flight-table th, .flight-table td {
            padding: 15px;
            border: 1px solid #444;
            font-size: 20px;
            word-wrap: break-word;
        }
        .flight-table th {
            background-color: #1a1a1a;
        }
        .flight-table td {
            background-color: #111111;
        }
        th.flight-col, td.flight-col { width: 120px; }
        th.from-col, td.from-col { width: 120px; }
        th.to-col, td.to-col { width: 120px; }
        th.status-col, td.status-col { width: 150px; }
        th.time-col, td.time-col { width: 180px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛬 UnicornAir Flight Information")

# Function to fetch data from the API
def fetch_latest_flights():
    try:
        response = requests.get(API_URL)
        
        if response.status_code == 200:
            data = pd.DataFrame(response.json())
            return data.sort_values(by="timestamp", ascending=False).head(10)
        else:
            st.error("Failed to fetch data from API")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return pd.DataFrame()

# Auto-refresh every 15 seconds
REFRESH_INTERVAL = 15

# Display Flight Information
flight_data = fetch_latest_flights()

if not flight_data.empty:
    st.markdown("<div class='big-font'>Flight Status Board</div>", unsafe_allow_html=True)
    
    def format_status(status):
        status_classes = {
            "ON_TIME": "status-on-time",
            "DELAYED": "status-delayed",
            "DEPARTED": "status-departed",
            "ARRIVED": "status-arrived",
            "CANCELLED": "status-cancelled"
        }
        css_class = status_classes.get(status, "")
        return f"<span class='{css_class}'>{status}</span>"

    # Display the flight table
    st.markdown("<table class='flight-table'>", unsafe_allow_html=True)
    st.markdown("<tr><th class='flight-col'>Flight</th><th class='from-col'>From</th><th class='to-col'>To</th><th class='status-col'>Status</th><th class='time-col'>Time</th></tr>", unsafe_allow_html=True)

    for _, row in flight_data.iterrows():
        status_html = format_status(row['status'])
        # Format timestamp to show only up to minutes
        formatted_time = datetime.strptime(row['timestamp'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y-%m-%d %H:%M")
        st.markdown(
            f"<tr>"
            f"<td class='flight-col'>{row['flight_id']}</td>"
            f"<td class='from-col'>{row['departure_airport']}</td>"
            f"<td class='to-col'>{row['arrival_airport']}</td>"
            f"<td class='status-col'>{status_html}</td>"
            f"<td class='time-col'>{formatted_time}</td>"
            f"</tr>",
            unsafe_allow_html=True
        )

    st.markdown("</table>", unsafe_allow_html=True)
else:
    st.warning("No recent flight data available.")

# Auto-refresh feature
st.caption(f"Screen auto-refreshes every {REFRESH_INTERVAL} seconds.")
time.sleep(REFRESH_INTERVAL)
st.rerun()
