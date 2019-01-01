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
        parser = argparse.ArgumentParser(description='monitor some GPIO from Rasberry Pi')
        parser.add_argument('--led', metavar='led', type=int,
                            help='led pin number')
        parser.add_argument('--button', metavar='button', type=int,
                            help='button pin number')
        options = parser.parse_args()

        self.config = {
            'led': options.led,
            'button': options.button
            }

    def display(self):
        """
        display current configuration
        """
        for item in self.config:
            print('Configuration items')
            print('{}: {}'.format(item, self.config[item]))
