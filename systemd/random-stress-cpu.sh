#!/bin/bash

# Log the start of the script
echo "Starting random-stress-cpu.sh at $(date)" >> /home/poddingue/logs/stress-cpu.log

# Generate a random delay between 600 and 1200 seconds (10 to 20 minutes)
RANDOM_DELAY=$(( RANDOM % 601 + 600 ))
echo "Random delay: $RANDOM_DELAY seconds" >> /home/poddingue/logs/stress-cpu.log

# Sleep for the random delay
sleep $RANDOM_DELAY

# Start the stress-cpu service
echo "Starting stress-cpu.service at $(date)" >> /home/poddingue/logs/stress-cpu.log
systemctl start stress-cpu.service

# Let the stress-cpu.py script run for 5 minutes (300 seconds)
sleep 300

# Stop the stress-cpu service
echo "Stopping stress-cpu.service at $(date)" >> /home/poddingue/logs/stress-cpu.log
systemctl stop stress-cpu.service

