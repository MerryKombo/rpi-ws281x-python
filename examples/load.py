# Please note that you need to install matplotlib using pip: ./bin/pip install matplotlib
# This script will print the 1-minute load average and the corresponding color every 5 seconds.
# The color is determined by looking up the load in the "colors" array.
# The load is multiplied by 10 to get the index in the array, and the min function is used to ensure that the index does not exceed the length of the array.
# The send_request function sends a POST request to the /light endpoint of the server with a JSON body containing the board name and color.
# Please note that you need to install the requests library using pip:
# ./bin/pip install requests

import os
import time
import requests
import socket
import matplotlib.cm as cm
import numpy as np

load_1, load_5, load_15 = os.getloadavg()

print(f"1 minute load: {load_1}")
print(f"5 minute load: {load_5}")
print(f"15 minute load: {load_15}")


# np.linspace(0, 1, 40) generates 40 evenly spaced points between 0 and 1.
# These points are then passed to the RdYlGn_r colormap to generate the corresponding colors.
# The colormap is reversed (_r) to go from green to red.
# The colors are returned as RGBA tuples with values between 0 and 1, so they are multiplied by 255 and converted to integers to get 8-bit RGB values.
# Create an array of 40 points from 0 to 1
points = np.linspace(0, 1, 40)

# Use the RdYlGn (Red-Yellow-Green) reversed colormap
cmap = cm.get_cmap('RdYlGn_r')

# Generate the colors
colors = [cmap(point) for point in points]

# This will give you an array of 40 colors, going from green to red, which you can use to represent load from 0.0 to 4.0 in increments of 0.1.
# Convert colors to 8-bit RGB values
colors = [(int(r*255), int(g*255), int(b*255)) for r, g, b, _ in colors]

def send_color_to_server(board_name, color):
    url = 'http://goun-3bplus-1.local:5000/light'
    data = {'board_name': board_name, 'color': color}
    response = requests.post(url, json=data)
    print(f'Response from server: {response.text}')


if __name__ == '__main__':
    # Get the hostname
    board_name = socket.gethostname()

while True:
    # Get the 1-minute load average
    load_1, _, _ = os.getloadavg()

    # Calculate the index in the colors array that corresponds to the load
    index = min(int(load_1 * 10), len(colors) - 1)

    # Get the color
    color = colors[index]

    # Print the load and the corresponding color
    print(f"1 minute load: {load_1}, color: {color}")

    # Send the color to the server
    send_color_to_server('your_board_name', color)

    # Wait for a bit before the next iteration
    time.sleep(5)