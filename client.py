# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 21:44:39 2022

@author: Niccolò Mussoni, Alessandro Sciarrillo
"""

import socket as sk
import threading

def wait_response():
    response = clientsocket.recv(1024)
    response = response.decode()
    print (response)  

clientsocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

try:
    clientsocket.connect(("localhost",8106))
except Exception as data:
    print (Exception,":",data)

while True:
    request = input("Insert command: ")
    clientsocket.send(request.encode()) 
    t = threading.Thread(target=wait_response, args=())
    t.start()

clientsocket.close()