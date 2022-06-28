# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 21:43:29 2022

@author: Niccolò Mussoni, Alessandro Sciarrillo
"""

import socket as sk
import threading

def handleDrones():
    while True:
        data, address = sock.recvfrom(4096)
        data = data.decode().split(' ')
    
        if data[0] == "READY":
            drone_id = data[1];
            connections[drone_id]=address
            available_drones.append(drone_id)
            print("Drone", drone_id, "connected")
        elif data[0] == "/delivered":
            available_drones.append(data[1])
            message = "Delivery completed by " + data[1]
            print('[SOURCE:', data[1], '  RECEIVER: Client] ==>', message)
            connectionSocket.send(message.encode())

def launchDrone(id_drone, delivery_address):
    message = delivery_address

    try:
        print ('[SOURCE: Client   RECEIVER:', id_drone + '] ==> Request delivery at', message)
        sock.sendto(message.encode(), connections[id_drone])
        available_drones.remove(id_drone)
    except Exception as info:
        print(info)

server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
server.bind(("localhost", 8100))
server.listen(2)

connections = dict()
available_drones = []

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
server_address = ('localhost', 8200)
sock.bind(server_address)
t = threading.Thread(target=handleDrones, args=())
t.start()

print('Ready to serve...')
connectionSocket, addr = server.accept()
print('Client connected')

while True:
    try:
        message = connectionSocket.recv(1024)
        message = message.decode()
        if message == "/drones":
            ans=""
            
            for drone in connections.keys():
                if drone in available_drones:
                    ans += drone + " Available\n"
                else:
                    ans += drone + " Not available\n"
                    
            connectionSocket.send(ans.encode())
        elif message.split(' ')[0] == "/ship":
            drone_id = message.split(' ')[1]
            delivery_address = ' '.join(message.split(' ')[2:])
            
            if drone_id in available_drones:
                t = threading.Thread(target=launchDrone, args=(drone_id, delivery_address))
                t.start()      
            else:
                message = "Drone " + drone_id + " is not available. Check the availables drones with /drones"
                connectionSocket.send(message.encode())
        
    except Exception as data:
        print (Exception,":",data)
        break
        connectionSocket.close()
        
connectionSocket.close()
