class Command:
    """ A class for handling the command sent by the C&C server. """

    def __init__(self, encoded_command):
        self.cmd = encrypted_command
    
    def decode(self):
        """ Decodes the encoded command into a bash command. """
        pass
    
    def execute(self):
        """ Executes the command in a bash environment . """
        pass