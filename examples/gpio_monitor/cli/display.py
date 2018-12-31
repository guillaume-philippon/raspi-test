"""
This module will define Display class that will be used to
display output on screen.

To follow monitoring, we will use matplotlib w/ animation (see
https://matplotlib.org/gallery/index.html)
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from gpio_monitor.gpio import GPIOS_LOCK, GPIOS_CURRENT_STATE, GPIOS_HISTORY


class Display():
    """
    This class will create a matplotlib graph animated
    """
    def __init__(self):
        """
        Initialize display class. We will create
          - figure
          - axe through -0.02 and 1.02. In fact we want a axe from 0 to 1 but we add
          some padding. Perhaps there are some other way
          - a dict of line that will store plot for each channel
        """
        figure, axe = plt.subplots()
        axe.set_ylim(-0.02, 1.02)
        self.figure = figure
        self.axe = axe
        self.line = dict()
        plt.legend()

    def draw(self):
        """
        Will start animation and render the plot
        We create a plot dict from GPIOS_HISTORY *and* GPIOS_CURRENT_STATE.

        For those not very confident w/ python
        - self.line[channel], = means self.line[channel] will contains the value of
        the *one element tuple* return by self.axe.plot.

        Per example:
        >>foo = (1)  # foo is a tuple w/ one element
        >>bar, = foo
        >>print(bar)
        1

        For those not very confident w/ matplotlib
        animation.FuncAnimation must be store into a variable name, if not the figure
        will not be displayed.
        - First argument will be the figure itself
        - Second argument will be the callback function. callback function will be
        call w/ a argument which is the frame current number (see doc to add argument
        to callback function)
        - interval is the time (ms) between to redraw
        - blit tell animation to redraw only the graph, not the background
        """
        with GPIOS_LOCK:
            for channel in GPIOS_CURRENT_STATE:
                self.line[channel], = self.axe.plot(GPIOS_HISTORY[channel], label=channel)
                self.axe.legend()
        image = animation.FuncAnimation(self.figure,  # pylint: disable=unused-variable
                                        self.redraw,
                                        interval=1000,
                                        blit=True)
        plt.show()

    def redraw(self, frame):  # pylint: disable=unused-argument
        """
        Even if frame argument is not use, we must add it as it's automaticaly added
        by FuncAnimation
        :param frame: frame current value
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
