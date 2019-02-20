<h1 align=center>Project Team & Initial Specifications</h1>

## Team Members
1. Mankirat Gulati
2. Stanley Lim

## Specifications
### Platform / OS
* Both our client and server machines will have Linux-based operating systems.

### Architecture
* Intel x86

### Technologies
* Python

### Features
* Text-based Steganography + DNS Queries
* **Command Transmission**
    * Commands are transmitted to the victim machine with custom malware running to deliver any payload.
    * The malware running on the client machine will execute them after decoding the hidden string.
* **Asynchronous or Periodic Transmission**
    * Notifications of any piece of data or status on the victim machine will be transmitted periodically and asynchronously.
    * The data will return the return values of commands or return various details about the victim machine.
* **Data Exfiltration**
    * Large files and sensitive data can be transferred to and from the victim and the attacker-controlled server.
    * The data transfer may occur periodically or at random times to mask this communication.
    * Additional configurations can be included in the settings file for masking connections as being sent from other applications, like Firefox.