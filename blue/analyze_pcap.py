#! /usr/bin/env python

import sys
import pyshark
#import tkinter as tk
from pyshark.capture.pipe_capture import PipeCapture

packets_categories_dict = {"TCP": 0, "UDP": 0, "TCP SYN": 0, "ICMP": 0}


def print_callback(pkt):
    #print(pkt)
    if 'tcp' in pkt:
        packets_categories_dict["TCP"] = packets_categories_dict["TCP"]+1
        print("TCP: " + str(packets_categories_dict["TCP"]))
    if 'udp' in pkt:
        packets_categories_dict["UDP"] = packets_categories_dict["UDP"]+1
        print("UDP: " + str(packets_categories_dict["UDP"]))
    if 'icmp' in pkt:
        packets_categories_dict["ICMP"] = packets_categories_dict["ICMP"]+1
        print("ICMP: " + str(packets_categories_dict["ICMP"]))


if __name__ == '__main__':

    r = sys.stdin

    #window = tk.Tk()

    cap = PipeCapture(pipe=r)  # open the capture file using the pyshark library

    cap.apply_on_packets(print_callback)








