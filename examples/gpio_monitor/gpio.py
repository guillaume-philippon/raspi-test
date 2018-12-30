"""
This module manage GPIO interaction.

We use RPi.GPIO (https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/) instead
of gpiozero (https://gpiozero.readthedocs.io/en/stable/) as we have low level access
"""
import RPi.GPIO as GPIO


class Gpio:
    """
    Gpio class will manage interaction between GPIO and the rest of the code
    """
    def __init__(self, channel):
        """
        Initialize GPIO to be monitor
        :param: channel: pin number we will monitor
        :return:
        """
        self.channel = channel
        self.name = 'gpio{}'.format(self.channel)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.IN)

    def __del__(self):
        """
        Clear all GPIO monitoring
        """
        GPIO.remove_event_detect(self.channel)
        GPIO.cleanup(self.channel)

    def monitor(self):
        """
        Monitor will return the current value of channel when it will change
        """
        GPIO.add_event_detect(self.channel, GPIO.BOTH)
        GPIO.add_event_callback(self.channel, self.state)

    def state(self):
        """
        Monitor will return the current value of channel when it will change
        :return: GPIO status
        """
        return GPIO.input(self.channel)
