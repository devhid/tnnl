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

   * The client can send three types of DNS requests to the server, **PING**, **DATA**, and **RECEIPT**.

     ```python
     from enum import Enum
     
     class RequestType(Enum):
         """ Enum that represents the type of request that is sent. """
     
         PING = 0, # sent periodically to check if the server has a command
         DATA = 1, # sent when a file retrieval command is issued for transmission of data
         RECEIPT = 2 # a receipt of the success (or failure) of the execution of a shell command
     ```

   * The client would first send a **PING** request to the server for a response. If the response contains a command, the client executes it and sends the result of that execution back to the server.

   * The result will be dependent on the type of command issued. 

     * The **shell** command would just be executed in a shell environment and the result would just be the status code of that command. This result would be sent as a **RECEIPT** request in order to let the server know whether the command succeeded or failed.
     * The **file retrieval** command would open the file specified, read and encrypt the maximum number of bytes that can fit inside a DNS request, and send it to the server as a **DATA** request.
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

     

### Handling Multiple Commands

* It is possible that as the client is sending **DATA** requests to the server, the server sends a response back with another command. In order to ensure that all commands are properly performed by the client, the client will push all commands received by the server into a queue.

  

### DNS Request Type Identification

* The server will need to know what type of DNS request the client will be sending. In order to identify the three different types, **PING**, **DATA**, and **RECEIPT**, we can use the `qtype` field in the `Question Record` in a DNS packet.

  * **PING**: `qtype = "A"`

  * **DATA**: `qtype = "TXT"`

  * **RECEIPT**: `qtype = "CNAME"`

    

### Data Encryption

* The strong encryption methods that are normally used today do not preserve the length of the original message.

* While this offers more security, the longer length of the encrypted message reduces the amount of data we can pack into one DNS request.

* To work around this, we will be using ***Format Preserving Encryption (FPE)*** which will encrypt our data without changing the original length.

  * This encryption algorithm is performed via a "*Feistel-based mode of operation*".
  * You can read more about it here: <https://csrc.nist.gov/csrc/media/projects/block-cipher-techniques/documents/bcm/proposed-modes/ffx/ffx-spec2.pdf>

* To use this encryption method in our program, we will be using a library called **pyffx**.

  

### Embedding Data into a DNS Request

* In order for the client to send the actual data requested by the server, the client will include it in the subdomains of a hostname specified in the `qname` field of a `Question Record`.
* A domain has a maximum length of `255` characters and each subdomain has a maximum length of `63` characters.
* The client needs to also identify itself to the server since the server will be sending commands to multiple victim machines. 
  * To identify the client, the beginning subdomain will be set to the client machine's **MAC** address since it is a **static address**.
  * A **MAC** address only takes up exactly `12` characters.
* The maximum number of bytes for the data we can include in the request will be  `num_chars(domain) - 12 - num_chars(periods)`.
  * The `num_chars(periods)` represents the periods in the full hostname (e.g. `<mac_address>.<data1>.<data2>.<domain>` has `3` periods).
  * In general: `num_chars(periods) = num(subdomains_for_data) + 1 `



### Ensuring Packet Completeness

* The server needs to know when it has fully received all the data it has requested from the client.

* To find out, there will be three types of **DATA** requests that will be sent during the transmission of data.

  1. `HEAD`
     * A `HEAD` request will signify the start of data transmission and will be indicated by setting `OPCODE = 1`.
  2. `NORMAL`
     * A `NORMAL` request contains actual data and will be indicated by setting `OPCODE = 0`.
  3. `TAIL`
     * A `TAIL` request will signify the end of data transmission and will be indicated by setting `OPCODE = 2`. 

  

### Ensuring Orderly Packet Arrival

* By the nature of how the network works, the order in which packets are sent to the server may be different than the order in which the server receives those packets.

  * An error in order would produce an incorrect sequence of the actual data being sent.

* In order to ensure the server will receive the packets in order, the client will use the 16-bit field `qclass` in the `Question Record` as a sequence count for each packet.

  * The `HEAD` packet will have `qclass = 0`.

  * The `NORMAL` packets that are sent will have `qclass = 1` to `qclass = <num_packets>`.

  * The `TAIL` packet will have `qclass = <num_packets> + 1`.

    

### Constraints

* The `qclass` field is limited to `16` bits which is equal to `2^16 = 65536` possible sequence numbers.

  * We use `0` to indicate the `HEAD` packet and we use `<num_packets> + 1` to indicate the `TAIL` packet.

  * This means that there are only `65534` sequence numbers we can use when sending our data.

    * Since there are only a limited number of sequence numbers we can use, the server can only request the content of files up to a certain file size.

    * This file size is dependent on the length of our domain since we can figure out the exact number of bytes we can pack into the `qname` once we know the length of the domain name.

      

### Dependencies

* **Python** (v3.7+)
  * Used to write the entire program.
* **Twisted** (v18.9.0)
  * Used for scheduling ping requests to the server.
* **Scapy** (v2.4.2)
  * Used to send custom DNS packets to the server and capture DNS responses.
* **pyffx** (v.0.2.0)
  * Used to encrypt data without changing its original length (which lets us pack more data into a request).







