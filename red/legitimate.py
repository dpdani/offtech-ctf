import urllib.request
import time, random

server_ip = "http://10.1.5.2"
while True:
    contents = urllib.request.urlopen(server_ip).read()
    time.sleep(random.randint(1,10))