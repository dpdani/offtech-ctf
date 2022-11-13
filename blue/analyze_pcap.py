#! /usr/bin/env python

import sys
import pyshark
from flask import Flask, render_template
import json

from pyshark.capture.pipe_capture import PipeCapture
import threading

app = Flask(__name__)
packets_categories_dict = {"TCP": 0, "UDP": 0, "TCP SYN": 0, "ICMP": 0}
full_packets_list = []
http_req_packets_list = []


def thread_function(capture):

    print("Thread called")
    capture.apply_on_packets(print_callback)


def print_callback(pkt):
    # print(pkt)
    full_packets_list.append(pkt)
    if 'tcp' in pkt:
        packets_categories_dict["TCP"] = packets_categories_dict["TCP"] + 1
        # print("TCP: " + str(packets_categories_dict["TCP"]))
    if 'udp' in pkt:
        packets_categories_dict["UDP"] = packets_categories_dict["UDP"] + 1
        # print("UDP: " + str(packets_categories_dict["UDP"]))
    if 'icmp' in pkt:
        packets_categories_dict["ICMP"] = packets_categories_dict["ICMP"] + 1
        # print("ICMP: " + str(packets_categories_dict["ICMP"]))
    if 'http' in pkt:
        if hasattr(pkt.http, 'request_line'):
            http_req_packets_list.append(str(pkt.http))
            # print(pkt.http.field_names)


@app.route("/")
def root():
    print("TCP packets: " + str(packets_categories_dict["TCP"]))
    return render_template('index.html', TCP=packets_categories_dict["TCP"], UDP=packets_categories_dict["UDP"],
                           ICMP=packets_categories_dict["ICMP"])


@app.route("/get_categories")
def get_categories():
    return json.dumps(packets_categories_dict)


@app.route("/http")
def get_http_req():
    return render_template('http.html', list=http_req_packets_list)


if __name__ == '__main__':
    r = sys.stdin

    cap = PipeCapture(pipe=r)
    x = threading.Thread(target=thread_function, args=(cap,))
    x.start()

    app.run()
