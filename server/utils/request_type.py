from enum import IntEnum

class RequestType(IntEnum):
    
    PING = 16, # TXT
    DATA = 1, # A
    RECPT = 5 # CNAME