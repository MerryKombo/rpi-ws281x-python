#!/bin/bash

# Enable printing of each command to the terminal
set -x

# Variables
KNOWN_IP="192.168.1.142"
SSH_KEY_PATH="/home/poddingue/.ssh/roundernetes.pub"
USERNAME="poddingue"
INVENTORY_FILE="/home/$USERNAME/generated-inventory.ini"
LOG_FILE="/home/$USERNAME/generated-inventory.log"

# Create the log file if it does not exist and clear it
ssh -i $SSH_KEY_PATH $USERNAME@$KNOWN_IP "touch $LOG_FILE && > $LOG_FILE" &>>$LOG_FILE

# SSH into the known machine and get its network mask
IP_OUTPUT=$(ssh -i $SSH_KEY_PATH $USERNAME@$KNOWN_IP "bash -c '/usr/sbin/ip -o -f inet addr show'" &>>$LOG_FILE)
echo "IP_OUTPUT: $IP_OUTPUT"

AWK_OUTPUT=$(echo "$IP_OUTPUT" | awk "/192.168.1.142/ {print \$4}")
echo "AWK_OUTPUT: $AWK_OUTPUT"

NETWORK_MASK=$(echo "$AWK_OUTPUT" | head -n 1)
echo "NETWORK_MASK: $NETWORK_MASK"
# Check if the SSH command was successful
if [ $? -ne 0 ]; then
    echo "Error: SSH command failed. Please check the SSH configuration."
    exit 1
fi

# Check if NETWORK_MASK is set
if [ -z "$NETWORK_MASK" ]; then
    echo "Error: NETWORK_MASK is not set. Please check the network configuration of the remote machine."
    exit 1
fi

# Use the network mask to scan the local network and get the list of IPs
IP_LIST=$(ssh -i $SSH_KEY_PATH $USERNAME@$KNOWN_IP "nmap -sn $NETWORK_MASK -oG - | awk '/Up$/{print \$2}'" &>>$LOG_FILE)

# Check if IP_LIST is set
if [ -z "$IP_LIST" ]; then
    echo "Error: IP_LIST is not set. Please check the network configuration of the remote machine."
    exit 1
fi

# Try to log into each IP and add it to the inventory file if successful
for IP in $IP_LIST; do
    ssh -i $SSH_KEY_PATH -o BatchMode=yes -o ConnectTimeout=5 $USERNAME@$IP echo &>>$LOG_FILE
    if [ $? -eq 0 ]; then
        ssh -i $SSH_KEY_PATH $USERNAME@$KNOWN_IP "echo '$IP ansible_python_interpreter=/usr/bin/python3' >> $INVENTORY_FILE" &>>$LOG_FILE
    fi
done

# Copy the inventory file back to the local machine
scp -i $SSH_KEY_PATH $USERNAME@$KNOWN_IP:$INVENTORY_FILE . &>>$LOG_FILE

# Copy the log file back to the local machine
scp -i $SSH_KEY_PATH $USERNAME@$KNOWN_IP:$LOG_FILE .