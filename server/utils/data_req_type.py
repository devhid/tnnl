from enum import IntEnum

class DataRequestType(IntEnum):

    HEAD = 0, # Head of file transfer
    NORMAL = 1, # Regular packet in middle of file transfer
    TAIL = 2 # End of file transfer