# Useful Information & Concepts

Just contains information that might be helpful in designing our C&C server for exfiltration.

## Exfiltration Methods
### DNS Tunneling
#### Summary
* DNS Tunnel uses a client server model, where the user’s computer (malware infected bot) runs 
DNS Tunneling client program and the attacker runs DNS Tunneling server program on his authoritative DNS server 
(C&C Server). The client sends data encoded in hostname label of a DNS Query and the server sends data encoded into 
the Resource Record (RR) of a DNS Response packet.

* DNS Tunneling program (or malware) encodes the payload data within DNS Query packet by using base64 encoding 
scheme then transmits the payload data as DNS Query to the server. Payload data is prepended as the hostname of a 
DNS Query. The server responds the query with its base64 encoded payload data in DNS Response packet by using RDATA 
field of various DNS Resource Record (RR) types. TXT, NULL and CNAME records are the most commonly used in DNS tunneling.

### Text-Based Steganography
#### Summary
