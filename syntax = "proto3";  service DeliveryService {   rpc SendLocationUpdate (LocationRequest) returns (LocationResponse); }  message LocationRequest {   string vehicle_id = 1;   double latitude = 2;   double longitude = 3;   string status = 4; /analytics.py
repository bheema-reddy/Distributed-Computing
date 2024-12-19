from pymongo import MongoClient
from sklearn.linear_model import LinearRegression
import numpy as np
import time

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["delivery_db"]
collection = db["location_data"]

# Sample model for ETA prediction
X = np.array([[10, 0.5], [20, 0.6], [30, 0.8]])  # Distance, traffic factor
y = np.array([15, 30, 45])  # ETAs in minutes
model = LinearRegression().fit(X, y)

def predict_eta(distance, traffic_factor):
    return model.predict([[distance, traffic_factor]])[0]

# Predict ETAs and print status based on MongoDB records
while True:
    for record in collection.find():
        vehicle_id = record['vehicle_id']
        status = record['status']

        # Example values for distance and traffic factor
        distance = 25
        traffic_factor = 0.7
        eta = predict_eta(distance, traffic_factor)

        print(f"Vehicle ID: {vehicle_id} | Status: {status} | Predicted ETA: {eta:.2f} minutes")
    time.sleep(5)  # Run periodically every 5 seconds
