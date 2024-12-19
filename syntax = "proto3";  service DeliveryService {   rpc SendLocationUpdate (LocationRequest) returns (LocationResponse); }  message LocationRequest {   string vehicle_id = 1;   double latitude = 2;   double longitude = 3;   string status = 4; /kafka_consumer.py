from kafka import KafkaConsumer
from pymongo import MongoClient
import json

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["delivery_db"]
collection = db["location_data"]

# Kafka consumer setup
consumer = KafkaConsumer(
    'location_updates',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Process incoming messages from Kafka
for message in consumer:
    data = message.value
    vehicle_id = data['vehicle_id']
    status = data['status']

    # Store data in MongoDB
    collection.insert_one(data)
    print(f"Stored data for vehicle {vehicle_id} with status: {status}")
