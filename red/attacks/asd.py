import random

import typer
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import send, sr1

from red.config import config


# from red.utils.std_packets import *


def packet_title(message):
    typer.secho(message, fg='blue')


def run():
    # client = TCP_client.tcplink(Raw, config.server_host, config.server_port)
    # client.sr1(Raw(b"GET /1.html HTTP/1.0\r\n\r\n"))
    # packets = [
    #     syn,
    #     (
    #             Ether() /
    #             IP(dst=config.server_host) /
    #             TCP(dport=config.server_port) /
    #             "GET /1.html HTTP/1.0\r\n\r\n"
    #     )
    # ]
    # for packet in packets:
    #     packet.show()
    # sendp(packets)
    # srp1(packets[1])
    # srp1(syn)
    # print(repeated(packets))

    syn = IP(dst=config.server_host) / TCP(sport=random.randint(1025, 65500), dport=80, flags='S')
    packet_title(" [>] SYN")
    syn.show()
    # GET SYNACK
    syn_ack = sr1(syn)
    packet_title(" [<] ACK SYN")
    syn_ack.show()
    # Send ACK
    out_ack = (
            IP(dst=config.server_host)
            / TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack,
                  ack=syn_ack[TCP].seq + 1, flags='A')
    )
    packet_title(" [>] ACK")
    out_ack.show()
    send(out_ack)
    # Send the HTTP GET
    request = (
            IP(dst=config.server_host)
            / TCP(dport=80, sport=syn_ack[TCP].dport, seq=syn_ack[TCP].ack,
                  ack=syn_ack[TCP].seq + 1, flags='P''A')
            / b"GET /1.html HTTP/1.0\r\n\r\n")
    packet_title(" [>] GET")
    request.show()
    response = sr1(request)
    packet_title(" [<] response")
    response.show()
