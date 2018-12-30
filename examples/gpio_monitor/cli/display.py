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
        plt.legend()

    def draw(self):
        """
        """
        with GPIOS_LOCK:
            for channel in GPIOS_CURRENT_STATE:
                self.axe.plot(GPIOS_HISTORY[channel], label=channel)
        image = animation.FuncAnimation(self.figure,
                                        self.redraw,
                                        interval=1000,
                                        blit=True)
        plt.show()

    @staticmethod
    def redraw(frame):
        """

        :param frame:
        :return:
        """
        output = ()
        with GPIOS_LOCK:
            for channel in GPIOS_CURRENT_STATE:
                GPIOS_HISTORY[channel].appendleft(GPIOS_CURRENT_STATE[channel])
                GPIOS_HISTORY[channel].pop()
                output = output + ()
        return output

# def plot():
#     """
#     We will use matplotlib w/ animation to render the output. As I m not confident w/
#     matplotblib that part could be not easly readeable.
#     """
#     figure = plt.figure()
#     plots = dict()
#     axe = figure.add_subplot(111)
#     axe.set_ylim(-0.1, 1.1)
#     with LOCK:
#         for gpio in GPIO_CURRENT_STATE:
#             plots[gpio], = axe.plot(GPIO_HISTORY[gpio], label=gpio)
#     plt.legend()
#     ani = animation.FuncAnimation(figure, plot_update,  # pylint: disable=unused-variable
#                                   fargs=(plots,),
#                                   interval=1000, blit=True)
#     plt.show()
#
#
# def plot_update(frame, plots):  # pylint: disable=unused-argument
#     """
#     Handler to update plot
#     """
#     ret = ()
#     with LOCK:
#         for gpio in GPIO_CURRENT_STATE:
#             print(plots)
#             GPIO_HISTORY[gpio].appendleft(GPIO_CURRENT_STATE[gpio])
#             GPIO_HISTORY[gpio].pop()
#             plots[gpio].set_ydata(GPIO_HISTORY[gpio])
#             ret = ret + (plots[gpio],)
#     return ret
