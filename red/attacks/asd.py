from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp, srp1

from red.config import config
from red.utils import repeated
from red.utils.std_packets import *


def run():
    packets = [
        syn,
        (
                Ether() /
                IP(dst=config.server_host) /
                TCP(dport=config.server_port) /
                "GET /1.html HTTP/1.0\r\n\r\n"
        )
    ]
    for packet in packets:
        packet.show()
    # sendp(packets)
    # srp1(packets[1])
    print(srp1(syn))
    # print(repeated(packets))
