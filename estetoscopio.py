#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import signal

RED = "\u001b[31m"
GREEN = "\u001b[32m"
YELLOW = "\u001b[33m"
RESET = "\u001b[0m"

OK = f"{GREEN}[OK]{RESET}"
WARNING = f"{YELLOW}[WARNING]{RESET}"
ERROR = f"{RED}[ERROR]{RESET}"


def section(title):
    leader = '-' * (75 - len(title))
    print(f"--[{GREEN}{title}{RESET}]{leader}")


PORT = 31415

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', PORT)
print(f'Starting up on port {PORT}', end=" ")
sock.bind(server_address)
print(OK)

while True:
    try:
        print('Waiting to receive messages')
        data, address = sock.recvfrom(4096)
        section(f'Received {len(data)} bytes from {address}')
        data = data.decode("utf-8")
        level, message = data.split(":", 1)
        if level in ("DEBUG", "INFO", "WARNING"):
            print(f"{YELLOW}{data}{RESET}")
        else:
            print(f"{RED}{data}{RESET}")

    except KeyboardInterrupt:
        print("Finishing server", end=" ")
        sock.close()
        print(OK)
        break


