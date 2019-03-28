import argparse
import os

from scapy.all import *
from sys import argv, exit

class TnnlServer():

    def __init__(self, interface = DEFAULT_INTERFACE, config = DEFAULT_CONFIG_PATH):
        self.interface = interface


def arg_parse():
    parser = argparse.ArgumentParser(
        description = 'tnnl-server',
        epilog = '0.0.1'
    )

    parser.add_argument('-i', metavar = '', required = False, help = HELP_INTERFACE)
    parser.add_argument('-c', metavar = '', required = False, help = HELP_CONFIG_PATH)

    args = parser.parse_args()

    if len(args) < 1:
        parser.print_help()
        exit(1)

    return args

def main():
    args = arg_parse()

if __name__ == '__main__':
    main()