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
* For every client that **pings** the server the first time, a new directory will be created named after the victim's IP address in the data folder (more information below).
* There will be 3 types of requests that the server will receive from the clients (specified in `request_type.py`). All clients will be identified by their IPv4 addresses:
  * PING - corresponds to client request to check for available commands.
  * DATA - packets that contain data corresponding to the current file transmission.
  * RECEIPT - results or output from running commands on client machines.
* For handling DATA and RECEIPT requests, it will maintain a mapping for each of the connected clients and will write the corresponding extracted data in a folder that corresponds to that user (identified by IP address).
  * Ideally, we should be able to create a folder for each user given their IP address and write the corresponding file contents in them.
  * Files will be written based on a prologue or beginning packet and will terminate once it receives a epilogue or terminating packet.
  * Files will be transferred one at a time whenever there is new data available from the client and read by the server.
* The data being sent in the server will mainly be encoded within the DNS request URL from the client.
  * One part of the entire domain will be reserved for the metadata, the actual payload, and the domain name.
    ```
    <metadata>.<payload>.server.com
    ```
    * We have to keep in mind that the domain names do have a size constraint of 255 bytes or 255 chars (which includes every character including the periods).
    * Therefore, we need to store only essential information as metadata, like the sequence of the packet (so they can be reordered if needed).
    * The QTYPE of the DNSQR field will store the value that corresponds the payload to the type of data being transmitted, like PING, FILE, and RECEIPT.

**cmdqueue.py**

* This file will hold the commands that will execute on victim machines after being read from a directory.
* The commands to be executed can be placed inside `./data` folder or whatever location specified by the configuration file (folder structure shown below).
* The input folder of the victim will hold the commands to be executed and will be read periodically.
* *tnnl* will support two types of commands:
  *  bash - commands that will be executed in the victim's shell
  * get - used for retrieving any file on victim machines, with the syntax `get: <file_path>`.

**config.ini**

* The main configuration file that will be parsed by the program to load up existing settings.
* Settings will include:
  * Time-intervals for client to request for commands from the server.
  * The application the client and server will disguise as to keep communications covert if applicable.
  * The data rate at which the client should send data back to the server.
  * More will be added in future iterations.

### Folder Structure

```
data/
├── 130.43.66.24/
│   ├── input/
│   └── output/
├── 75.25.64.188/
└── 12.53.155.64/
```

* The data folder will contain directories that correspond to each victim machine with a given IP address.
  * The `input` folder will contain text files that are placed by the attacker containing commands to be issued. Once the server processes the commands, the file read will be deleted.
  * The `output` folder will contain files retrieved by the client programs along with the output logs from executed commands if available.