# internal imports
from threading.sniffer import Sniffer
from threading.pinger import Pinger

def main():
    sniffer = Sniffer(interface="eth0", packet_filter="src port 53")
    sniffer.start()

    pinger = Pinger(ping_interval=60)
    pinger.start()

if __name__ == "__main__":
    main()