# -*- coding: utf-8 -*-
"""
@author: Niccolò Mussoni, Alessandro Sciarrillo
"""

import socket as sk
import threading

#Attende e gestisce i pacchetti in entrata nel socket UDP relativi ai droni
def handleDrones():
    while True:
        data, address = socketUDP.recvfrom(1024)
        data = data.decode().split(' ')
        drone_id = data[1]
        
        #Se il drone invia READY significa che si è connesso ed è pronto
        if data[0] == "READY":
            if drone_id not in connections.keys():
                logic_conn[drone_id]=data[2]
                connections[drone_id]=address
                available_drones.append(drone_id)
                print("Drone", drone_id, "connected (" + data[2] + ")")
            else:
                print("Drone", drone_id, "already connected")
        #Se il drone invia /delivered significa che ha completato la consegna
        elif data[0] == "/delivered":
            available_drones.append(drone_id)
            message = "Delivery completed by " + drone_id
            ip_drone = logic_conn[drone_id]
            print('[SOURCE:' , data[1] , '(' + ip_drone + ')  RECEIVER: Client (' + client_ip + ')] ==>', message)
            socketTCP.send(message.encode())
        #Se il drone invia close significa che si è disconnesso e non è più disponibile
        elif data[0] == "/close":
            logic_conn.pop(drone_id)
            connections.pop(drone_id)
            
            if drone_id in available_drones:
                available_drones.remove(drone_id) 
                
            print("Drone", drone_id, "disconnected")

#Gestisce il lancio di un drone a uno specifico indirizzo 
def launchDrone(drone_id, delivery_address):
    message = delivery_address

    try:
        ip_drone = logic_conn[drone_id]
        print ('[SOURCE: Client (' + client_ip + ')  RECEIVER:', drone_id , '(' + ip_drone + ')] ==> Request delivery at', message)
        available_drones.remove(drone_id)
        socketUDP.sendto(message.encode(), connections[drone_id])
    except Exception as info:
        print(info)


logic_conn = dict()
connections = dict()
available_drones = []
client_ip=""

#Creazione socket TCP
server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
server.bind(("localhost", 8400))
server.listen(2)

#Creazione socket UDP
socketUDP = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
server_address = ('localhost', 8200)
socketUDP.bind(server_address)
t = threading.Thread(target=handleDrones, args=())
t.start()

print('Ready to serve...')
#Attende la connessione del client TCP
socketTCP, address_Client = server.accept()

while True:
    try:
        message = socketTCP.recv(1024)
        message = message.decode()
        
        #Se il client invia /drones, risponde con la lista di droni e la loro disponiblità
        if message == "/drones":
            ans=""
            for drone in connections.keys():
                ans += drone + " (" + logic_conn[drone] +  ")"
                if drone in available_drones:
                    ans += " Available\n"
                else:
                    ans += " Not available\n"
                    
            socketTCP.send(ans.encode())
        #Se il client invia /ship, controlla che ci siano almeno 3 argomenti e gestisce il lancio del drone
        elif message.split(' ')[0] == "/ship" and len(message.split(' ')) >= 3:
            drone = message.split(' ')[1]
            delivery_address = ' '.join(message.split(' ')[2:])
            
            #Se è stato passato l'ip, lo converte in ID del drone
            if drone in logic_conn.values():
                drone = [k for k, v in logic_conn.items() if v == drone][0]
                
            if drone in available_drones:     
                t = threading.Thread(target=launchDrone, args=(drone, delivery_address))
                t.start()
            else:
                #Se il messaggio è indirizzato a un IP che fa parte della subnet del client, allora viene
                #comunicato al client che non è necessario l'utilizzo del gateway per questo compito 
                if len(drone.split('.')) == 4 and '.'.join(drone.split('.')[:3]) == "192.168.1":
                    message = "The given IP belongs to your subnet and doesn't need this gateway"
                else:
                    message = "Drone " + drone + " is not available. Check availables drones with /drones"
                    
                socketTCP.send(message.encode())
        #Se il client invia /hello e il suo IP, si salva l'IP controllando che non sia già salvato
        elif message.split(' ')[0] == '/hello' and not client_ip:
            client_ip = message.split(' ')[1]
            print("Client connected (" + client_ip + ")")
        
    except Exception as data:
        print (Exception,":",data)
        socketTCP.close()
        break
        
socketTCP.close()
