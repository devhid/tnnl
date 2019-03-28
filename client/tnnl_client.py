# library imports
from twisted.internet import reactor, task

# internal imports
from config import PING_INTERVAL
from request import Request
from command import Command
from request_type import RequestType

def main():
    pass

def read_command(response):
    """ Returns the encoded command from a DNS response. """
    pass

def schedule_ping():
    """ Sends a ping request to the server in an interval. """
    def ping():
        request = Request(RequestType.PING)
        request.send()

    ping_task = task.LoopingCall(ping)
    ping_task.start(PING_INTERVAL)

    reactor.run()

if __name__ == "__main__":
    main()