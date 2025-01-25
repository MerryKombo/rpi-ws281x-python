#!/bin/bash

# Lock file to prevent multiple instances
LOCK_FILE="/home/poddingue/random-stress-cpu.lock"

# Function to clean up the lock file
cleanup() {
    echo "Cleaning up lock file: $LOCK_FILE" >> /home/poddingue/logs/stress-cpu.log
    rm -f "$LOCK_FILE"
}

# Trap EXIT signal to ensure cleanup
trap cleanup EXIT

# Check if another instance is running
if [ -f "$LOCK_FILE" ]; then
    echo "Another instance of random-stress-cpu.sh is already running. Exiting." >> /home/poddingue/logs/stress-cpu.log
    exit 1
fi

# Create the lock file
echo "Creating lock file: $LOCK_FILE" >> /home/poddingue/logs/stress-cpu.log
touch "$LOCK_FILE"

# Log the start of the script
echo "Starting random-stress-cpu.sh at $(date)" >> /home/poddingue/logs/stress-cpu.log

# Generate a random delay between 600 and 1200 seconds (10 to 20 minutes)
RANDOM_DELAY=$(( RANDOM % 601 + 600 ))
echo "Random delay: $RANDOM_DELAY seconds" >> /home/poddingue/logs/stress-cpu.log

# Sleep for the random delay
sleep $RANDOM_DELAY

# Start the Python script and stop it after 3 minutes
echo "Starting stress-cpu.py at $(date)" >> /home/poddingue/logs/stress-cpu.log
timeout 180 /usr/bin/python3 /home/poddingue/rpi-ws281x-python/examples/stress-cpu.py

# Log the end of the script
echo "Stopping stress-cpu.py at $(date)" >> /home/poddingue/logs/stress-cpu.log
