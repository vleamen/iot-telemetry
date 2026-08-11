CREATE TABLE sensor_logs (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(50) NOT NULL,
    sensor_type VARCHAR(50) NOT NULL,
    reading_value DECIMAL NOT NULL,
    status_code VARCHAR(20),
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);