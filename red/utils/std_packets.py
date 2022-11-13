from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether

from red.config import config


syn = (
        Ether()
        / IP(dst=config.server_host)
        / TCP(dport=config.server_port, flags='S')
)

ack_syn = (
        Ether()
        / IP(dst=config.server_host)
        / TCP(dport=config.server_port, flags='SA')
)

ack = (
        Ether()
        / IP(dst=config.server_host)
        / TCP(dport=config.server_port, flags='A')
)

__all__ = [
    'syn',
]
