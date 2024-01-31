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

def identify_leds(strip):
    """Light up each LED in sequence with a unique color."""
    for i in range(strip.numPixels()):
        # Turn off all LEDs
        colorWipe(strip, Color(0, 0, 0), 0)

        # Turn on the current LED with a unique color
        strip.setPixelColor(i, Color(255, 0, 0))  # Set to red for visibility
        strip.show()

        print(f"LED {i} is now on. Press enter to continue...")
        input()  # Wait for user to press enter

# Main program logic follows:
if __name__ == '__main__':
    print('Press Ctrl-C to quit.')
    try:
        while True:
            identify_leds(strip)
    except KeyboardInterrupt:
        colorWipe(strip, Color(0, 0, 0), 10)