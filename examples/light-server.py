# This script creates a web server that listens for POST requests on the /light endpoint.
# The request should contain a JSON body with a board_name and a color (a tuple of RGB values).
# When a request is received, the server will light up the LEDs associated with the specified board in the specified color.
# Please note that you need to install Flask using pip: pip install flask
# Also, this script should be run with root privileges to access the GPIO pins: sudo python3 light-server.py
# You can then send a POST request to http://your_pi_ip_address:5000/light with a JSON body like {"board_name": "dami-3bplus-2", "color": [255, 0, 0]} to light up the LEDs.

from flask import Flask, request
from rpi_ws281x import PixelStrip, Color
import logging

# Sets up the logging to output messages of level INFO and above.
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# LED strip configuration:
LED_COUNT = 24
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

# Define the mapping of boards to LEDs
board_leds = {
    'dami-3bplus-2': [0, 8, 18, 19],
    'dami-3bplus-3': [0, 1, 8, 19, 20, 21],
    'dami-3bplus-1': [1, 2, 8, 21, 22],
    'goun-3bplus-1': [2, 3, 9, 8, 9, 10, 22, 23],
    'goun-3bplus-2': [3, 4, 10, 11, 10, 11, 12],
    'dami-3b-1': [5, 13, 13, 14],
    'dami-3b-2': [5, 6, 15, 14, 15, 16],
    'goun-3bplus-3': [6, 7, 16, 17],
    'dami-3bplus-2': [7, 17, 18, 19],
}


def light_up_board(board_name, color):
    """Light up all LEDs linked to a board."""
    if board_name in board_leds:
        for led in board_leds[board_name]:
            strip.setPixelColor(led, color)
            strip.show()

@app.route('/light', methods=['POST'])
def light_up():
    data = request.get_json()
    board_name = data.get('board_name')
    color = data.get('color')

    # Check if color is a string (color name) or a list/tuple (RGB values)
    if isinstance(color, list) or isinstance(color, tuple):
        # Log the RGB values
        logging.info(f'Received color RGB values {color} for board {board_name}')

        # Convert RGB values to a Color
        color = Color(*color)

    light_up_board(board_name, color)
    return 'OK', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
