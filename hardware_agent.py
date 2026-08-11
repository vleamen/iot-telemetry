import requests
import time
import psutil
import socket

API_URL = "http://127.0.0.1:5001/api/ingest"

# Automatically get machine's actual network name
DEVICE_NAME = socket.gethostname() 

print(f"Starting live hardware monitor on {DEVICE_NAME}... Press Ctrl+C to stop.")

try:
    # Prime the CPU reader (the first reading is usually 0.0)
    psutil.cpu_percent(interval=0.1)

    while True:
        # 1. Read the real hardware sensors
        cpu_load = psutil.cpu_percent(interval=None)
        ram_usage = psutil.virtual_memory().percent
        
        # 2. Package and send the CPU telemetry
        requests.post(API_URL, json={
            "device_id": DEVICE_NAME,
            "sensor_type": "cpu_load_percent",
            "reading_value": cpu_load,
            # Dynamically flag high usage
            "status_code": "WARNING" if cpu_load > 85 else "OK" 
        })
        
        # 3. Package and send the RAM telemetry
        requests.post(API_URL, json={
            "device_id": DEVICE_NAME,
            "sensor_type": "ram_usage_percent",
            "reading_value": ram_usage,
            "status_code": "WARNING" if ram_usage > 85 else "OK"
        })
        
        print(f"Logged -> CPU: {cpu_load}% | RAM: {ram_usage}%")
        
        # Wait 1 second before grabbing the next snapshot
        time.sleep(1) 
        
except KeyboardInterrupt:
    print("\nHardware monitor stopped.")
except Exception as e:
    print(f"\nFailed to connect to API: {e}")
