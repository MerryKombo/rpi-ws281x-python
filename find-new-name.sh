#!/bin/bash
# set -x

# Default values
owner="goun"
type="3bplus"

# Check if command line arguments are provided
if [ $# -ge 2 ]; then
    owner=$1
    type=$2
fi

# Truncate owner name to first four characters
owner=$(echo $owner | cut -c 1-4)

# Variables
KNOWN_IP="$(hostname -I | awk '{print $1}')"
NETWORK_MASK=$(ip -o -f inet addr show | awk "/${KNOWN_IP}/ {print \$4}" | cut -d'/' -f2 | head -n 1)
NETWORK=$(ipcalc -n "$KNOWN_IP/$NETWORK_MASK" | awk '/Network:/ {print $2}')
SSH_KEY_PATH="/home/poddingue/.ssh/roundernetes"
USERNAME="poddingue"
INVENTORY_FILE="/home/$USERNAME/generated-inventory.ini"
LOG_FILE="/home/$USERNAME/generated-inventory.log"

find_ssh_machines() {
    nmap -p 22 "$NETWORK" -oG - | awk '/Host:/{ip=$2} /22\/open|22\/filtered/{print ip}'
}

# Get the IP addresses of all machines with open or filtered SSH ports
ssh_machines=$(find_ssh_machines)

# Print the value of ssh_machines for debugging
echo "SSH machines: $ssh_machines"

accessible_machines=""

# Declare an associative array
declare -A ip_hostname_map

for ip in $ssh_machines; do
    # Remove the stored key for the host
    ssh-keygen -R $ip

    # Attempt to log in to the machine with the roundernetes key
    if ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no -i $SSH_KEY_PATH "$USERNAME@$ip" exit; then
        # If the login is successful, add the machine to the list of accessible machines
        accessible_machines="$accessible_machines $ip"
    fi
done

# Print the value of accessible_machines for debugging
echo "Accessible machines: $accessible_machines"

for ip in $accessible_machines; do
    # Use avahi-resolve to get the hostname for the IP address
    avahi_hostname=$(avahi-resolve -4 -a $ip | awk '{print $2}')

    # Use ssh to get the hostname
    ssh_hostname=$(ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no -i $SSH_KEY_PATH "$USERNAME@$ip" hostname)

    # Compare the hostnames
    if [[ $avahi_hostname != "$ssh_hostname" ]]; then
        # If the hostnames are different, log the discrepancy
        echo "Discrepancy for IP $ip: Avahi hostname is $avahi_hostname, but ssh hostname is $ssh_hostname" >> "$LOG_FILE"
    fi

    # Add the IP and ssh_hostname to the associative array
    ip_hostname_map[$ip]=$ssh_hostname

    # Print the values of ssh_hostname and ip for debugging
    echo "ssh_hostname: $ssh_hostname, ip: $ip"
done

# Store the current hostname
current_hostname=$(hostname)

# Store the current IP
current_ip=$(hostname -I | awk '{print $1}')

# Print the associative array sorted by IP
for ip in $(echo "${!ip_hostname_map[@]}" | tr ' ' '\n' | sort -n -t . -k 1,1 -k 2,2 -k 3,3 -k 4,4); do
    echo "IP: $ip, Hostname: ${ip_hostname_map[$ip]}"
done

# Sort the IPs before updating the /etc/hosts file
sorted_ips=$(echo "${!ip_hostname_map[@]}" | tr ' ' '\n' | sort -n -t . -k 1,1 -k 2,2 -k 3,3 -k 4,4)

# Update the /etc/hosts file
for ip in $sorted_ips; do
    hostname=${ip_hostname_map[$ip]}
    if [[ $hostname != "$current_hostname" ]]; then
        if grep -q "$hostname" /etc/hosts; then
            # If the hostname is already in the file, update the existing entry
            sudo sed -i "/$hostname/d" /etc/hosts
        fi
        if grep -q "$hostname.local" /etc/hosts; then
            # If the hostname.local is already in the file, update the existing entry
            sudo sed -i "/$hostname.local/d" /etc/hosts
        fi
    else
        # If the hostname is the current hostname, remove all existing entries
        sudo sed -i "/$hostname/d" /etc/hosts
    fi
    # Check if hostname already ends with .local
    if [[ $hostname == *.local ]]; then
        # If it does, add the new entry with only "machine name"
        echo "$ip $hostname" | sudo tee -a /etc/hosts
    else
        # If it doesn't, add the new entry with both "machine name" and "machine name.local"
        echo "$ip $hostname $hostname.local" | sudo tee -a /etc/hosts
    fi
    # Append 'localhost' to lines that contain the current hostname but not 'localhost'
    sudo sed -i "/$current_hostname/ {/localhost/ !s/$/ localhost/}" /etc/hosts
done

# Clear the inventory file
echo "" > $INVENTORY_FILE

# Start the inventory file with the [pis] section
echo "[pis]" > $INVENTORY_FILE

# Add each IP address to the [pis] section
for ip in $sorted_ips; do
    # Get the hostname for the IP address
    hostname=$(ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no -i $SSH_KEY_PATH "$USERNAME@$ip" hostname)

    # Add the IP address, Python interpreter path, and hostname to the inventory file
    echo "$ip ansible_python_interpreter=/usr/bin/python3 # $hostname" >> $INVENTORY_FILE
done

# Add the [main-pi] section with the current hostname to the inventory file
echo -e "\n[main-pi]\n$current_hostname ansible_python_interpreter=/usr/bin/python3" >> $INVENTORY_FILE

# Generate the new name
echo "${owner}-${type}-3"
