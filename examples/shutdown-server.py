import socket
import os

def start_server():
    host = 'localhost'  # replace with the IP address of the board
    port = 12345  # choose an appropriate port

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
                    os.system('sudo shutdown -h now')
                    break
                elif command == 'reboot':
                    print('Reboot signal received. Rebooting...')
                    os.system('sudo reboot')
                    break

if __name__ == '__main__':
    start_server()