#! /usr/bin/env python

import socket
import sys
from dealer.player import Player
from dealer_proxy import Dealer_Proxy
from convert import *

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 9997)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

try:
    sock.sendall("sign-up")
    response = Convert.listen(sock)

    if response == "ok":
        dealer_proxy = Dealer_Proxy(Player(), sock)
        dealer_proxy.wait_for_start()

        while True:
            continue

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()