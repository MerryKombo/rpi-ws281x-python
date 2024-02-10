import socket
import os
import sys
import socket
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def generate_host_file(filename):
    """
    This function generates a host file containing IP addresses.

    Parameters:
    filename (str): The name of the file to be generated.

    Returns:
    None
    """
    arp_output = os.popen('arp -a').read()
    ip_addresses = re.findall(r'\((.*?)\)', arp_output)

    with open(filename, 'w') as file:
        for ip in ip_addresses:
            file.write(ip + '\n')

def send_command_to_all(command, host_file):
    """
    This function sends a command to all hosts listed in the host file.

    Parameters:
    command (str): The command to be sent.
    host_file (str): The file containing the list of hosts.

    Returns:
    None
    """
    # Generate the host file before reading it
    generate_host_file(host_file)

    with open(host_file, 'r') as file:
        hosts = file.read().splitlines()

    for host in hosts:
        logging.info(f"Sending command to host: {host}")
        try:
            send_command(command, host)
            logging.info(f"Command sent successfully to host: {host}")
        except Exception as e:
            logging.error(f"Failed to send command to host: {host}. Error: {e}")

def send_command(command, host):
    """
    This function sends a command to a specific host.

    Parameters:
    command (str): The command to be sent.
    host (str): The host to send the command to.

    Returns:
    None
    """
    port = 12345  # must be the same as in the server script

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(command.encode('utf-8'))

def start_server():
    """
    This function starts a server that listens for commands and performs actions based on the received commands.

    Returns:
    None
    """
    host = 'localhost'  # replace with the IP address of the board
    port = 12345  # choose an appropriate port
    master_host = 'goun-3bplus-1'  # replace with the hostname of the master
    host_file = 'hosts.txt'  # replace with the path to your file of hostnames

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                command = data.decode('utf-8')
                if command == 'shutdown':
                    print('Shutdown signal received. Shutting down...')
                    if socket.gethostname() == master_host:
                        send_command_to_all('shutdown', host_file)
                    os.system('sudo shutdown -h now')
                    break
                elif command == 'reboot':
                    print('Reboot signal received. Rebooting...')
                    if socket.gethostname() == master_host:
                        send_command_to_all('reboot', host_file)
                    os.system('sudo reboot')
                    break

if __name__ == '__main__':
    start_server()