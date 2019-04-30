"""Sniff inbound requests to the server
"""
from scapy.all import *
from datarecv import DataReceiver

class Sniffer():

    def __init__(self, interface, packet_filter):
        self.interface = interface
        self.bpf = 'udp' + (f' and {packet_filter}' if len(packet_filter) > 0 else '') # Setup filter to automatically filter for UDP
        self.parser = DataReceiver()

    def start(self):
        thread = Thread(target = self._receive)
        thread.daemon = True
        thread.start()

        time.sleep(1)

    def _sniff(self):
        sniff(iface=self.interface, filter=self.bpf, store=False, prn=self._process_pkt)

    def _process_pkt(self, pkt):
        # Perform associated actions for type of packet
        self.parser.parse(pkt)
