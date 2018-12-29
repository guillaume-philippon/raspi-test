#!/usr/bin/env python3
"""
gpio-monitor is a program that will wait and display GPIO status when it change. The goal is
learning how to manipulate gpio through python3.

We will use some basic python module to have more versatility (as argparse) but we will embeded
it on sub-module so it will not interfer with basic GPIO command.
"""
from gpio_monitor.cli import config, display
from gpio_monitor.gpio import Gpio

CONFIG = config.Config()
gpios = list()
for gpio in CONFIG.config['gpio']:
    gpios.append(Gpio(gpio))

displays = list()
for gpio in gpios:
    displays.append(display.Display(gpio))

for thread in displays:
    thread.start()
for thread in displays:
    thread.join()
