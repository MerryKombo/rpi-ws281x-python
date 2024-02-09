import socket

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
                elif data.decode('utf-8') == 'shutdown':
                    print('Shutdown signal received. Shutting down...')
                    # Insert your shutdown command here
                    break

if __name__ == '__main__':
    start_server()