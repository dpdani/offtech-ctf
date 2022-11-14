import urllib.request, urllib.error
import time, random, sys

server_ip = "http://10.1.5.2/cmFuZG9tdXJs"

if len(sys.argv) != 2:
    print("Usage: python3 legitimate.py 1-9")
    exit(0)
rate = int(sys.argv[1])
if rate > 9:
    rate = 9
elif rate < 2:
    rate = 2

while True:
    try:
        contents = urllib.request.urlopen(server_ip).read() # GET requests the server
    except urllib.error.HTTPError as e:
        pass # Handle 404 and ignores it because be actually want to request a 404
    time.sleep(rate + random.uniform(-1, 1)) # Sleeps a random number of seconds between rate-1 and rate+1
    