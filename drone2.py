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

server_address = ('localhost', 8200)
message = "READY D2"
sock.sendto(message.encode(), server_address) 
print("Connected to Server")

while True:
    print('Ready to ship...')
    data, address = sock.recvfrom(4096)
    
    delivery_address=data.decode()
    print("Shipping at", delivery_address + "...")   
    time.sleep(random.randrange(15,20,1))
    
    print("Package delivered at", delivery_address)
    data1='/delivered D2'
    sock.sendto(data1.encode(), address)