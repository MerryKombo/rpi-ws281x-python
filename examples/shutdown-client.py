import socket
import sys

def send_command(command):
    host = 'localhost'  # replace with the IP address of the board
    port = 12345  # must be the same as in the server script

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(command.encode('utf-8'))

if __name__ == '__main__':
    # send 'reboot' by default, 'shutdown' if an argument is provided
    command = 'shutdown' if len(sys.argv) > 1 else 'reboot'
    send_command(command)