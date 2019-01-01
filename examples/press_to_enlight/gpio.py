"""
This module will manage gpio.
 - listening for press button
 - enlight or switch off the LED

We will use gpiozero module (https://gpiozero.readthedocs.io/en/stable/) to manage it
"""
from signal import pause
from gpiozero import LED, Button  # pylint: disable=import-error


class GPIO():
    """
    This is a short module to monitor press button and swith on/off LED
    """
    def __init__(self, config):
        """
        Initialisation module
        :param config: Configuration file
        :return:
        """
        self.led = LED(config['led'])
        self.button = Button(config['button'])

    def start(self):
        self.button.when_pressed = self.led.on
        self.button.when_release = self.led.off

        pause()
