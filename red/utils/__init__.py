import netifaces
from scapy.sendrecv import sendpfast

from red.config import config


def repeated(packet):
    return sendpfast(
        packet,
        pps=config.cli.pps,
        mbps=config.cli.bps / 1_000_000 if config.cli.bps is not None else None,
        loop=1_000,
        parse_results=True,
    )

def get_experiment_interface():
    for iface in netifaces.interfaces():
        try:
            addr = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']
        except KeyError: pass
        else:
            if addr.startswith('10.'):
                return iface
