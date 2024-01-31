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