import os
import re
import argparse

def generate_host_file_with_arp(filename):
    """
    This function generates a host file containing IP addresses using the arp command.

    Parameters:
    filename (str): The name of the file to be generated.

    Returns:
    None
    """
    arp_output = os.popen('arp -a').read()
    ip_addresses = re.findall(r'\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)', arp_output)

    with open(filename, 'w') as file:
        for ip in ip_addresses:
            file.write(ip + '\n')

def generate_host_file_with_nmap(filename):
    """
    This function generates a host file containing IP addresses using the nmap command.

    Parameters:
    filename (str): The name of the file to be generated.

    Returns:
    None
    """
    # Replace '192.168.1.0/24' with your network range
    nmap_output = os.popen('nmap -sn 192.168.1.0/24').read()
    ip_addresses = re.findall(r'\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)', nmap_output)

    with open(filename, 'w') as file:
        for ip in ip_addresses:
            file.write(ip + '\n')

if __name__ == '__main__':
    """
    Main function that parses command line arguments and calls the appropriate function to generate the host file.
    """
    parser = argparse.ArgumentParser(description='Generate host file using arp or nmap.')
    parser.add_argument('--arp', action='store_true', help='Use arp to generate host file.')
    args = parser.parse_args()

    if args.arp:
        generate_host_file_with_arp('hosts.txt')
    else:
        generate_host_file_with_nmap('hosts.txt')