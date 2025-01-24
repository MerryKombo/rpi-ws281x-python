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

# SSH into the known machine and get its network configuration
IP_OUTPUT=$(ssh -i $SSH_KEY_PATH $USERNAME@$KNOWN_IP "bash -c '/usr/sbin/ip -o -f inet addr show'" 2>>$LOG_FILE)
echo "IP_OUTPUT: $IP_OUTPUT"

# Check if IP_OUTPUT is empty
if [ -z "$IP_OUTPUT" ]; then
    echo "Error: No output from 'ip' command. Please check the SSH connection and the remote machine's network configuration."
    exit 1
fi

# Extract the subnet mask for the known IP
SUBNET_MASK=$(echo "$IP_OUTPUT" | awk -v ip="$KNOWN_IP" '$0 ~ ip {split($4, a, "/"); print a[2]}')
echo "SUBNET_MASK: $SUBNET_MASK"

# Check if SUBNET_MASK is empty
if [ -z "$SUBNET_MASK" ]; then
    echo "Error: SUBNET_MASK is not set. Please check the network configuration of the remote machine."
    exit 1
fi

# Derive the network mask from the subnet mask
NETWORK_MASK=$(echo "$KNOWN_IP" | awk -F '.' -v subnet_mask="$SUBNET_MASK" '{print $1"."$2"."$3".0/"subnet_mask}')
echo "NETWORK_MASK: $NETWORK_MASK"

# Check if NETWORK_MASK is set
if [ -z "$NETWORK_MASK" ]; then
    echo "Error: NETWORK_MASK is not set. Please check the network configuration of the remote machine."
    exit 1
fi

# Use the network mask to scan the local network and get the list of IPs
IP_LIST=$(ssh -i $SSH_KEY_PATH $USERNAME@$KNOWN_IP "nmap -sn $NETWORK_MASK -oG - | awk '/Up$/{print \$2}'" 2>>$LOG_FILE)

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
