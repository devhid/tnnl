from collections import deque
from scapy.all import *

class CommandQueue():

    def __init__(self, interface):
        self.queue = deque()
        self.interface = interface

        # TODO: Possible try block needed
        self.socket = conf.L2socket(iface = interface)

    def enqueue(self, command_pkt):
        self.queue.append(command_pkt)

    def dequeue(self):
        command_pkt = None
        try:
            command_pkt = self.queue.popleft()
        except Exception:
            return None

        return command_pkt

    def process(self):
        if self.queue:
            command_pkt = self.dequeue()
            print('sending packet')

            if command_pkt == None:
                return
        
            # Send the packet that was built
            # sendp(command_pkt, iface = self.interface)
            self.socket.send(command_pkt)
