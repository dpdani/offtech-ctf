from scapy.sendrecv import sendpfast

from red.config import config


def repeated(packet):
    return sendpfast(
        packet,
        pps=config.cli.pps,
        mbps=config.cli.bps / 1_000_000,
        loop=10000
    )
