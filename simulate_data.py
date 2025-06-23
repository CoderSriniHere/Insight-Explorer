import random
from datetime import datetime, timedelta
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["ai_intern"]
collection = db["parameter_metadata"]

# Clear existing data
collection.delete_many({})

# Define start date and number of entries
start_time = datetime.utcnow() - timedelta(weeks=3)
entries = 21 * 24  # 21 days of hourly data

for i in range(entries):
    timestamp = start_time + timedelta(hours=i)
    doc = {
        "timestamp": timestamp,
        "temperature": round(random.uniform(20, 35), 2),
        "humidity": round(random.uniform(30, 70), 2),
        "pressure": round(random.uniform(990, 1020), 2),
        "voltage": round(random.uniform(210, 250), 2),
        "current": round(random.uniform(0.5, 10), 2),
        "co2_level": round(random.uniform(400, 1000), 2),
        "noise_level": round(random.uniform(30, 100), 2),
        "light": round(random.uniform(100, 1000), 2),
        "vibration": round(random.uniform(0, 5), 2),
        "altitude": round(random.uniform(0, 100), 2)
    }
    collection.insert_one(doc)

print(f"✅ Inserted {entries} documents into 'parameter_metadata'")
