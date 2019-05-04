import secrets
import time

from collections import deque
from scapy.all import *
from utils.consts import log

class CommandQueue():

    def __init__(self, interface, config):
        self.queue = deque()
        self.interface = interface
        self.config = config

        # TODO: Possible try block needed
        self.socket = conf.L2socket(iface = interface)

    def enqueue(self, command_pkt):
        log('CommandQueue', 'enqueue', 'Added to queue')
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
            log('CommandQueue', 'process', 'Processing packet')

            # Randomize packet transfer interval
            low = int(self.config.delay_time) - int(self.config.delay_time_offset)
            high = int(self.config.delay_time) + int(self.config.delay_time_offset)
            timeout = secrets.choice(range(low, high))
            log('CommandQueue', 'process', 'Timeout ({})'.format(timeout))

            time.sleep(timeout)

            print(command_pkt.show())

            if command_pkt == None:
                return
        
            # Send the packet that was built
            sendp(command_pkt, iface = self.interface)
            # self.socket.sendp(command_pkt)
