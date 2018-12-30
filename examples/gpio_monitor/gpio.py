"""
This module manage GPIO interaction.

We use RPi.GPIO (https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/) instead
of gpiozero (https://gpiozero.readthedocs.io/en/stable/) as we have low level access
"""
from threading import RLock
import RPi.GPIO as GPIO


# We define some global variable to share information
#  - GPIOS_LOCK: a thread locker
#  - GPIO_CURRENT_STATE: to store current state of GPIO
#  - GPIO_HISTORY: last "WINDOW_SIZE" GPIO state
#  - WINDOW_SIZE: number of event we will store
GPIOS_LOCK = RLock()
GPIOS_CURRENT_STATE = dict()
GPIOS_HISTORY = dict()
GPIOS_WINDOW_SIZE = 1000


class GPIOMonitoring():
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
        print('Initialize gpio {}'.format(self.channel))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.IN)

    def __del__(self):
        """
        Clear all GPIO monitoring
        """
        print('Destroy gpio {}'.format(self.channel))
        GPIO.remove_event_detect(self.channel)
        GPIO.cleanup(self.channel)

    def monitor(self):
        """
        Monitor will return the current value of channel when it will change
        """
        print('Add event detection for gpio {}'.format(self.channel))
        GPIO.add_event_detect(self.channel, GPIO.BOTH)
        GPIO.add_event_callback(self.channel, self.state)

    def state(self):
        """
        Monitor will return the current value of channel when it will change
        :return: GPIO status
        """
        print('gpio {} state is {}'.format(self.channel, GPIO.input(self.channel)))
        return GPIO.input(self.channel)


class GPIOSMonitoring():
    """
    We store information about all GPIOS we want to monitor
    """
    def __init__(self, channels):
        """
        Initialize GPIOS
        """
        self.channels = list()
        for channel in channels:
            self.channels.append(GPIOMonitoring(channel))

    def __del__(self):
        for channel in self.channels:
            channel.__del__()
