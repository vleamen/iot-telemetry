#!/bin/bash

# Navigate to the folder where this script is saved
cd "$(dirname "$0")"

# Activate the virtual environment
source venv/bin/activate

echo "Starting IoT Telemetry Pipeline..."

# 1. Start the Docker backend (API and Database) in detached mode
echo "Spinning up Docker containers..."
docker-compose up --build -d

# Give the database a few seconds to fully initialize
sleep 4 

# 2. Start the local Hardware Monitor
echo "Starting Hardware Agent..."
python3 hardware_agent.py &
AGENT_PID=$!

# 3. Start the local Visualizer
echo "Starting Visualizer GUI..."
python3 visualizer.py &
VIS_PID=$!

echo "All systems running!"
echo "Press [Ctrl + C] in this window to stop everything."

# 4. Catch the Ctrl+C command to cleanly shut down the scripts AND Docker
trap "echo 'Shutting down pipeline...'; kill $AGENT_PID $VIS_PID; docker-compose down; exit" SIGINT

wait
