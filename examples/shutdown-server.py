import socket
import os
import sys
import socket

def send_command_to_all(command, host_file):
    with open(host_file, 'r') as file:
        hosts = file.read().splitlines()

    for host in hosts:
        send_command(command, host)

def send_command(command, host):
    port = 12345  # must be the same as in the server script

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(command.encode('utf-8'))

def start_server():
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