'''
Course: ESC 204
Team: 0105-08
Project: Plant Monitoring System
Description: This file contains the main program that will run on the Raspberry Pi Pico.
'''

import time
import board
import digitalio

LED_PINS = {
    'RED': board.GP17,  # FINAL PIN
    'BLUE': board.GP12,  # FINAL PIN
    'GREEN': board.GP19  # FINAL PIN
}

WORKER_BUTTON = board.GP10  # FINAL PIN
SYSTEM_BUTTON = board.GP22  # FINAL PIN


class LED_CONTROLLER:
    def __init__(self, redPin, greenPin, bluePin):

        # initialize the LEDs
        self.redPin = digitalio.DigitalInOut(redPin)
        self.greenPin = digitalio.DigitalInOut(greenPin)
        self.bluePin = digitalio.DigitalInOut(bluePin)

        self.redPin.direction = digitalio.Direction.OUTPUT
        self.greenPin.direction = digitalio.Direction.OUTPUT
        self.bluePin.direction = digitalio.Direction.OUTPUT

        # When the LEDs are initialized (worker mode will be enabled by default)
        self.LEDs_white()

    # Turn off all three LEDs
    def LEDs_off(self):
        self.redPin.value = False
        self.greenPin.value = False
        self.bluePin.value = False

    # LEDs for the plants
    def LEDs_pink(self):
        self.redPin.value = True
        self.greenPin.value = False
        self.bluePin.value = True

    # LEDs for worker
    def LEDs_white(self):
        self.redPin.value = True
        self.greenPin.value = True
        self.bluePin.value = True


class BOARD_CONTROLLER:
    def __init__(self):

        # Initialize the board's LED
        self.Leds = LED_CONTROLLER(
            LED_PINS['RED'], LED_PINS['GREEN'], LED_PINS['BLUE'])

        self.board_led = digitalio.DigitalInOut(board.LED)
        self.board_led.direction = digitalio.Direction.OUTPUT

        # Initialize the buttons
        self.WorkerButton = digitalio.DigitalInOut(WORKER_BUTTON)
        self.WorkerButton.direction = digitalio.Direction.INPUT
        self.WorkerButton.pull = digitalio.Pull.UP  # Set internal pull-up resistor

        self.SystemButton = digitalio.DigitalInOut(SYSTEM_BUTTON)
        self.SystemButton.direction = digitalio.Direction.INPUT
        self.SystemButton.pull = digitalio.Pull.UP

        self.state = {
            'Worker': 1,  # Indicates if the worker mode is enabled
            'System': 1,   # Indicates if the system KEDs are on
            'Previous_WORKER_BUTTON': 0,
            'Previous_SYSTEM_BUTTON': 0,
        }

        # Turn on the board LED to indicate that the program has started
        self.board_led.value = True

    def updateState(self):
        # Check if the buttons have been pressed since the last loop
        if self.state['Previous_WORKER_BUTTON'] != self.WorkerButton.value and self.WorkerButton.value == 0:
            # This will check for negative edges of the worker button
            self.state['Worker'] = not self.state['Worker']

        if self.state['Previous_SYSTEM_BUTTON'] != self.SystemButton.value and self.SystemButton.value == 0:
            # This will check for negative edges of the plant button
            self.state['System'] = not self.state['System']

            # When the system is turned on, the worker mode is turned on.
            # When the system is turned off, the worker mode is also turned off.
            self.state['Worker'] = self.state['System']

    def updateLEDs(self):
        # Update the LED based on the state
        if self.state['System'] == 0:
            # If the system is off, turn off all of the LEDs
            self.Leds.LEDs_off()

        # The following cases will only be applied if the system is on
        elif (self.state['Worker'] == 0):
            # If the worker mode is disabled, turn on the plant LEDs,
            self.Leds.LEDs_pink()
        else:
            # If the worker mode is enabled, turn on the worker LEDs,
            self.Leds.LEDs_white()

    def loop(self):
        while True:
            # Update the state and LEDs
            self.updateState()
            self.updateLEDs()

            # Update the previous button values
            self.state['Previous_WORKER_BUTTON'] = self.WorkerButton.value
            self.state['Previous_SYSTEM_BUTTON'] = self.SystemButton.value

            time.sleep(0.5)


# Initialize the controller instance
controller = BOARD_CONTROLLER()

# Run the loop
controller.loop()
