import argparse
import os

# from scapy.all import *
from sys import argv, exit
from utils.consts import *
from configs import config

class TnnlServer():

    def __init__(self, path = DEFAULT_CONFIG_PATH):
        
        self.server_conf = config.load_configs(path, CONFIG_SERVER, CONFIG_SERVER_KEYS) if path != None else default_server_conf()

        self.client_conf = config.load_configs(path, CONFIG_CLIENT, CONFIG_CLIENT_KEYS) if path != None else default_client_conf()

        print(self.server_conf)
        print(self.client_conf)

def arg_parse():
    parser = argparse.ArgumentParser(
        description = 'tnnl-server',
        epilog = '0.0.1'
    )

    parser.add_argument('-c', metavar = '', required = False, help = HELP_CONFIG_PATH)

    args = parser.parse_args()

    if len(argv) < 1:
        parser.print_help()
        exit(1)

    return args

def main():
    args = arg_parse()
    tnnl = TnnlServer(args.c)

if __name__ == '__main__':
    main()