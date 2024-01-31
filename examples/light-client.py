# In this script, replace 'http://your_server_ip_address:5000/light' with the actual IP address and port of your server.
# The send_request function sends a POST request to the /light endpoint of the server with a JSON body containing the board name and color.
# Please note that you need to install the requests library using pip:
# ./bin/pip install requests
# You can then run this script to send a request to the server. The server should light up the LEDs associated with the board name in the specified color.

import requests
import socket

def send_request(board_name, color):
    url = 'http://goun-3bplus-1.local:5000/light'
    data = {'board_name': board_name, 'color': color}
    response = requests.post(url, json=data)
    print(f'Response from server: {response.text}')

if __name__ == '__main__':
    # Get the hostname
    board_name = socket.gethostname()

    # Define the colors
    colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        # add more colors as needed
    }

    send_request(board_name, colors["blue"])