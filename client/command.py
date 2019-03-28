class Command:
    """ A class for handling the command sent by the C&C server. """

    def __init__(self, encoded_command):
        self.cmd = encoded_command
    
    def decode(self):
        """ Decodes the encoded command into a shell command. """
        pass
    
    def execute(self):
        """ Executes the command in a shell environment . """
        pass