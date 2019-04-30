# system imports
import time

# internal imports
from command.cmdqueue import CommandQueue
from command.cmdparser import CommandParser
from command.command import Command

class Sniffer:

    def __init__(self, interface, packet_filter):
        self.interface = interface
        self.filter = packet_filter

        self.stopped = False

        self.queue = CommandQueue()
        self.parser = CommandParser()
    
    def start():
        thread = Thread(target = self._sniff)
        thread.daemon = True
        thread.start()

        time.sleep(1) # add delay to prevent resource lock (might not be needed)

        while not stopped:
            self.queue.process()
    
    def _process_packet(self, pkt):
        cmd = parser.parse(pkt)
        if cmd != None:
            self.queue.enqueue(Command(pkt))

    def _sniff(self):
        global stopped
        sniff(iface=self.interface, filter=self.packet_filter, store=0, prn=self._process_packet)
        stopped = True
