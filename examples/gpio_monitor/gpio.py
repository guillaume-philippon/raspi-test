"""
This module manage GPIO interaction
"""
# We use RPi.GPIO (https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/) instead
# of gpiozero (https://gpiozero.readthedocs.io/en/stable/) as we have low level access
import RPi.GPIO as GPIO

class Gpio:
    """
    Gpio class will manage interaction between GPIO and the rest of the code
    """
    def __init__(self, channel):
        """
        :desc: init function prepare GPIO to be monitor
        :channel: pin number we will monitor
        """
        self.channel = channel
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.gpio_function(self.channel))

    def monitor(self):
        """
        :desc: monitor will return the current value of channel when it will change
        """
        GPIO.wait_for_edge(self.channel, GPIO.BOTH)
        return GPIO.input(self.channel)
