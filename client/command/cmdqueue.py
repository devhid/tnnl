# system imports
from queue import Queue

class CommandQueue:
    """ A class to handle the processing of all commands sent by the server. """

    def __init__(self):
        self.queue = Queue()
    
    def enqueue(self, command):
        self.queue.put(command)
    
    def dequeue(self):
        command = None
        try:
            command = self.queue.get()
        except Queue.Empty:
            return None
        
        return command
    
    def process(self):
        