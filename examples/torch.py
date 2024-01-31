#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
import argparse
import random
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 24  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

def torch_effect3(strip, flame_min, flame_max):
    # Initialize the color of each LED
    colors = [Color(flame_max, flame_max // 3, flame_max // 20) for _ in range(strip.numPixels())]

    while True:
        for i in range(strip.numPixels()):
            # Occasionally generate a new color for an LED
            if random.random() < 0.05:
                r = random.randint(flame_min, flame_max)
                g = min(max(int(r * 0.3), 0), 255)  # Green component is 30% of red component
                b = min(max(int(r * 0.05), 0), 255)  # Blue component is 5% of red component
                colors[i] = Color(r, g, b)

            # Set the color of the LED
            strip.setPixelColor(i, colors[i])

        # Update the LED strip
        strip.show()

        # Adjust for desired flickering speed
        time.sleep(0.2)


def torch_effect2(strip, base_r, base_g, base_b):
    for i in range(strip.numPixels()):
        flicker = random.randint(0, 55)
        r = max(base_r - flicker, 0)
        g = max(base_g - flicker, 0)
        b = max(base_b - flicker, 0)
        strip.setPixelColor(i, Color(r, g, b))
        strip.show()
        time.sleep(random.uniform(0.01, 0.113))  # Adjust for desired flickering speed


def torch_effect(strip, flame_min, flame_max):
    for i in range(strip.numPixels()):
        r = random.randint(flame_min, flame_max)
        g = r // 2
        b = r // 3
        strip.setPixelColor(i, Color(r, g, b))
        strip.show()
        time.sleep(0.1)  # Adjust for desired flickering speed


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
            print('Torch effect 3.')
            torch_effect3(strip, 100, 255)  # Call the torch effect function
            print('Torch effect 2.')
            base_r, base_g, base_b = 226, 121, 35  # Base color for the flame
            torch_effect2(strip, base_r, base_g, base_b)  # Call the torch effect function
            print('Color wipe animations.')
            colorWipe(strip, Color(255, 0, 0))  # Red wipe
            colorWipe(strip, Color(0, 255, 0))  # Green wipe
            colorWipe(strip, Color(0, 0, 255))  # Blue wipe
            print('Theater chase animations.')
            theaterChase(strip, Color(127, 127, 127))  # White theater chase
            theaterChase(strip, Color(127, 0, 0))  # Red theater chase
            theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
            print('Rainbow animations.')
            rainbow(strip)
            rainbowCycle(strip)
            theaterChaseRainbow(strip)
            print('Torch effect.')
            torch_effect(strip, 100, 255)  # Call the torch effect function

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0, 0, 0), 10)
