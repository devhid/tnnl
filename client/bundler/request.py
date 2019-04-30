# from scapy.all import DNS, DNSQR

# internal imports
from constants import REQUEST_TYPE_ERR
from request_type import RequestType

class Request:
    """ A class for the DNS request that is sent to the C&C server holding information / receipt. """

    def __init__(self, request_type):
        # type = (PING, DATA, RECEIPT)
        self.type = request_type
    
    def send(self):
        """ Main function that sends a request based on its type. """
        if self.request.type == RequestType.PING: _send_ping(self)
        elif self.request.type == RequestType.DATA: _send_data(self)
        elif self.request.type == RequestType.RECEIPT: _send_receipt(self)
        else: raise Exception(REQUEST_TYPE_ERR)
    
    def _send_ping(self):
        """ Helper function to send a ping request. """
        pass
    
    def _send_data(self):
        """ Helper function to send a data request. """
        pass
    
    def _send_receipt(self):
        """ Helper function to send a receipt request. """
        pass
