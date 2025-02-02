import streamlit as st
import websocket
import json
import pandas as pd

# Streamlit UI Setup
st.set_page_config(page_title="✈️ Flight Status Dashboard", layout="wide")
st.title("Real-Time Flight Status Dashboard")

# Placeholder for Flight Status Updates
status_placeholder = st.empty()

# List to Store All Messages
messages = []

# WebSocket Message Handler
def on_message(ws, message):
    flight_data = json.loads(message)
    print(flight_data)
    messages.append(flight_data)

    # Display all messages as a table
    if messages:
        df = pd.DataFrame(messages)
        status_placeholder.dataframe(df[::-1])  # Show latest messages on top

# WebSocket Error Handler
def on_error(ws, error):
    st.error(f"WebSocket Error: {error}")

# WebSocket Close Handler
def on_close(ws, close_status_code, close_msg):
    st.warning("WebSocket connection closed")

# WebSocket Connection Setup
ws = websocket.WebSocketApp(
    "ws://localhost:8000/ws",  # WebSocket URL
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# Run WebSocket Connection
ws.run_forever()
