"""
This module will define Display class that will be used to
display output on screen
"""
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from gpio_monitor.gpio import GPIOS_LOCK, GPIOS_CURRENT_STATE, GPIOS_HISTORY


class Display():
    """
    This class will create a matplotlib graph animated
    """
    def __init__(self, channels):
        """
        Initialize display class
        """
        figure, axe = plt.subplots()
        axe.set_ylim(-0.02, 1.02)
        self.figure = figure
        self.axe = axe
        self.line = dict()
        plt.legend()

    def draw(self):
        """
        """
        with GPIOS_LOCK:
            for channel in GPIOS_CURRENT_STATE:
                self.line[channel], = self.axe.plot(GPIOS_HISTORY[channel], label=channel)
                self.axe.legend()
        image = animation.FuncAnimation(self.figure,
                                        self.redraw,
                                        interval=1000,
                                        blit=True)
        plt.show()

    def redraw(self, frame):
        """

        :param frame:
        :return:
        """
        output = ()
        with GPIOS_LOCK:
            for channel in GPIOS_CURRENT_STATE:
                GPIOS_HISTORY[channel].appendleft(GPIOS_CURRENT_STATE[channel])
                GPIOS_HISTORY[channel].pop()
                self.line[channel].set_ydata(GPIOS_HISTORY[channel])
                output = output + (self.line[channel], )
        return output
