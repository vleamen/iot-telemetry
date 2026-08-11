import requests
import time
import random

# The URL of your Flask API
API_URL = "http://127.0.0.1:5001/api/ingest"

# A list of fake devices in our network
DEVICES = ["sensor-alpha-01", "sensor-beta-02", "sensor-gamma-03", "drone-esc-04"]

def generate_payload():
    """Creates a random JSON payload mimicking a sensor reading."""
    return {
        "device_id": random.choice(DEVICES),
        "sensor_type": random.choice(["temperature", "voltage", "rpm"]),
        "reading_value": round(random.uniform(20.0, 100.0), 2),
        "status_code": random.choice(["OK", "OK", "OK", "WARNING"]) # mostly OKs
    }

print("Starting IoT Simulator... Press Ctrl+C to stop.")

try:
    while True:
        payload = generate_payload()
        
        # Send the POST request to Flask
        response = requests.post(API_URL, json=payload)
        
        if response.status_code == 201:
            print(f"Sent data for {payload['device_id']}: {payload['reading_value']}")
        else:
            print(f"Failed to send data: {response.status_code}")
            
        # Wait a tiny fraction of a second before sending the next one
        time.sleep(0.2) 
        
except KeyboardInterrupt:
    print("\nSimulator stopped.")
