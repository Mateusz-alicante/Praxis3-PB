import board
import digitalio

LED_RED = board.GP17
LED_BLUE = board.GP18 #PIN TBD
LED_GREEN = board.GP19 #PIN TBD

WORKER_BUTTON = board.GP20
SYSTEM_BUTTON = board.GP21


class Controller:
    def __init__(self):
        # Initialize the LEDs
        self.LedRED = digitalio.DigitalInOut(LED_RED)
        self.LedRED.direction = digitalio.Direction.OUTPUT
        self.LedGREEN = digitalio.DigitalInOut(LED_GREEN)
        self.LedGREEN.direction = digitalio.Direction.OUTPUT
        self.LedBLUE = digitalio.DigitalInOut(LED_BLUE)
        self.LedBLUE.direction = digitalio.Direction.OUTPUT

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
            'Worker': 1,
            'System': 1,
            'Previous_WORKER_BUTTON': 0,
            'Previous_SYSTEM_BUTTON': 0,
        }

        # Turn on the board LED to indicate that the program has started
        self.board_led.value = True

    def updateState(self):
        # Check if the buttons have been pressed since the last loop
        if self.state['Previous_WORKER_BUTTON'] != self.WorkerButton.value and self.WorkerButton.value == 0:
            # This will check for negative edges of the worker button (when the button is pressed)
            self.state['Worker'] = not self.state['Worker']

        if self.state['Previous_SYSTEM_BUTTON'] != self.SystemButton.value and self.SystemButton.value == 0:
            # This will check for negative edges of the plant button (when the button is pressed)
            self.state['System'] = not self.state['System']

            # When the system is turned on, for the convenience of the user, the worker mode is also turned on
            if self.state['System'] == 1:
                self.state['Worker'] = 1

    def updateLEDs(self):
        # Update the LED based on the state
        if self.state['System'] == 0:
            # If the system is off, turn off all of the LEDs
            self.LedRED.value = False
            self.LedBLUE.value = False
            self.LedGREEN.value = False

        # The following cases will only be applied if the system is on
        elif (self.state['Worker'] == 0):
            # If the worker mode is disabled, turn on the plants LED, i.e red and blue
            self.LedRED.value = True
            self.LedGREEN.value = False
            self.LedBLUE.value = True

        else:
            # If the worker mode is enabled, turn on all LEDs to form white light
            self.LedRED.value = True
            self.LedGREEN.value = True
            self.LedBLUE.value = True

    def loop(self):
        while True:
            # Update the state and LEDs
            self.updateState()
            self.updateLEDs()

            # Update the previous button values
            self.state['Previous_WORKER_BUTTON'] = self.WorkerButton.value
            self.state['Previous_SYSTEM_BUTTON'] = self.SystemButton.value


controller = Controller()
controller.loop()
