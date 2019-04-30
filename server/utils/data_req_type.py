from enum import Enum

class DataRequestType(Enum):

    HEAD = 0, # Head of file transfer
    NORMAL = 1, # Regular packet in middle of file transfer
    TAIL = 2 # End of file transfer