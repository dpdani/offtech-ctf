from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether

from red.config import config


def run():
    packet = (
            Ether() /
            IP(dst=config.server_host) /
            TCP(dport=config.server_port) /
            "GET /1.html HTTP/1.1\r\n\r\n"
    )
