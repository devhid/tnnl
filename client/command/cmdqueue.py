# system imports
from Queue import Queue

class CommandQueue:
    """ A class to handle the processing of all commands sent by the server. """

    def __init__(self):
        self.queue = Queue()
    
    def enqueue(self, command):
        """ Add a command to the queue (FIFO). """
        self.queue.put(command)
    
    def dequeue(self):
        """ Delete a command off the queue if one exists and return it (FIFO). """
        command = None
        try:
            command = self.queue.get()
        except Queue.Empty:
            return None
        
        return command
    
    def process(self):
        """ Dequeues the next command and executes it. """
        if not self.queue.empty():
            cmd = self.dequeue()
            print("got command: " + cmd)

            if cmd == None:
                return
            
            cmd.execute()
        
        else:
            print("queue is empty")

