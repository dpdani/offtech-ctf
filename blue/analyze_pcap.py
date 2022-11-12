#! /usr/bin/env python

import sys
import pyshark
from pyshark.capture.pipe_capture import PipeCapture


def print_callback(pkt):
    print(pkt)



if __name__ == '__main__':

    r = sys.stdin

    cap = PipeCapture(pipe=r)  # open the capture file using the pyshark library

    cap.apply_on_packets(print_callback)







