# Tnnl Design Spec: Server

The server is designed to be the **source** for **commanding and controlling** infected clients over a botnet for exfiltrating data and delivering payloads. 



### Features

These are the main capabilities of the server:

1. Transmission of encoded commands to victim machines and process data transferred from client responses.
2. Ability to manage and sort data for multiple users to be stored on server hardware. Large files will be processed in a packet by packet basis until a terminating packet is sent by client.
3. Stores default configuration for client setup such as the time interval used by clients to query server and the identity the servers should be masked as.

### Hosting

The server itself can be hosted on a private server or a public cloud provider to carry out attacks.

Since this server program is written in Python, it is able to run on any instance that has Python 3.7+ installed.

### Dependencies

The server itself will require Python 3.7+ and Scapy to be installed. Scapy will be used for intercepting DNS packets that are sent by clients along with transmitting DNS responses containing information for client machines.

Scapy will allow us to be able to intercept packets that are sent from the clients for large data transfers along with obtaining results from executed from commands.

## Technical Details

These are crucial files that will be used by the server program.

**server.py**

* This is the starting point of the program where the attacker will start the service via the command line.
* The attacker can set different flags to change various settings such as the client-side time-interval for checking server-issued commands, directory to store exfiltrated data, and other configurations on how the client programs should mask itself to avoid detection.
* Here, the main thread will be used for issuing commands to various clients.
* A thread is started up for each given client-server connection from each thread from `datarecv.py`.

**datarecv.py**

* This class is used for handling the data that is being transferred from the clients to the server.
* It will maintain a mapping for each of the connected clients and will writ the corresponding extracted data in a folder that corresponds to that user.
  * Ideally, we should be able to create a folder for each user given their IP address and write the corresponding file contents in them.
  * Files will be written based on a prologue or beginning packet and will terminate once it receives a epilogue or terminating packet.
  * Files will be transferred one at a time whenever there is new data available from the client and read by the server.

**config.ini**

* The main configuration file that will be parsed by the program to load up existing settings.
* Settings will include:
  * Time-intervals for client to request for commands from the server.
  * The application the client and server will disguise as to keep communications covert if applicable.
  * The data rate at which the client should send data back to the server.