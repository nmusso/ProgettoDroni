#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Niccolò Mussoni, Alessandro Sciarrillo
"""

import socket as sk
import time
import random

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)

server_address = ('localhost', 8200)
#Invia messaggio al gateway per la connessione
message = "/ready D1 192.168.1.101"
sock.sendto(message.encode(), server_address) 
print("Connected to Gateway")

while True:
    try:
        print('Ready to ship...')
        data, address = sock.recvfrom(1024)
        
        delivery_address=data.decode()
        print("Shipping at", delivery_address + "...")
        time.sleep(random.randrange(15,20,1))
        
        print("Package delivered at", delivery_address)
        #Invia messaggio di avvenuta consegna
        data1='/delivered D1'
        sock.sendto(data1.encode(), address)
    #Gestisce un eventuale interruzione da tastiera
    except KeyboardInterrupt:
        print("Closing...")
        data='/close D1'
        sock.sendto(data.encode(), server_address)
        sock.close()
        break