# -*- coding: utf-8 -*-
"""
@author: Niccolò Mussoni, Alessandro Sciarrillo
"""

import socket as sk
import threading

#Attende le risposte del gateway relative alle richieste inoltrate
def wait_response():
    response = clientsocket.recv(1024)
    response = response.decode()
    print (response)

clientsocket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)

def closeClient(sock, request):
    print("\nClosing...")
    sock.send(request.encode())
    sock.close()

try:
    clientsocket.connect(("localhost",8100))
    #Simula la connessione e la comunicazione del proprio IP al gateway
    message="/hello 10.10.10.101"
    clientsocket.send(message.encode())
    print("Connected to Gateway\n")    
    print("CLIENT CONSOLE: Use /help for list of commands")
    
    while True:
        request = input("Insert command: ")
        
        if request == '/help':
            print("Commands:")
            print("/drones:\t Get list of all drones, with info about availability")      
            print("/ship <drone_id / drone_ip> <delivery_address>:\t Use a drone to ship to a specific address")
            print("/close:\t Close the connection to the Gateway")
            
        elif request == '/drones' or request.split(' ')[0] == '/ship':
            if request.split(' ')[0] == '/ship':
                print("Ship request sent to gateway")
            
            #Manda una richiesta al gateway e avvia un thread che si mette in attesa della risposta
            clientsocket.send(request.encode()) 
            t = threading.Thread(target=wait_response, args=())
            t.start()
        elif request == '/close':
            closeClient(clientsocket, request)
            break
        else:
            print("Command not found")
except Exception as data:
    print (Exception,":",data)
except KeyboardInterrupt:
    closeClient(clientsocket, '/close')