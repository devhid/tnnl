import time

from command.cmdparser import CommandParser
from threading import Thread

class CommandTask():

    def __init__(self, directory, cmd_file):
        self.can_watch = True
        self.cmdparser = CommandParser(directory, cmd_file)
    
    def start(self):
        thread = Thread(target = self._parse)
        thread.daemon = True
        thread.start()

        time.sleep(1)


    def _parse(self):
        if self.can_watch:
            self.cmdparser.parse()