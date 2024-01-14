'''
ESC204 2024S Prototyping Assignment
'''
# Import libraries needed for blinking the LED
import board
import digitalio

class Controller:
    def __init__(self):
        self.led = digitalio.DigitalInOut(board.GP16)
        self.led.direction = digitalio.Direction.OUTPUT
        self.button = digitalio.DigitalInOut(board.GP15)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP # Set internal pull-up resistor
        self.led.value = 0

    def run(self):
        while True:
            self.led.value = not self.button.value #light up if button is pressed

# Configure the GPIO pin connected to the LED as a digital output
led = digitalio.DigitalInOut(board.GP16)
led.direction = digitalio.Direction.OUTPUT
# Configure the GPIO pin connected to the button as a digital input
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP # Set internal pull-up resistor
# Print a message on the serial console
print('Hello! My LED is controlled by the button.')
# Loop so the code runs continuously
while True:
led.value = not button.value #light up if button is pressed
