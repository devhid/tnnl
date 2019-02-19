<h1 align="center">Useful Information & Concepts</h1>

<p align="center">Just contains information that might be helpful in designing our C&C server for exfiltration.</p>

## Exfiltration Methods
### DNS Tunneling
* DNS Tunnel uses a client server model, where the user’s computer (malware infected bot) runs 
DNS Tunneling client program and the attacker runs DNS Tunneling server program on his authoritative DNS server 
(C&C Server). The client sends data encoded in hostname label of a DNS Query and the server sends data encoded into 
the Resource Record (RR) of a DNS Response packet.

* DNS Tunneling program (or malware) encodes the payload data within DNS Query packet by using base64 encoding 
scheme then transmits the payload data as DNS Query to the server. Payload data is prepended as the hostname of a 
DNS Query. The server responds the query with its base64 encoded payload data in DNS Response packet by using RDATA 
field of various DNS Resource Record (RR) types. TXT, NULL and CNAME records are the most commonly used in DNS tunneling.

### Text-Based Steganography
* Steganography  is  the  art  of  hiding  information  within  other  less conspicuous  information  to  prevent  eavesdropping  by  way  of  hiding  its existence  in  the first place.

### HTTP/HTTPS
* In order to mask communications crossing the target’s network perimeter APT groups often implement covert channels. These channels are often encrypted in order to hide the contents of the communications. While there are many ways to establish malicious C&C channels, ports 80 and 443 are usually used due to the fact that only these ports are allowed for outgoing connections in properly secured corporate environments or governmental institutions.

Depending on the actual C&C and malware implementation, the communication which is being transmitted over HTTP/HTTPS ports can be a legit HTTP protocol or a binary communication. Additionally, malware might be connecting via proxies in order to mask the real location of the C&C server.

## What does PacketWhisperer do?

#### Short Summary
* Any sort of data that is needed from the client is first "cloaked" or encrypted as FQDN strings. These FQDN strings are then queried by DNS (using nslookup). To receive the encrypted data, the server captures the network traffic, extracts the payload, and then decrypts the FQDN strings.

#### Long Summary
* To make it all happen, PacketWhisper combines **DNS queries with text-based steganography**. Leveraging the Cloakify Toolset, it transforms the payload into a list of FQDN strings. PacketWhisper then uses the list of FQDNs to create sequential DNS queries, transferring the payload across (or within) network boundaries, with the data hidden in plain sight, and without the two systems ever directly connecting to a each other or to a common endpoint. The ciphers used by PacketWhisper provide multiple levels of deception to avoid generating alerts as well as to mislead analysis attempts.

* **To receive the data, you capture the network traffic containing the DNS queries**, using whatever method is most convenient for you. (See "Capturing The PCAP File" below for examples of capture points.) You then load the captured PCAP file into PacketWhisper (running on whatever system is convenient), which extracts the payload from the file and Decloakifies it into its original form.

* DNS is an attractive protocol to use because, even though it's a relatively slow means of transferring data, DNS is almost always allowed across network boundaries, even on the most sensitive networks.

* Important note: We're using DNS queries to transfer the data, not successful DNS lookups. PacketWhisper never needs to successfully resolve any of its DNS queries. In fact PacketWhisper doesn't even look at the DNS responses. This expands our use cases, and underscores the fact that we never need to control a domain we're querying for, never need to control a DNS Name Server handling DNS requests.

## Terminology
* **FDQN**: A fully qualified domain name (FQDN) is the complete domain name for a specific computer, or host, on the internet. The FQDN consists of two parts: the hostname and the domain name. For example, an FQDN for a hypothetical mail server might be mymail.somecollege.edu
