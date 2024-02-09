import socket

def send_shutdown_signal():
    host = 'localhost'  # replace with the IP address of the board
    port = 12345  # must be the same as in the server script

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'shutdown')

if __name__ == '__main__':
    send_shutdown_signal()