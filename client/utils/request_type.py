from enum import Enum

class RequestType(Enum):
    """ Enum that represents the type of request that is sent. """

    PING = 5 # sent periodically to check if the server has a command
    DATA = 1 # sent when a file retrieval command is issued for transmission of data
    RECEIPT = 16 # a receipt of the success (or failure) of the execution of a shell command