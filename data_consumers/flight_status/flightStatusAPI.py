from fastapi import FastAPI, WebSocket
from kafka import KafkaConsumer
import json
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kafka Configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'flight_status_updates'

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='websocket_consumer_group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    try:
        for message in consumer:
            flight_data = message.value
            print(flight_data)
            await websocket.send_text(json.dumps(flight_data))
    except Exception as e:
        print(f"WebSocket Error: {e}")
    finally:
        await websocket.close()

# Run with: uvicorn websocket_api:app --reload
