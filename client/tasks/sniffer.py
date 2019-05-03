# system imports
import time
from threading import Thread

# library imports
from scapy.all import sniff

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
    
    def start(self):
        print("[Sniffer] Started")
        thread = Thread(target = self._sniff)
        thread.daemon = True
        thread.start()

        time.sleep(1) # add delay to prevent resource lock (might not be needed)

        while not self.stopped:
            print("[Sniffer] Processing...")
            self.queue.process()
            time.sleep(2) # sleep so queue has time to process
    
    def _process_packet(self, pkt):
        cmd = self.parser.parse(pkt)
        if cmd != None:
            self.queue.enqueue(Command(pkt))

    def _sniff(self):
        sniff(iface=self.interface, filter=self.filter, store=0, prn=self._process_packet)
        self.stopped = True
