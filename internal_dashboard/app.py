import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px

# API Endpoint
API_URL = "http://flight_status_api:8000/flights"

# Streamlit Configuration
st.set_page_config(page_title="UnicornAir Flight Status Dashboard", layout="wide")
st.title("🛫 UnicornAir Flight Status Dashboard")

# Function to fetch data from the API
def fetch_flight_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error("Failed to fetch data from API")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {e}")
        return pd.DataFrame()

# Auto-refresh every 30 seconds
REFRESH_INTERVAL = 30

# Streamlit Layout
st.sidebar.header("Filters")
status_filter = st.sidebar.selectbox("Select Flight Status", ("ALL", "ON_TIME", "DELAYED", "DEPARTED", "ARRIVED", "CANCELLED"))

# Fetch data from API
flight_data = fetch_flight_data()

# Apply status filter if selected
if status_filter != "ALL" and not flight_data.empty:
    flight_data = flight_data[flight_data['status'] == status_filter]

# Display Data Table
st.subheader("📋 Flight Status Overview")
if not flight_data.empty:
    st.dataframe(flight_data.sort_values(by="timestamp", ascending=False), height=400)

    # Visualizations
    st.subheader("📊 Flight Status Summary")
    status_counts = flight_data['status'].value_counts()
    st.bar_chart(status_counts)

    st.subheader("🕗 Delay Reasons Analysis")
    delay_data = flight_data[flight_data['status'] == "DELAYED"]

    if not delay_data.empty:
        delay_reasons = delay_data['delay_reason'].value_counts().reset_index()
        delay_reasons.columns = ['Reason', 'Count']

        # Create Pie Chart
        fig = px.pie(delay_reasons, names='Reason', values='Count', title='Delay Reasons Distribution')
        st.plotly_chart(fig)
    else:
        st.info("No delayed flights to display delay reasons.")
else:
    st.warning("No flight data available. Please check the API or data source.")

# Auto-refresh feature
st.caption(f"Dashboard auto-refreshes every {REFRESH_INTERVAL} seconds.")
time.sleep(REFRESH_INTERVAL)
st.rerun()
