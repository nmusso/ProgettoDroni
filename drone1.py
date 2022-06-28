#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 15:18:32 2022

@author: Niccolò Mussoni, Alessandro Sciarrillo
"""

import socket as sk
import time
import random

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 8001)
sock.bind(server_address)

ok=True

while True:
    print('\n\r ready to ship...')
    data, address = sock.recvfrom(4096)
    
    if data.decode('utf8')=="/areUready" and ok:
        data1="READY"
        sock.sendto(data1.encode(), address)
        ok=False
    elif data.decode('utf8')!="/areUready":
        print ("Address to ship: ",data.decode('utf8'))
        
        data1='Pack delivered'
        time.sleep(random.randrange(15,20,1))
        
        sent = sock.sendto(data1.encode(), address)

