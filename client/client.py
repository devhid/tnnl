# internal imports
from tasks.sniffer import Sniffer
from tasks.pinger import Pinger
from utils.consts import INTERFACE, PING_INTERVAL, SNIFF_FILTER

def main():
    pinger = Pinger(ping_interval=PING_INTERVAL)
    pinger.start()

    sniffer = Sniffer(interface=INTERFACE, packet_filter=SNIFF_FILTER)
    sniffer.start()

if __name__ == "__main__":
    main()