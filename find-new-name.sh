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

# Get the hostnames and IP addresses of all machines in the local network
# The awk command is used to extract the hostname and IP address from the output of the avahi-browse command
hostnames_and_ips=$(avahi-browse -alr | awk '/=/{print $4, $8}')

# Print the value of hostnames_and_ips for debugging
echo "hostnames_and_ips: $hostnames_and_ips"

for hostname_and_ip in $hostnames_and_ips; do
    # Use awk to separate the hostname and IP address
    hostname=$(echo $hostname_and_ip | awk '{print $1}')
    ip=$(echo $hostname_and_ip | awk '{print $2}')

    # Print the values of hostname and ip for debugging
    echo "hostname: $hostname, ip: $ip"
done

# Generate the new name
echo "${owner}-${type}-3"