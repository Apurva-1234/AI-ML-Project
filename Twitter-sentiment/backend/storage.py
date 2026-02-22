# backend/storage.py
from datetime import datetime

predictions = []

def add_prediction(sentiment):
    predictions.append({
        "time": datetime.now(),
        "sentiment": sentiment
    })
