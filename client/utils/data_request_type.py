from enum import Enum

class DataRequestType(Enum):
    """ Enum that represents the type of data request that is sent. """

    HEAD = 0 # sent to signify beginning of data transfer
    NORMAL = 1 # contains actual file data
    TAIL = 2 # sent to signify end of data transfer