class DataRequest:
    """ A data request sends actual file data via the subdomains in an A record. """

    def __init__(self, _type, packet_number):
        self.type = _type
        self.packet_number = packet_number
    
    def build()