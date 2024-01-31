import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 24        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def light_up_boards(strip, board_leds):
    """Light up all LEDs linked to each board."""
    for board, leds in board_leds.items():
        print(f"Lighting up LEDs for board {board}...")

        # Turn off all LEDs
        colorWipe(strip, Color(0, 0, 0), 0)

        # Turn on the LEDs for the current board
        for led in leds:
            strip.setPixelColor(led, Color(255, 0, 0))  # Set to red for visibility
            strip.show()

        print(f"LEDs for board {board} are now on. Press enter to continue...")
        input()  # Wait for user to press enter

# Main program logic follows:
if __name__ == '__main__':
    print('Press Ctrl-C to quit.')
    try:
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

        while True:
            light_up_boards(strip, board_leds)
    except KeyboardInterrupt:
        colorWipe(strip, Color(0, 0, 0), 10)