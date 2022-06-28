# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 21:43:29 2022

@author: Niccolò Mussoni, Alessandro Sciarrillo
"""

import socket as sk
import threading
import time

def checkReadyDrone(port):
    while True:
        time.sleep(1)
        sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        server_address = ('localhost', port)
        message = "/areUready"
    
        try:
            sock.sendto(message.encode(), server_address)
            data, server = sock.recvfrom(4096)
            recived_message=data.decode('utf8')     
            print("recived_message: ",recived_message," port: ",port)
            if recived_message=="READY":
                if port==8001:
                    available_drones.append("d1")   
                elif port==8002:
                    available_drones.append("d2") 
                elif port==8003:
                    available_drones.append("d3") 
        except Exception as info:
            print(info)
        finally:
            sock.close()


def connectAndLaunchDrone(delivery_address):
    sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    server_address = ('localhost', 8001)
    message = delivery_address

    try:
        print ('sending "%s"' % message)
        sent = sock.sendto(message.encode(), server_address)
        available_drones.remove("d1")

        # Ricevete la risposta dal server
        print('waiting to receive from')
        data, server = sock.recvfrom(4096)
        recived_message=data.decode('utf8')
        print ('received message: "%s"' % recived_message)
        
        if recived_message=="Pack delivered":
            available_drones.append("d1")
            
    except Exception as info:
        print(info)
    finally:
        print ('closing socket')
        sock.close()

def sendToDrone(ip, delivery_address):
    #print("Connessione UDP.send(address) se disponibile")
    print(ip, ", ", delivery_address)
    connectAndLaunchDrone(delivery_address)
    message = "Consegna avvenuta da " + ip
    connectionSocket.send(message.encode())
    
server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
server.bind(("localhost", 8106))
server.listen(2)

available_drones = []

print('Ready to serve...')
connectionSocket, addr = server.accept()
#print(connectionSocket,addr)

ports=[8001, 8002, 8003]
t1 = threading.Thread(target=checkReadyDrone, args=(ports[0],))
t1.start()
t2 = threading.Thread(target=checkReadyDrone, args=(ports[1],))
t2.start()
t3 = threading.Thread(target=checkReadyDrone, args=(ports[2],))
t3.start()


while True:
    try:     
        message = connectionSocket.recv(1024)
        message = message.decode()
        if message == "/drones":
            connectionSocket.send((','.join(available_drones)).encode())
        elif message.split(' ')[0] == "/ship":
            drone_id = message.split(' ')[1]
            delivery_address = message.split(' ')[2]
            
            ip_drone = "192.168.1.10" + drone_id
            
            if drone_id in available_drones:
                t = threading.Thread(target=sendToDrone, args=(ip_drone, delivery_address))
                t.start()      
            else:
                message = "Drone "+drone_id+" is not available. Check the availables drones with /drones"
                connectionSocket.send(message.encode())
        
    except Exception as data:
        print (Exception,":",data)
        break
        connectionSocket.close()
        
connectionSocket.close()
