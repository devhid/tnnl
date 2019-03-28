from enum import Enum

class RequestType(Enum):
    
    PING = 0,
    DATA = 1,
    RECEIPT = 2