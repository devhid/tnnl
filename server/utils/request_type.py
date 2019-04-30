from enum import Enum

class RequestType(Enum):
    
    PING = 'TXT',
    DATA = 'A',
    RECEIPT = 'CNAME'