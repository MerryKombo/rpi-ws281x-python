#!/bin/bash

# Replace with the IP address of the board and the port number
SERVER="goun-3bplus-1.local:12345"

# Default command is 'reboot', if an argument is provided, command is 'shutdown'
COMMAND=${1:-reboot}

# Send POST request
curl -X POST -H "Content-Type: application/json" -d "{\"command\":\"$COMMAND\"}" $SERVER