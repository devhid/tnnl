from enum import IntEnum

class RequestType(IntEnum):
    
    PING = 5, # CNAME
    DATA = 1, # A
    RECPT = 16 # TXT