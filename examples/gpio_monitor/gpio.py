"""
This module manage GPIO interaction.

We use RPi.GPIO (https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/) instead
of gpiozero (https://gpiozero.readthedocs.io/en/stable/) as we have low level access
"""
from collections import deque
from threading import RLock
import RPi.GPIO as GPIO  # pylint: disable=import-error


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
        To monitor GPIO, we need to setup GPIO in ingress mode (GPIO.IN), after
        that, it can be changed to egress (GPIO.OUT) but it can't be initialize
        at GPIO.OUT.

        We also use BCM notation (see: https://fr.pinout.xyz/pinout/pin29_gpio5)
        instead of physical notation as BCM is used by sysfs and it will be easiest
        to test code with commands:
        pi@raspi:~$ cd /sys/class/gpio
        pi@raspi:gpio$ echo out > gpio*id*/direction
        pi@raspi:gpio$ echo 1 > gpio*id*/value
        pi@raspi:gpio$ sleep 20
        pi@raspi:gpio$ echo 0 > gpio*id*/value

        where *id* is the channe we monitor.
        """
        self.channel = channel
        self.name = 'gpio{}'.format(self.channel)
        print('Initialize gpio {}'.format(self.channel))
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.channel, GPIO.IN)
        with GPIOS_LOCK:
            GPIOS_CURRENT_STATE[self.name] = self.state()
            GPIOS_HISTORY[self.name] = deque([GPIOS_CURRENT_STATE[self.name]] * GPIOS_WINDOW_SIZE)
            print('GPIOS_CURRENT_STATE: {}'.format(GPIOS_CURRENT_STATE))
            print('GPIOS_HISTORY: {}'.format(GPIOS_HISTORY))
        self.monitor()

    def __del__(self):
        """
        Clear all GPIO monitoring
        """
        print('Destroy gpio {}'.format(self.channel))
        GPIO.remove_event_detect(self.channel)
        GPIO.cleanup(self.channel)

    def monitor(self):
        """
        Monitor will return the current value of channel when it will change.

        add_event_detect will create a thread to follow GPIO status modification,
        GPIO_BOTH means that RISING *and* FAILING will trig thread
        add_event_callback is (or are) function(s) called when a event is detected,
        the callback will be call with *channel* as argument
        """
        print('Add event detection for gpio {}'.format(self.channel))
        GPIO.add_event_detect(self.channel, GPIO.BOTH)
        GPIO.add_event_callback(self.channel, self.state)

    def state(self, channel=None):
        """
        We will modify GPIOS_CURRENT_STATE. As this variable will also be modify by
        callback thread we need to lock access before writing in it.
        :return: GPIO status
        """
        with GPIOS_LOCK:
            GPIOS_CURRENT_STATE[self.name] = GPIO.input(self.channel)
        print('gpio {} state is {}'.format(self.channel, GPIO.input(self.channel)))
        return GPIO.input(self.channel)


class GPIOSMonitoring():  # pylint: disable=too-few-public-methods
    """
    We store information about all GPIOS we want to monitor
    """
    def __init__(self, channels):
        """
        Initialize GPIOS
        """
        print('Initialize GPIOS')
        self.channels = list()
        for channel in channels:
            gpio = GPIOMonitoring(channel)
            self.channels.append(gpio)
