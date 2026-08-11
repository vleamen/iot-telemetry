from flask import Flask, request, jsonify
import psycopg2
import logging
import os

# Set up basic logging so we can track errors in the terminal
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

import os

def get_db_connection():
    return psycopg2.connect(
        # Look for Docker variables first, default to local settings if not found
        host=os.environ.get("DB_HOST", "localhost"),
        database="iot_telemetry", 
        user=os.environ.get("DB_USER", "vincentnguyen"),     
        password=os.environ.get("DB_PASSWORD", "")               
    )


@app.route('/api/ingest', methods=['POST']) # More professional endpoint name
def ingest_data():
    data = request.get_json()
    
    # Extract generalized elements
    device = data.get('device_id')
    sensor = data.get('sensor_type')
    value = data.get('reading_value')
    status = data.get('status_code', 'OK') # Defaults to 'OK' if not provided
    
    # Basic validation: ensure required fields exist
    if not all([device, sensor, value]):
        return jsonify({"error": "Missing required fields"}), 400
        
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            """INSERT INTO sensor_logs (device_id, sensor_type, reading_value, status_code) 
               VALUES (%s, %s, %s, %s)""",
            (device, sensor, value, status)
        )
        conn.commit()
        cur.close()
        
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Database error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if conn:
            conn.close()
            
    return jsonify({"status": "success"}), 201

if __name__ == '__main__':
    # "0.0.0.0" accepts external Docker traffic
    app.run(host="0.0.0.0", port=5001, debug=True)
