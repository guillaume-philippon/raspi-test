"""
This module will define Display class that will be used to
display output on screen
"""
from threading import Thread, RLock
import time

LOCK = RLock()

class Display(Thread):
    """
    :desc: Display is a sub-class of Thread. It will monitor one specific pin (channel)
    """
    def __init__(self, gpio):
        """
        Initialise output
        """
        Thread.__init__(self)
        self.gpio = gpio
        print('Init thread gpio({})'.format(gpio.channel))

    def run(self):
        """
        run method is the method that will be started when we launch a thread
        """
        channel = self.gpio.channel
        value = self.gpio.monitor()
        with LOCK:
            print('{} {} {}'.format(time.time(), channel, value))
        