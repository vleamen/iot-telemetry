# iot-telemetry

A containerized data pipeline built to handle high-frequency hardware telemetry. 

Instead of relying on simulated data, this project uses a local Python agent to scrape real-time CPU and RAM utilization directly from the host machine. It fires those metrics to a Flask API, logs them permanently into a PostgreSQL database, and queries them back out to a live-updating Matplotlib dashboard.

I built this to get hands-on with the kind of data ingestion you'd see in enterprise IoT systems or vehicle hardware, focusing on making the backend lightweight, scalable, and deployable anywhere using Docker.

## Under the Hood
* **The Agent:** A lightweight script using `psutil` to track hardware load and push JSON payloads.
* **The API (Flask):** The ingestion engine. It catches the payloads, validates them, and securely maps them to the database.
* **The Database (PostgreSQL):** Permanent storage. Spun up automatically via Docker volumes with a pre-configured relational schema.
* **The Visualizer:** A localized Matplotlib GUI that queries the database on a loop and graphs the system load in real-time. 

## Key Features
* **Clean Architecture:** Strict separation of concerns between the containerized backend and the local edge clients.
* **Dockerized Backend:** Built with multi-stage Dockerfiles to keep the Flask production image lean, using Docker Compose to network the API and Postgres together so they work out of the box.
* **Real-World Networking:** Configured host-binding (`0.0.0.0`) and connection-retry logic to ensure the API and database sync up perfectly on boot.

## Tech Stack
* **Backend:** Python, Flask, PostgreSQL (`psycopg2`)
* **Infrastructure:** Docker, Docker Compose
* **Client:** `requests`, `psutil`, `matplotlib`

---

## How to Run It

You don't need to install Postgres locally as Docker handles the heavy lifting.

1. Make sure Docker Desktop is running, then spin up the API and database:

docker-compose up --build -d

2. In your virtual environment, install the local dependencies and run the start script:

pip install requests psutil matplotlib psycopg2-binary
./start_pipeline.command

(Hit Ctrl + C in the terminal to cleanly kill the local processes when you're done).