"""
This module will manage Command Line Interface (CLI) for gpio-monitor.
It will parse argument and build a configuration reference for gpio-monitor.

For more information about argparse, see https://docs.python.org/3/library/argparse.html
"""
import argparse


class Config:  # pylint: disable=too-few-public-methods
    """
    Config class will be use to store configuration give by user
    """
    def __init__(self):
        """
        initialise class
        """
        # We build argument parser
        # Usage: $0 GPIO ...
        parser = argparse.ArgumentParser(description='monitor some GPIO from Rasberry Pi')
        parser.add_argument('gpio', metavar='GPIO', type=int, nargs='+',
                            help='list of GPIO we want monitor')
        options = parser.parse_args()

        # We build a dict of options. By default, there are only gpio but we can add some
        # option later
        self.config = {
            'gpio': list()
            }
        for gpio in options.gpio:
            self.config['gpio'].append(gpio)

    def display(self):
        """
        display current configuration
        """
        for item in self.config:
            print('Configuration items')
            print('{}: {}'.format(item, self.config[item]))
