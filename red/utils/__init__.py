import ipaddress
import random
import struct

import netifaces
from scapy.sendrecv import sendpfast

from red.config import config


def repeated(packet):
    return sendpfast(
        packet,
        pps=config.attack.cli.pps,
        mbps=config.attack.cli.bps * 8 if config.attack.cli.bps is not None else None,
        loop=1000000000,
        parse_results=True,
        file_cache=True,
    )

def get_experiment_interface_and_ip():
    for iface in netifaces.interfaces():
        try:
            addr = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
        except KeyError: pass
        else:
            if addr.startswith('10.'):
                return iface, addr

def random_port():
    return random.randint(1025, 64000)

def spoof_ip():
    def random_ip(network):
        network = ipaddress.IPv4Network(network)
        network_int, = struct.unpack("!I", network.network_address.packed)  # make network address into an integer
        rand_bits = network.max_prefixlen - network.prefixlen  # calculate the needed bits for the host part
        rand_host_int = random.randint(0, 2 ** rand_bits - 1)  # generate random host part
        ip_address = ipaddress.IPv4Address(network_int + rand_host_int)  # combine the parts
        return ip_address.exploded

    network = "10.0.0.0/8"
    ip = random_ip(network)
    while ip in config.attack.spoof_blacklist:
        ip = random_ip(network)
    return ip
