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
        drone_id = data[1]
        
        if data[0] == "READY":
            logic_conn[drone_id]=data[2]
            connections[drone_id]=address
            available_drones.append(drone_id)
            print("Drone", drone_id, "connected")
        elif data[0] == "/delivered":
            available_drones.append(drone_id)
            message = "Delivery completed by " + drone_id
            ip_drone = logic_conn[drone_id]
            print('[SOURCE:' , data[1] , '(' + ip_drone + ')  RECEIVER: Client (192.168.0.1)] ==>', message)
            connectionSocket.send(message.encode())
        elif data[0] == "/close":
            print("TODO")

def launchDrone(drone_id, delivery_address):
    message = delivery_address

    try:
        ip_drone = logic_conn[drone_id]
        print ('[SOURCE: Client (192.168.0.1)  RECEIVER:', drone_id , '(' + ip_drone + ')] ==> Request delivery at', message)
        sock.sendto(message.encode(), connections[drone_id])
        available_drones.remove(drone_id)
    except Exception as info:
        print(info)

server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
server.bind(("localhost", 8400))
server.listen(2)

logic_conn = dict()
connections = dict()
available_drones = []

sock = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
server_address = ('localhost', 8200)
sock.bind(server_address)
t = threading.Thread(target=handleDrones, args=())
t.start()

print('Ready to serve...')
connectionSocket, address_Client = server.accept()
print('Client connected')

while True:
    try:
        message = connectionSocket.recv(1024)
        message = message.decode()
        if message == "/drones":
            ans=""
            for drone in connections.keys():
                ans += drone + " (" + logic_conn[drone] +  ")"
                if drone in available_drones:
                    ans += " Available\n"
                else:
                    ans += " Not available\n"
                    
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
        connectionSocket.close()
        break
        
connectionSocket.close()
