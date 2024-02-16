#!/bin/bash
set +x

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

find_ssh_machines() {
    nmap -p 22 192.168.1.0/24 -oG - | awk '/Host:/{ip=$2} /22\/open|22\/filtered/{print ip}'
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
    if ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no -i ~/.ssh/roundernetes poddingue@$ip exit; then
        # If the login is successful, add the machine to the list of accessible machines
        accessible_machines="$accessible_machines $ip"
    fi
done

# Print the value of accessible_machines for debugging
echo "Accessible machines: $accessible_machines"

# Create a log file
logfile="$(pwd)/$0.log"

for ip in $accessible_machines; do
    # Use avahi-resolve to get the hostname for the IP address
    avahi_hostname=$(avahi-resolve -4 -a $ip | awk '{print $2}')

    # Use ssh to get the hostname
    ssh_hostname=$(ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no -i ~/.ssh/roundernetes poddingue@$ip hostname)

    # Compare the hostnames
    if [[ $avahi_hostname != $ssh_hostname ]]; then
        # If the hostnames are different, log the discrepancy
        echo "Discrepancy for IP $ip: Avahi hostname is $avahi_hostname, but ssh hostname is $ssh_hostname" >> $logfile
    fi

    # Add the IP and ssh_hostname to the associative array
    ip_hostname_map[$ip]=$ssh_hostname

    # Print the values of ssh_hostname and ip for debugging
    echo "ssh_hostname: $ssh_hostname, ip: $ip"
done

# Store the current hostname
current_hostname=$(hostname)

# Print the associative array sorted by IP
for ip in $(echo "${!ip_hostname_map[@]}" | tr ' ' '\n' | sort -n -t . -k 1,1 -k 2,2 -k 3,3 -k 4,4); do
    echo "IP: $ip, Hostname: ${ip_hostname_map[$ip]}"
done

# Sort the IPs before updating the /etc/hosts file
sorted_ips=$(echo "${!ip_hostname_map[@]}" | tr ' ' '\n' | sort -n -t . -k 1,1 -k 2,2 -k 3,3 -k 4,4)

# Update the /etc/hosts file
for ip in $sorted_ips; do
    hostname=${ip_hostname_map[$ip]}
    if [[ $hostname != $current_hostname ]]; then
        if grep -q $hostname /etc/hosts; then
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
        # Add 'localhost' to the current hostname line if it's not already present
        if [[ $hostname != localhost* ]]; then
            hostname="localhost $hostname"
        fi
    fi
    # Check if hostname already ends with .local
    if [[ $hostname == *.local ]]; then
        # If it does, add the new entry with only "machine name"
        echo "$ip $hostname" | sudo tee -a /etc/hosts
    else
        # If it doesn't, add the new entry with both "machine name" and "machine name.local"
        echo "$ip $hostname $hostname.local" | sudo tee -a /etc/hosts
    fi
done

# Generate the new name
echo "${owner}-${type}-3"
