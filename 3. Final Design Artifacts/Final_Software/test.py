'''
Course: ESC 204
Team: 0105-08
Project: Plant Monitoring System
Description: 
This file replaces imported libraries that rely on being executed on the board by 
custom objects that simulate the state of the board. Then the code written for the board 
is tested using these objects, which allows us to inspect the state of the object (which simulated
the board) at each moment.

The different test cases are designed to test edge cases for the functionality.
Test cases should start at very basic to more advanced functionality to aid debugging.
'''


class LED_CONTROLLER:
    def __init__(self):
        self.redPin = {"value": False}
        self.greenPin = {"value": False}
        self.bluePin = {"value": False}

        self.LEDs_white()

    def LEDs_off(self):
        self.redPin["value"] = False
        self.greenPin["value"] = False
        self.bluePin["value"] = False

    def LEDs_pink(self):
        self.redPin["value"] = True
        self.greenPin["value"] = False
        self.bluePin["value"] = True

    def LEDs_white(self):
        self.redPin["value"] = True
        self.greenPin["value"] = True
        self.bluePin["value"] = True


class BOARD_CONTROLLER:
    def __init__(self):
        # Initialize the LEDs
        self.Leds = LED_CONTROLLER()

        # Initialize the buttons
        self.WorkerButton = {"value": True}

        self.SystemButton = {"value": True}

        self.state = {
            'Worker': 1,  # Indicates if the worker mode is enabled
            'System': 1,   # Indicates if the system KEDs are on
            'Previous_WORKER_BUTTON': 0,
            'Previous_SYSTEM_BUTTON': 0,
        }

    def updateState(self):
        # Check if the buttons have been pressed since the last loop
        if self.state['Previous_WORKER_BUTTON'] != self.WorkerButton["value"] and self.WorkerButton["value"] == 0:
            # This will check for negative edges of the worker button (when the button is pressed)
            self.state['Worker'] = not self.state['Worker']

        if self.state['Previous_SYSTEM_BUTTON'] != self.SystemButton["value"] and self.SystemButton["value"] == 0:
            # This will check for negative edges of the plant button (when the button is pressed)
            self.state['System'] = not self.state['System']

            # When the system is turned on, for the convenience of the user, the worker mode is also turned on.
            # When the system is turned off, the worker mode is also turned off.
            # (if someone is there to turn the system on, he will appreciate the worker mode being on)
            self.state['Worker'] = self.state['System']

    def updateLEDs(self):
        # Update the LED based on the state
        if self.state['System'] == 0:
            # If the system is off, turn off all of the LEDs
            self.Leds.LEDs_off()

        # The following cases will only be applied if the system is on
        elif (self.state['Worker'] == 0):
            # If the worker mode is disabled, turn on the plant LEDs, and turn the worker LEDs to a specific colour (e.g red)
            self.Leds.LEDs_pink()
        else:
            # If the worker mode is enabled, turn on the worker LEDs, and turn on the plant LEDs
            self.Leds.LEDs_white()

    def singleLoop(self):
        # Update the state and LEDs
        self.updateState()
        self.updateLEDs()

        # Update the previous button values
        self.state['Previous_WORKER_BUTTON'] = self.WorkerButton["value"]
        self.state['Previous_SYSTEM_BUTTON'] = self.SystemButton["value"]


controller = BOARD_CONTROLLER()

# Test 1: Check that when the system is just enabled, make sure the worker mode is on
# color should be white
assert controller.state['Worker'] == 1
assert controller.state['System'] == 1
assert controller.Leds.redPin['value'] == True
assert controller.Leds.greenPin['value'] == True
assert controller.Leds.bluePin['value'] == True
print("Test 1 passed")

# Test 2: After one loop, check that the worker mode is still on
controller.__init__()
controller.singleLoop()
assert controller.state['Worker'] == 1
assert controller.state['System'] == 1
assert controller.Leds.redPin['value'] == True
assert controller.Leds.greenPin['value'] == True
assert controller.Leds.bluePin['value'] == True
print("Test 2 passed")

# Test 3: After pressing the worker button, check that the worker mode is off
controller.__init__()
controller.SystemButton['value'] = True
controller.singleLoop()
controller.WorkerButton['value'] = False
controller.singleLoop()
assert controller.state['Worker'] == 0
assert controller.state['System'] == 1
assert controller.Leds.redPin['value'] == True
assert controller.Leds.greenPin['value'] == False
assert controller.Leds.bluePin['value'] == True
print("Test 3 passed")

# Test 4: After pressing the worker button, check that the worker mode is off, check after several cycles
controller.__init__()
controller.SystemButton['value'] = True
controller.singleLoop()
controller.WorkerButton['value'] = False
controller.singleLoop()
controller.singleLoop()
controller.singleLoop()
assert controller.state['Worker'] == 0
assert controller.state['System'] == 1
assert controller.Leds.redPin['value'] == True
assert controller.Leds.greenPin['value'] == False
assert controller.Leds.bluePin['value'] == True
print("Test 4 passed")

# Test 5: After pressing the system button, check that the worker mode is on
controller.__init__()
controller.SystemButton['value'] = True
controller.singleLoop()
controller.WorkerButton['value'] = False
controller.singleLoop()
controller.singleLoop()
controller.WorkerButton['value'] = True
controller.singleLoop()
controller.singleLoop()
assert controller.state['Worker'] == 0
assert controller.state['System'] == 1
assert controller.Leds.redPin['value'] == True
assert controller.Leds.greenPin['value'] == False
assert controller.Leds.bluePin['value'] == True
print("Test 5 passed")

# Test 6: When the system off button is pressed, check that the system turns off
controller.__init__()
controller.SystemButton['value'] = True
controller.singleLoop()
controller.SystemButton['value'] = False
controller.singleLoop()
controller.SystemButton['value'] = True
controller.singleLoop()
print(controller.state)
assert controller.state['Worker'] == 0
assert controller.state['System'] == 0
assert controller.Leds.redPin['value'] == False
assert controller.Leds.greenPin['value'] == False
assert controller.Leds.bluePin['value'] == False
print("Test 6 passed")

# Test 7: When the system button is pressed twice, turn off and then turn on, check that the worker mode still enables.
controller.__init__()
controller.SystemButton['value'] = True
controller.singleLoop()
controller.SystemButton['value'] = False
controller.singleLoop()
controller.SystemButton['value'] = True
controller.singleLoop()
controller.SystemButton['value'] = False
controller.singleLoop()
controller.SystemButton['value'] = True
controller.singleLoop()
controller.singleLoop()
assert controller.state['Worker'] == 1
assert controller.state['System'] == 1
assert controller.Leds.redPin['value'] == True
assert controller.Leds.greenPin['value'] == True
assert controller.Leds.bluePin['value'] == True
print("Test 7 passed")
