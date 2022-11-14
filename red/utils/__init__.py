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
