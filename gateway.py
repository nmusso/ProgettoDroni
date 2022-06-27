# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 21:43:29 2022

@author: Niccolò Mussoni, Alessandro Sciarrillo
"""

import socket as sk
import time
import random

def sendToDrone(ip, address):
    #print("Connessione UDP.send(address) se disponibile")
    print(ip, ", ", address)
    #Simula attesa e risposta
    time.sleep(random.randrange(2,5,1))
    message = "Consegna avvenuta da " + ip
    connectionSocket.send(message.encode())
    
server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
server.bind(("localhost", 8100))
server.listen(2)

available_drones = ["Drone1"]

print('Ready to serve...')
connectionSocket, addr = server.accept()
print(connectionSocket,addr)

while True:
    try:     
        message = connectionSocket.recv(1024)
        message = message.decode()
        if message == "/drones":
            connectionSocket.send("Lista droni disponibili risposta prova".encode())
        elif message.split(' ')[0] == "/ship":
            drone_id = message.split(' ')[1]
            drone_address = message.split(' ')[2]
            
            ip_drone = "192.168.1.10" + drone_id
            sendToDrone(ip_drone, drone_address)          
        
    except Exception as data:
        print (Exception,":",data)
        connectionSocket.close()
        
connectionSocket.close()
