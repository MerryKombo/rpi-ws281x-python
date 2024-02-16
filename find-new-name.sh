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

for ip in $accessible_machines; do
    # Use avahi-resolve to get the hostname for the IP address
    hostname=$(avahi-resolve -4 -a $ip | awk '{print $2}')

    # If avahi-resolve fails, use ssh to get the hostname
    if [ -z "$hostname" ]; then
        hostname=$(ssh -o BatchMode=yes -o ConnectTimeout=5 -o StrictHostKeyChecking=no -i ~/.ssh/roundernetes poddingue@$ip hostname)
    fi

    # Print the values of hostname and ip for debugging
    echo "hostname: $hostname, ip: $ip"
done

# Generate the new name
echo "${owner}-${type}-3"