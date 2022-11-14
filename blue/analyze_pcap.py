#! /usr/bin/env python

import sys
import pyshark
from flask import Flask, render_template
import json

from pyshark.capture.pipe_capture import PipeCapture
import threading
from collections import OrderedDict

app = Flask(__name__)
packets_categories_dict = {"TCP": 0, "UDP": 0, "TCP SYN": 0, "ICMP": 0, "Others": 0}
ip_dict = {}
packets_timestamp_list = []
http_req_packets_list = []
total_http_delay = 0
date_dict = OrderedDict()


def thread_function(capture):

    print("Thread called")
    capture.apply_on_packets(analyze)


def analyze(pkt):
    # print(pkt)
    global total_http_delay
    packets_timestamp_list.append(pkt.sniff_timestamp)

    key = str(pkt.sniff_time.replace(microsecond=0))
    # print(key)
    if key in date_dict:
        date_dict[key] = date_dict[key]+1
    else:
        date_dict[key] = 1

    if 'ip' in pkt:
        if pkt.ip.src not in ip_dict:
            ip_dict[pkt.ip.src] = {"TCP": 0, "UDP": 0, "TCP SYN": 0, "ICMP": 0, "Others": 0}

    # TODO: do we analyze all the packets or discard the responses from the server ??? pkt.ip.src != "10.1.5.2
    if 'tcp' in pkt:
        packets_categories_dict['TCP'] = packets_categories_dict["TCP"] + 1
        ip_dict[pkt.ip.src]["TCP"] = ip_dict[pkt.ip.src]["TCP"] + 1
        if pkt.tcp.flags_syn == "1" and pkt.tcp.flags_ack == "0":
            packets_categories_dict['TCP SYN'] = packets_categories_dict["TCP SYN"] + 1
            ip_dict[pkt.ip.src]["TCP SYN"] = ip_dict[pkt.ip.src]["TCP SYN"] + 1
        if 'http' in pkt:
            if hasattr(pkt.http, 'request_line'):  # if it is a HTTP request
                http_req_packets_list.append([str(pkt.sniff_time), pkt.ip.src, pkt.tcp.srcport, pkt.http.request_method,
                                              pkt.http.request_uri, pkt.http.request_version, pkt.http.host,
                                              pkt.http.user_agent])
                # print(pkt.http.field_names)
            if hasattr(pkt.http, 'request_in'):  # if it is a HTTP response
                req_timestamp = packets_timestamp_list[int(pkt.http.request_in) - 1]  # -1 because frame index start from 1
                # print(req_pkt)
                approximate_delay = float(pkt.sniff_timestamp) - float(req_timestamp)
                # print("delay: " + str(approximate_delay))
                total_http_delay += approximate_delay

    elif 'udp' in pkt:
        packets_categories_dict["UDP"] = packets_categories_dict["UDP"] + 1
        ip_dict[pkt.ip.src]["UDP"] = ip_dict[pkt.ip.src]["UDP"] + 1
        # print("UDP: " + str(packets_categories_dict["UDP"]))
    elif 'icmp' in pkt:
        packets_categories_dict["ICMP"] = packets_categories_dict["ICMP"] + 1
        ip_dict[pkt.ip.src]["ICMP"] = ip_dict[pkt.ip.src]["ICMP"] + 1
        # print("ICMP: " + str(packets_categories_dict["ICMP"]))
    else:
        packets_categories_dict["Others"] = packets_categories_dict["Others"] + 1
        # ip_dict[pkt.ip.src]["Others"] = ip_dict[pkt.ip.src]["Others"] + 1 # NON IP protocol...


@app.route("/index.html")
@app.route("/")
def root():
    return render_template('index.html')


@app.route("/http.html")
def http():
    if len(http_req_packets_list) > 0:
        return render_template('http.html', avg_delay=(total_http_delay / len(http_req_packets_list)))
    else:
        return render_template('http.html', avg_delay=0)


@app.route("/ip.html")
def ip():
    return render_template('ip.html')


@app.route("/get_categories")
def get_categories():
    return json.dumps(packets_categories_dict)


@app.route("/get_http_req")
def get_http_req():
    ret = {"data": http_req_packets_list}
    return json.dumps(ret)


@app.route("/get_ips")
def get_ips():
    ip_dict.pop('10.1.5.2', None)  # do not count the server in the source IP statistics
    ret = []
    for key, data in ip_dict.items():
        ret.append([key, data["TCP"], data["UDP"], data["ICMP"], data["Others"]])

    return json.dumps({"data": ret})


@app.route("/get_pkt_sec")
def get_pkt_sec():
    ret = []
    for key, data in date_dict.items():
        ret.append({"x": key, "y": data})
    return json.dumps(ret[-30:])


if __name__ == '__main__':

    cap = PipeCapture(pipe=sys.stdin)
    x = threading.Thread(target=thread_function, args=(cap,))
    x.start()

    app.run()
