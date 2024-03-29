"""Sniff inbound requests to the server
"""
from scapy.all import *
from datarecv import DataReceiver
from command.cmdqueue import CommandQueue
from utils.consts import log

class Sniffer():

    def __init__(self, interface, packet_filter, rel_path, cmd_file, config):
        self.interface = interface
        self.bpf = packet_filter
        self.config = config

        # Receive packets
        self.queue = CommandQueue(self.interface, self.config)
        self.parser = DataReceiver(rel_path, cmd_file, self.queue, self.config)
        self.stopped = False

    def start(self):
        thread = Thread(target = self._sniff)
        thread.daemon = True
        thread.start()

        time.sleep(1)

        # Process packets in queue
        while not self.stopped:
            self.queue.process()
            # time.sleep(2)

    def _sniff(self):
        sniff(iface=self.interface, filter=self.bpf, store=False, prn=self._process_pkt)

    def _process_pkt(self, pkt):
        # Perform associated actions for type of packet
        self.parser.parse(pkt)
