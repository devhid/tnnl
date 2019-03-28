from enum import Enum

class RequestType(Enum):
    """ Enum that represents the type of request that is sent. """

    PING = 0, # sent periodically to check if the server has a command
    DATA = 1, # any data requested from the execution of the command sent by the server
    RECEIPT = 2 # a receipt of the success (or failure) of the execution of a command