"""
This module will define Display class that will be used to
display output on screen
"""
from collections import deque
from threading import Thread, RLock
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Some global variable
LOCK = RLock() # A lock to control Thread acces to variables
GPIO_CURRENT_STATE = dict() # Current value for GPIO
GPIO_HISTORY = dict() # Historic value for GPIO
WINDOW_SIZE = 400 # Number of even we will keep

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
        with LOCK:
            GPIO_CURRENT_STATE[gpio.name] = self.gpio.state()
            GPIO_HISTORY[gpio.name] = deque([GPIO_CURRENT_STATE[gpio.name]] * WINDOW_SIZE)
        print("initial value for {}: {}".format(self.gpio.name, self.gpio.state()))

    def run(self):
        """
        run method is the method that will be started when we launch a thread
        """
        while True:
            value = self.gpio.monitor()
            with LOCK:
                GPIO_CURRENT_STATE[self.gpio.name] = value
                print("new value for {}: {}".format(self.gpio.name, value))

def plot():
    """
    We will use matplotlib w/ animation to render the output. As I m not confident w/
    matplotblib that part could be not easly readeable.
    """
    figure = plt.figure()
    plots = dict()
    axe = figure.add_subplot(111)
    axe.set_ylim(-0.1, 1.1)
    with LOCK:
        for gpio in GPIO_CURRENT_STATE:
            plots[gpio], = axe.plot(GPIO_HISTORY[gpio], label=gpio)
    plt.legend()
    ani = animation.FuncAnimation(figure, plot_update, fargs=(plots,), # pylint: disable=unused-variable
                                  interval=1000, blit=True)
    plt.show()

def plot_update(frame, plots): # pylint: disable=unused-argument
    """
    Handler to update plot
    """
    ret = ()
    with LOCK:
        for gpio in GPIO_CURRENT_STATE:
            print(plots)
            GPIO_HISTORY[gpio].appendleft(GPIO_CURRENT_STATE[gpio])
            GPIO_HISTORY[gpio].pop()
            plots[gpio].set_ydata(GPIO_HISTORY[gpio])
            ret = ret + (plots[gpio],)
    return ret
