"""Process a given packet
"""
from scapy.all import *
from utils.request_type import *

class DataReceiver():

    def __init__(self):
        pass

    def parse(self, pkt):
        # Check qtype field to delineate type of given packet
        if pkt.getlayer(DNSQR).qtype == PING:
            self._receive_ping(pkt)
        elif pkt.getlayer(DNSQR).qtype == DATA:
            self._receive_data(pkt)
        elif pkt.getlayer(DNSQR).qtype == RECPT:
            self._receive_recpt(pkt)

    def _receive_ping(self, pkt):
        pass

    def _receive_data(self, pkt):
        pass

    def _receive_recpt(self, pkt):
        pass